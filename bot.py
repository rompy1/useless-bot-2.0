import discord
import random
import time
from discord.ext import commands
from random import randrange
import shelve

previous_authors = {}
game = 0


bot = commands.Bot(command_prefix='^', description="I am a test")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = 0

@bot.command(aliases = ["p"])
async def ping(ctx):
    """Says Pong!"""
    await ctx.send("Pong!")


@bot.command(aliases = ["ss"])
async def storystart(ctx, a: str):
    """start a 1 word story game"""
    await ctx.send("You have created a new story under the name of %s" % a)
    data = {'%s' % a : ["The story so far:"]}
    d = shelve.open("stories3.db")
    d[a] = data
    d.close


@bot.command(aliases = ["sw"])
async def storywrite(ctx, a: str, b: str):
    """write to a 1 word story"""
    if a not in previous_authors:
        await ctx.send(ctx.author.id)
        d = shelve.open("stories3.db")
        temp = d[a]
        temp2 = ""
        for item in temp[a]:
            temp2 += item
            temp2 += " "
        await ctx.send(temp2)
        temp[a].append(b)
        d[a] = temp
        d.close
        await ctx.send("Your word has been added!")
        previous_authors[a] = ctx.author.id
    else:
        writer = ctx.author.id
        if writer == previous_authors[a]:
            await ctx.send("Wait your turn!")
        else:
            d = shelve.open("stories3.db")
            temp = d[a]
            temp2 = ""
            for item in temp[a]:
                temp2 += item
                temp2 += " "
            await ctx.send(temp2)
            temp[a].append(b)
            d[a] = temp
            d.close
            await ctx.send("Your word has been added!")
            previous_authors[a] = ctx.author.id


@bot.command(aliases = ["sr"])
async def storyread(ctx, a: str):
    """read a 1 word story"""
    d = shelve.open("stories3.db")
    temp = d[a]
    temp2 = ""
    for item in temp[a]:
        temp2 += item
        temp2 += " "
    await ctx.send(temp2)
    d.close

@bot.command(aliases = ["sl"])
async def storylist(ctx):
    """see all the 1 word stories"""
    d = shelve.open("stories3.db")
    await ctx.send("Stories:")
    for key in d:
        await ctx.send(key)


#only use below code on DB reset

cash = {}
players = []

@bot.command()
async def fixdb(ctx):
    """Fixes DB errors (Please do not use)"""
    db = shelve.open("slots")
    db["cash"] = cash
    db["players"] = players
    db.close

@bot.command()
async def bank(ctx):
    """work in progress"""
    player = str(ctx.author.id)
    db = shelve.open("slots")
    players = db["players"]
    cash = db["cash"]
    if player not in players:
        await ctx.send("New account registered!")
        players.append(player)
        db["players"] = players
        cash[player] = 1000
        db["cash"] = cash
    else:
        await ctx.send("Old account detected!")
    await ctx.send("Current cash: %d" % cash[player])
    db.close





random_emoji_list = ["🍒","💯",":seven:","🔔","🍎 ","🍊","🥝",]
game = [0]

@bot.command(aliases = ["gamble"])
async def slot(ctx):
    if game[0] == 1:
        await ctx.send("Oy, wait your turn!")
    else:
        game[0] = 1
        player = str(ctx.author.id)
        db = shelve.open("slots")
        players = db["players"]
        cash = db["cash"]
        if player not in players:
            await ctx.send("Please use the ^bank command to set up your account!")
        else:
            cash[player] -= 100
            rand1 = random.randint(0,6)
            rand2 = random.randint(0,6)
            rand3 = random.randint(0,6)
            msg = await ctx.send("Slot Machine: \n" + random_emoji_list[rand1] + random_emoji_list[rand2] + random_emoji_list[rand3])
            for i in range(5):
                rand1 = random.randint(0,6)
                rand2 = random.randint(0,6)
                rand3 = random.randint(0,6)
                await msg.edit(content = "Slot Machine:\n" + random_emoji_list[rand1] + random_emoji_list[rand2] + random_emoji_list[rand3])
                time.sleep(1)
            outcome = random.randint(1, 10)
            if outcome == 6:
                await msg.edit(content = "Slot Machine:\n" + "🥝🥝🥝 \n You're a winner! You have won 200 cash.")
                cash[player] += 200
            elif outcome == 7:
                await msg.edit(content = "Slot Machine:\n" + "🍊🍊🍊 \n You're a winner! You have won 150 cash.")
                cash[player] += 150
            elif outcome == 8:
                await msg.edit(content = "Slot Machine:\n" + "🔔🔔🔔 \n You're a winner! You have won 300 cash.")
                cash[player] += 300
            elif outcome == 9:
                await msg.edit(content = "Slot Machine:\n" + ":seven::seven::seven: \n SUPER WIN!!! You have won 500 cash.")
                cash[player] += 500
            elif outcome == 10:
                await msg.edit(content = "Slot Machine:\n" + "💯💯💯 \n JACKPOT!!!!! You have won 1000 cash.")
                cash[player] += 1000
            else:
                rand1 = random.randint(0,2)
                rand2 = random.randint(0,2)
                rand3 = random.randint(0,2)
                if rand3 == rand2 and rand3 == rand1:
                    while rand3 == rand2 and rand3 == rand1:
                        rand1 = random.randint(0,6)
                        rand2 = random.randint(0,6)
                        rand3 = random.randint(0,6)
                await msg.edit(content = "Slot Machine:\n" + random_emoji_list[rand1] + random_emoji_list[rand2] + random_emoji_list[rand3] + "\n I'm sorry, you didn't win anything!")
                db["cash"] = cash
            game[0] = 0
            db.close




@bot.command()
async def givemoney(ctx):
    player = str(ctx.author.id)
    db = shelve.open("slots")
    players = db["players"]
    cash = db["cash"]
    if player not in players:
        await ctx.send("Please use the ^bank command to set up your account!")
    else:
        cash[player] += 100
    db["cash"] = cash


@bot.command()
async def check(ctx):
    await ctx.send(ctx.author.check.is_admin())






@bot.command(aliases = ["re"])
async def randomemojis(ctx):
    rand1 = random.randint(0,6)
    rand2 = random.randint(0,6)
    rand3 = random.randint(0,6)
    msg = await ctx.send(random_emoji_list[rand1] + random_emoji_list[rand2] + random_emoji_list[rand3])
    for i in range(10):
        rand1 = random.randint(0,6)
        rand2 = random.randint(0,6)
        rand3 = random.randint(0,6)
        await msg.edit(content = random_emoji_list[rand1] + random_emoji_list[rand2] + random_emoji_list[rand3])
        time.sleep(1)













@bot.command()
async def shutdown(ctx):
    """shutdown the bot (admin only)"""
    if ctx.author.id == 192735146003267584 or 133642107259846657:
        exit()
    else:
        await ctx.send("I'm sorry, you don't have permission to do that!")

@bot.command()
async def me(ctx):
    """test code"""
    await ctx.send(ctx.author.id)





#lukeabby: 133642107259846657







bot.run("NDU2MDkxMTQ0NTAyMjQ3NDQ0.DgFkRQ.gh-URYH3pphRvTRAczQe00ofP4Y")
