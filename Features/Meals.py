import discord
from discord.ext import commands
from random import choice

class meals(commands.Cog):
    def __init__(self, bot):
        self.breakfast_list = [ '蛋餅配大冰奶', '燒餅油條配豆漿', '蔥抓餅加蛋', '牛奶麥片', '三明治', '麵包', '包子饅頭', '飯糰', '鬆餅', '豬肉滿福堡加蛋', '烤吐司', '鐵板麵',
                                '麵線羹', '鍋燒意麵', '控肉飯', '肉燥飯', '虱目魚粥', '不吃早餐才是一件很嘻哈的事 <:3_:569162222819999744>']
        meal_list = ['燒臘便當', '雞腿便當', '排骨便當', '鴨肉飯', '滷肉飯', '蛋包飯', '水餃', '鍋貼', '炒飯', '炒麵', '炒米粉', '拉麵', '咖哩飯', '義大利麵', '牛肉麵', '乾麵',
                     '丼飯', '炸豬排定食']
        self.lunch_list = ['沙拉', '魷魚羹', '涼麵', '自助餐', '空氣、陽光、水'] + meal_list
        self.dinner_list = ['小火鍋', '麻辣鍋', '鐵板燒', '壽司', '牛排', '麥當勞', '肯德基', '披薩'] + meal_list
        self.snack_list = ['鹽酥雞', '鹹水雞', '泡麵', '臭豆腐', '滷味', '麻辣燙', '雞排', '涼麵味噌湯', '麥當勞', '永和豆漿', '樓下便利商店']
        
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