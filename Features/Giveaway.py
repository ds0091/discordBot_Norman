import discord
from discord.ext import commands
from random import choice

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_terminate = False
        self.giveawayCnt = 0
        self.drawList = []


    def set_keyword(self, keyword):
        self.keyword = keyword


    def set_permission(self, permission):
        if(permission == 'all'):
            self.role = '@everyone'
        else:
            self.role = '我有付保護費'

    
    def set_channel(self,channel):
        self.in_channel = channel


    def check_permission(self, roles):
        for role in roles:
            if (self.role == str(role)):
                return True
        return False

    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if(msg.author != self.bot.user):
            if (self.is_terminate and self.keyword in msg.content):
                await msg.channel.send('你來晚了，抽獎報名已經截止囉')
            elif ((self.in_channel == msg.channel) and (self.keyword in msg.content) and self.check_permission(msg.author.roles)):
                if (msg.author.id not in self.drawList):
                    self.drawList.append(msg.author.id)
                    await msg.channel.send('<@!{}> 已加入抽獎名單中'.format(msg.author.id))
                else:
                    await msg.channel.send('<@!{}> 你已經在名單內，別再刷了'.format(msg.author.id))


    @commands.has_any_role('諾曼大帝', '有劍94屌')    
    @commands.command(name='截止', pass_context=True)
    async def giveaway_terminate(self, ctx):
        self.is_terminate = True
        await ctx.send('抽獎結束，究竟誰是歐洲人呢?')
    

    @commands.has_any_role('諾曼大帝', '有劍94屌')
    @commands.command(name='抽', pass_context=True)
    async def giveaway_draw(self, ctx):
        if (self.is_terminate):
            peopleRemain = len(self.drawList)
            if (peopleRemain != 0):
                winner = self.drawList.pop(choice(range(peopleRemain)))
                self.giveawayCnt+=1
                await ctx.send('恭喜歐洲人{} 號：<@!{}> 中獎啦'.format(self.giveawayCnt, winner))
            else:
                await ctx.send('已經沒有人可以抽了')
        else:
            await ctx.send('報名還沒截止，先別急著抽啊')
            


def setup(bot):
    bot.add_cog(giveaway(bot))