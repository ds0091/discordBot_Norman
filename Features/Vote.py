import discord
from discord.ext import commands
import string

class vote(commands.Cog):
    def __init__(self, bot):
        self.voted_list = {}
        self.desc = ''


    def set_vote(self, settings):
        self.numSelection = settings[0]
        self.numOption = settings[1]
        self.alphabet = list(string.ascii_uppercase[0:self.numOption])
        self.description_unlimited = '投票開始! 請從【A~{}】中選出「所有」你想選擇的選項'.format(self.alphabet[-1])
        self.description_limited = '投票開始! 請從【A~{}】中選出「{} 個」你想選擇的選項'.format(self.alphabet[-1], self.numSelection)

    
    def show_description(self, mode):
        if (mode == 'unlimited'):
            self.desc = self.description_unlimited
        elif (mode == 'limited'):
            self.desc = self.description_limited

        return self.desc


    def check_selections(self, selections):
        for sel in selections:
            if (sel not in self.alphabet):
                return '是不是混進了不在選項內的東西？\n使用【!投票】指令再看一次投票說明吧'
        numSel = len(selections)
        if (numSel != len(list(set(selections)))):
            return '就算是複選一個選項也只能選一次啦'
        if (numSel > self.numSelection):
            return '別太貪心，最多只能選擇 {} 項'.format(self.numSelection)
        else:
            return 'ok'

    
    def voteCount(self):
        voteStr = ''
        voteMax = []
        maxVoted = 0
        allVote = sum(self.voted_list.values(), [])
        for option in self.alphabet:
            optCnt = allVote.count(option)
            voteStr = voteStr + '{}：{} 票\n'.format(option, optCnt)
            if (maxVoted < optCnt):
                maxVoted = optCnt
                voteMax = [option]
            elif (maxVoted == optCnt):
                voteMax.append(option)
        maxVotedStr = ','.join(voteMax)
        
        resultStr = '得票數最高的選項為：{}，得票數為 {} 票'.format(maxVotedStr, maxVoted)
        return [voteStr, resultStr]
    

    @commands.command(name='投', pass_context=True)
    async def voting(self, ctx, selections: str, revote='n'):
        selections = selections.upper()
        checkStr = self.check_selections(selections)
        if (checkStr != 'ok'):
            await ctx.send(checkStr)
        else:
            user = ctx.message.author.id
            if (user in self.voted_list.keys()):
                if (revote != '-r'):
                    await ctx.send('<@!{}> 你已經投過票囉，想改變主意的話就用【!投 <選項> -r】'.format(user))
                else:
                    self.voted_list[user] = list(selections)
                    await ctx.send('<@!{}> 投票更改成功，你投給了{}'.format(user, ','.join(selections)))    
            else:
                selList = list(selections)
                self.voted_list[user] = selList
                selList = selList.sort()
                await ctx.send('<@!{}> 投票成功，你投給了{}'.format(user, ','.join(selList)))


    @commands.command(name='投票', pass_context=True)
    async def vote_description(self, ctx):
        await ctx.send(self.desc)                 



def setup(bot):
    bot.add_cog(vote(bot))