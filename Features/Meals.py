import discord
from discord.ext import commands
from random import choice

class meals(commands.Cog):
    def __init__(self, bot):
        self.breakfast_list = ['蛋餅', '燒餅']
        self.lunch_list = ['雞腿便當', '排骨便當']
        self.dinner_list = ['水餃', '炒飯']
        self.snack_list = ['鹽酥雞', '鹹水雞']
        
    @commands.command(name='早餐', pass_context=True)
    async def breakfast_recommend(self, ctx):
        recommend = choice(self.breakfast_list)
        await ctx.send('早餐推薦：{}'.format(recommend))
    

    @commands.command(name='午餐', pass_context=True)
    async def lunch_recommend(self, ctx):
        recommend = choice(self.lunch_list)
        await ctx.send('午餐推薦：{}'.format(recommend))


    @commands.command(name='晚餐', pass_context=True)
    async def dinner_recommend(self, ctx):
        recommend = choice(self.dinner_list)
        await ctx.send('晚餐推薦：{}'.format(recommend))


    @commands.command(name='宵夜', pass_context=True)
    async def snack_recommend(self, ctx):
        recommend = choice(self.snack_list)
        await ctx.send('宵夜推薦：{}'.format(recommend))



def setup(bot):
    bot.add_cog(meals(bot))