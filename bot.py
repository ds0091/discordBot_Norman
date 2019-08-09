import discord
from discord.ext import commands
import pytz
import datetime
import random

import Features.Weather
import Features.Giveaway

wx = Features.Weather.weather()

class NormansBot(commands.Bot):
    def __init__(self, **kwargs):
        commands.Bot.__init__(self, **kwargs)

bot = NormansBot(command_prefix='!', help_command=None)



def tz_converter(input_dt, current_tz='UTC', target_tz='Asia/Taipei'):
    current_tz = pytz.timezone(current_tz)
    target_tz = pytz.timezone(target_tz)
    target_dt = current_tz.localize(input_dt).astimezone(target_tz)
    return target_tz.normalize(target_dt) 


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


error_log = []
@bot.event
async def on_command_error(ctx, error):
    global error_log
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole, commands.NotOwner)):
        await ctx.send('你沒有權限使用這個指令喔 ^^')
    else:
        timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log.append(str(timeStamp) + ' | ' + str(error))


@commands.is_owner()
@bot.command(name='error', pass_context=True)
async def get_error_log(ctx, com: str):
    global error_log
    if (com == 'show'):
        if(error_log != []):
            errorStr = ''
            for err in error_log:
                errorStr = errorStr + err + '\n'
            await ctx.send(errorStr)
        else:
            await ctx.send('Log is empty.')
    elif(com == 'reset'):
        error_log = []



@bot.command(name='測試')
async def test(ctx):
    await ctx.send('<:3_:569162222819999744>')
    

@bot.command(name='加入', pass_context=True)
async def when(ctx):
    joinDate = tz_converter(ctx.message.author.joined_at).strftime("%Y-%m-%d %H:%M")
    await ctx.send('<@!{}> 在 {} 正式加入成為肉曼王國的一員'.format(ctx.message.author.id, joinDate))


@bot.command(name='天氣', pass_context=True)
async def weather(ctx, loc: str):
    weatherInfo = wx.get_weather(loc)
    if (weather == None):
        await ctx.send('找不到該縣市啦')
    else:
        warningStr = ''
        weatherNow = weatherInfo['weather'][0]
        weatherStr = '「{}」於 {} 開始六小時內\n天氣狀況：{}\n舒適度：{}\n氣溫：{}-{} 度\n降雨機率：{}%'.format(loc, weatherNow[0], weatherNow[1], weatherNow[4], weatherNow[3], weatherNow[5], weatherNow[2])
        uvStr = '\n\n({})\n當日最高紫外線指數：{} ({})'.format(weatherInfo['uvIndex'][1], weatherInfo['uvIndex'][0][0][1], weatherInfo['uvIndex'][0][0][0])
        if (len(weatherInfo['uvIndex'][0]) != 1):
            uvStr = uvStr + '\t{} ({})'.format(weatherInfo['uvIndex'][0][1][1], weatherInfo['uvIndex'][0][1][0])

        if (weatherInfo['warning'] != None):
            warningStr = '\n天氣警特報：{}'.format(weatherInfo['warning'])
        
        await ctx.send(weatherStr + warningStr + uvStr)

@bot.command(name='地震', pass_context=True)
async def earthquake(ctx):
    eqStr = ''
    earthquakes = wx.get_earthquake()
    for eq in earthquakes:
        eqStr = eqStr + eq + '\n'
    await ctx.send('最近一起或12小時內有感地震事件：\n{}'.format(eqStr))


@commands.has_any_role('諾曼大帝', '有劍94屌')
@bot.command(name='抽獎', pass_context=True)
async def giveaway_start(ctx, permission: str, keyword: str):
    if (permission != 'all' and permission != 'sub'):
        await ctx.send('請選擇抽獎模式：所有觀眾(all)/訂閱者限定(sub)')
    else:
        try:
            bot.load_extension('Features.Giveaway')
            set_limit = bot.get_cog('giveaway')
            set_limit.set_keyword(keyword)
            set_limit.set_permission(permission)
            set_limit.set_channel(ctx.message.channel)
            await ctx.send('抽獎開始! 輸入關鍵字「{}」進行抽獎'.format(keyword))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send('抽獎已經開始啦')
        

@commands.has_any_role('諾曼大帝', '有劍94屌')
@bot.command(name='抽獎結束', pass_context=True)
async def giveaway_end(ctx):
    try:
        bot.unload_extension('Features.Giveaway')
        await ctx.send('抽獎結束囉，感謝大家參與')
    except commands.ExtensionNotLoaded:
        await ctx.send('【抽獎尚未開始】')


todayAsked = ['']
@bot.command(name='運勢', pass_context=True)
async def luck_today(ctx):
    global todayAsked
    today = datetime.date.today()
    whoAsk = ctx.message.author.id

    if (todayAsked[0] != today):
        todayAsked = [today]
    if(whoAsk not in todayAsked):
        todayAsked.append(whoAsk)
        luck = random.randint(0, 9)
        if (luck >= 8):
            luckStr = '大吉'
        elif (luck >= 6):
            luckStr = '吉'
        elif (luck >= 3):
            luckStr = '普通'
        else:
            luckStr = '不好說'
        await ctx.send('今日運勢：{}'.format(luckStr))
    else:
        await ctx.send('你今天已經問過囉')




if __name__ == "__main__":
    bot.load_extension('Features.Meals')
    bot.run('NTkxNTYzMzA0MDQ5MzExNzc0.XUyCRQ.wU9WwiUaiQuW648G6ASTLnjr08w')
