from ast import alias
import datetime
from io import BytesIO
from turtle import title
import discord
from discord.ext import commands, tasks
import random
import os
from itertools import cycle
import sys
import asyncio
import time
import json
from PIL import Image
from requests import get
import animec
import aiohttp
import praw 
import requests



os.chdir('C:\\Users\\Riner\\Documents\\GitHub\\Discord-Bot')

TOKEN = 'lolz'

intents = discord.Intents().all()


client = commands.Bot(command_prefix = '!', intents=intents)
client.remove_command("help")



status = cycle([
    "My prefix is: '!'",
    'With you',
    'Waifu Dating Sim'
])

@tasks.loop(seconds = 40)
async def status_swap():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')
    await status_swap.start()




@client.command(aliases=['p', 'P', 'Ping'])
async def ping(ctx):
     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#@client.command()
#async def meme(ctx):
 #   content = get("https://meme-api.herokuapp.com/gimme").text
  #  data = json.loads(content,)
   # meme_Embed = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    #meme_Embed.set_footer(text='The meme command is under developing!')
    #await ctx.send(embed=meme_Embed)
     
@client.command(pass_context=True)
async def meme(ctx):
    
    if not hasattr(client, 'nextMeme'):
        client.nextMeme = getMeme()

    name, url = client.nextMeme
    meme_embed = discord.Embed(title = name, timestamp = ctx.message.created_at)
    meme_embed.set_footer(text="lolz", icon_url=ctx.author.avatar_url)

    meme_embed.set_image(url=url)

    await ctx.send(embed=meme_embed)
    
    client.nextMeme = getMeme()


def getMeme():
    subreddit = reddit.subreddit("meme")
    all_subs = []   

    top = subreddit.top(limit=70)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    return name, url
   

@client.command()
async def anime(ctx,*,query):
    try:
        anime = animec.Anime(query)
    except:
        await ctx.send(embed = discord.Embed(description='No anime found, so sad.', color = discord.Color.red()))
        return 

    if query == None:
        await ctx.send("Enter an anime")    

    anime_embed = discord.Embed(title = anime.title_english, url=anime.url,description = f"{anime.description[:200]}...", color = discord.Color.random())
    anime_embed.add_field(name= "English Name", value= str(anime.name))
    anime_embed.add_field(name = "Japanese Name", value = str(anime.title_jp))
    anime_embed.add_field(name= "Episodes", value= str(anime.episodes))
    anime_embed.add_field(name= "NSFW?", value= str(anime.is_nsfw()))
    anime_embed.add_field(name= "URL", value= str(anime.url))
    anime_embed.add_field(name= "Genres", value= str(anime.genres))
    anime_embed.add_field(name= "Episodes", value= str(anime.episodes))
    anime_embed.add_field(name= "Favorites", value= str(anime.favorites))
    anime_embed.add_field(name= "Alternative Names", value= str(anime.alt_titles))
    anime_embed.add_field(name= "Teaser", value= str(anime.teaser))
    anime_embed.set_thumbnail(url = anime.poster)
    anime_embed.set_footer(text=f'Requested by {ctx.author}')

    await ctx.send(embed = anime_embed)

@client.command(aliases=['char'])
async def character(ctx,*,query):
    try:
        char = animec.Charsearch(query)
    except:
        await ctx.send(embed = discord.Embed(description="No character found, so sad.", color = discord.Color.red()))
        return 

    if query == None:
        await ctx.send('Enter a character.')    

    char_embed = discord.Embed(title = char.title, url = char.url, color = discord.Color.random())
    char_embed.set_image(url = char.image_url)
    char_embed.set_footer(text= ', '.join(list(char.references.keys())[:2]))
    await ctx.send(embed = char_embed)

@client.command()
async def secret(ctx):
    await ctx.send(f'{ctx.author.mention} woah you found this "secret" command somehow, here is ur gift: **nothing bruh**')

@client.command(aliases=['aninews'])
async def animenews(ctx, amount:int=3):
    news = animec.Aninews(amount)
    links = news.links
    titles = news.titles 
    descriptions = news.description

    aninews_embed = discord.Embed(title = "Latest Anime News!", color = discord.Color.random())
    aninews_embed.set_thumbnail(url = news.images[0])

    for i in range(amount):
        aninews_embed.add_field(name= f"{i+1}) {titles[i]}", value = f"{descriptions[i][:200]}...\n[Read more]({links[1]})", inline = False)

    await ctx.send(embed = aninews_embed)

@client.command()
async def cool(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.author
    cool = random.randrange(101)
    cool_embed = discord.Embed(title='How Cool!', description = f"{user.mention} You are {cool}% Cool!", color = user.color)
    if cool <= 70:
        cool_embed.set_footer(text = 'Meh')
    elif cool <= 60:
        cool_embed.set_footer(text = "Ew")

    elif cool <= 90:
        cool_embed.set_footer(text= 'You are pog man')

    await ctx.send(embed = cool_embed)

@client.command()
async def howgay(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.author
    gay = random.randrange(101)
    gay_embed = discord.Embed(title='How gay!', description = f"{user.mention} You are {gay}% gay!", color = user.color)
    if gay <= 70:
        gay_embed.set_footer(text = 's u s')
    elif gay <= 60:
        gay_embed.set_footer(text = "sus")

    elif gay == 0:
        gay_embed.set_footer(text = ':o')

    elif gay <= 90:
        gay_embed.set_footer(text= 'S U S')

    elif gay == 100:
        gay_embed.set_footer(text= 'Ayo???')

    await ctx.send(embed = gay_embed)

@client.command(aliases=['howyuri'])
async def howlesbi(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.author
    lesbian = random.randrange(101)
    Lesbian_embed = discord.Embed(title='How Lesbi!', description = f"{user.mention} You are {lesbian}% lesbi!", color = user.color)
    if lesbian <= 70:
        Lesbian_embed.set_footer(text = 's u s')
    elif lesbian <= 60:
        Lesbian_embed.set_footer(text = "sus")

    elif lesbian == 0:
        Lesbian_embed.set_footer(text = ':o')

    elif lesbian <= 90:
        Lesbian_embed.set_footer(text= 'S U S')

    elif lesbian <= 100:
        Lesbian_embed.set_footer(text= 'Ayo???')    

    await ctx.send(embed = Lesbian_embed)    

@client.command()
async def howpro(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.author

    pro = random.randrange(101)
    pro_embed = discord.Embed(title='How pro!', description = f"{user.mention} You are {pro}% pro!", color = user.color)
    if pro <= 70:
        pro_embed.set_footer(text = 'you are just a tryhard, not a pro.')
    elif pro <= 60:
        pro_embed.set_footer(text = "yeah kinda")

    elif pro <= 90:
        pro_embed.set_footer(text= 'You are pog man')

    elif pro >= 20:
        pro_embed.set_footer(text = 'No friends')    

    await ctx.send(embed = pro_embed)
            
@client.command()
async def pp(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.author
    pp_list = ["8D", '8=D', '8==D', '8===D', '8====D', '8=====D', '8=====D', '8========D', '8==========D', '8, yeah u got no pp', '8================D']
    pp_embed = discord.Embed(title='PP!', description= f"{user.mention} your pp is:\n {random.choice(pp_list)}")
    pp_embed.set_footer(text = 'pp pp pp pp')
    await ctx.send(embed = pp_embed)

@client.command()
async def waifu(ctx):
    
    waifus = animec.Waifu.waifu()
    
    waifu_embed=discord.Embed(title = 'Waifu >-<!' ,url = waifus, color = ctx.author.color)
    waifu_embed.set_image(url = waifus)
    await ctx.send(embed=waifu_embed)

@client.command()
async def neko(ctx):
    
    neko = animec.Waifu.neko()
    
    neko_embed=discord.Embed(title = 'Neko >-<!' ,url = neko, color = ctx.author.color)
    neko_embed.set_image(url = neko)
    await ctx.send(embed=neko_embed)

@client.command()
async def kiss(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to kiss!!')
        return

    if member == ctx.author:
        await ctx.send('Wait what you can kiss yourself?')
        return    
    
    kiss = animec.Waifu.kiss()
    
    kiss_embed=discord.Embed(title = 'Kiss!', description = f'{ctx.author.mention} **Has kissed {member.mention}!!!**' ,url = kiss, color = ctx.author.color)
    kiss_embed.set_image(url = kiss)
    await ctx.send(embed=kiss_embed)

@client.command()
async def hug(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to hug!!')
        return
    
    hug = animec.Waifu.hug()
    
    hug_embed=discord.Embed(title = 'Hug!', description = f'{ctx.author.mention} **Has hugged {member.mention}!!!**' ,url = hug, color = ctx.author.color)
    hug_embed.set_image(url = hug)
    await ctx.send(embed=hug_embed)

@client.command()
async def lick(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to lick!!')
        return
    
    lick = animec.Waifu.lick()
    
    lick_embed=discord.Embed(title = 'Lick!', description = f'{ctx.author.mention} **Has licked {member.mention}!!!**' ,url = lick, color = ctx.author.color)
    lick_embed.set_image(url = lick)
    await ctx.send(embed=lick_embed)

@client.command()
async def pat(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to pat!!')
        return
    
    pat = animec.Waifu.pat()
    
    pat_embed=discord.Embed(title = 'Pat!', description = f'{ctx.author.mention} **Has patted {member.mention}!!!**' ,url = pat, color = ctx.author.color)
    pat_embed.set_image(url = pat)
    await ctx.send(embed=pat_embed)


@client.command()
async def bonk(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to bonk!!')
        return
    
    bonk = animec.Waifu.bonk()
    
    bonk_embed=discord.Embed(title = 'Bonk!', description = f'{ctx.author.mention} **Has Bonked {member.mention}!!!**' ,url = bonk, color = ctx.author.color)
    bonk_embed.set_image(url = bonk)
    await ctx.send(embed=bonk_embed)

@client.command()
async def bully(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to bully!!')
        return
    
    bully = animec.Waifu.bully()
    
    bully_embed=discord.Embed(title = 'Bully!', description = f'{ctx.author.mention} **Has Bullied {member.mention}!!!**' ,url = bully, color = ctx.author.color)
    bully_embed.set_image(url = bully)
    await ctx.send(embed=bully_embed)

@client.command()
async def howcute(ctx, member = None):
    if member == None:
        member = ctx.author
    
    cute = random.randrange(101)
    cute_embed = discord.Embed(title = 'How cute!', description = f'{member.mention} is {cute}% Cute!')
    await ctx.send(embed = cute_embed)        

@client.command()
async def cry(ctx):
    
    cry = animec.Waifu.cry()
    
    cry_embed=discord.Embed(title = 'Cry :(' ,url = cry, color = ctx.author.color)
    cry_embed.set_image(url = cry)
    cry_embed.set_footer(text = 'so sad')
    await ctx.send(embed=cry_embed)

@client.command()
async def awoo(ctx):
    
    awoo = animec.Waifu.awoo()
    
    awoo_embed=discord.Embed(title = 'Awoo!' ,url = awoo, color = ctx.author.color)
    awoo_embed.set_image(url = awoo)
    await ctx.send(embed=awoo_embed)    
 

@client.command()
async def cuddle(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to cuddle!!')
        return
    
    cuddle = animec.Waifu.cuddle()
    
    cuddle_embed=discord.Embed(title = 'Cuddle!', description = f'{ctx.author.mention} **Has cuddled {member.mention}!!!**' ,url = cuddle, color = ctx.author.color)
    cuddle_embed.set_image(url = cuddle)
    await ctx.send(embed=cuddle_embed)

@client.command()
async def smug(ctx):
    smug = animec.Waifu.smug()
    
    smug_embed=discord.Embed(title = 'Smug!', url = smug, color = ctx.author.color)
    smug_embed.set_image(url = smug)
    await ctx.send(embed=smug_embed)

@client.command()
async def smile(ctx):
    smile = animec.Waifu.smile()
    
    smile_embed=discord.Embed(title = 'Smile!', description = f"{ctx.author.mention} Smiled!", url = smile, color = ctx.author.color)
    smile_embed.set_image(url = smile)
    smile_embed.set_footer(text = 'How cute <3!')
    await ctx.send(embed=smile_embed)        

@client.command()
async def handhold(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member a member to hold his/her hand!!')
        return
    
    handhold = animec.Waifu.handhold()
    
    handhold_embed=discord.Embed(title = 'Hand Hold!', description = f"{ctx.author.mention} **is holding {member.mention}'s hand!!!**" ,url = handhold, color = ctx.author.color)
    handhold_embed.set_image(url = handhold)
    await ctx.send(embed=handhold_embed)

@client.command()
async def slap(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member so slap!')
        return
    
    slap = animec.Waifu.slap()
    
    slap_embed=discord.Embed(title = 'Slap!', description = f"{ctx.author.mention} **just slapped {member.mention}!!!**" ,url = slap, color = ctx.author.color)
    slap_embed.set_image(url = slap)
    await ctx.send(embed=slap_embed) 

@client.command()
async def glomp(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member so glomp!')
        return
    
    glomp = animec.Waifu.glomp()
    
    glomp_embed=discord.Embed(title = 'Glomp!', description = f"{ctx.author.mention} **just Glomped {member.mention}!!!**" ,url = glomp, color = ctx.author.color)
    glomp_embed.set_image(url = glomp)
    await ctx.send(embed=glomp_embed)

@client.command()
async def bite(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to Bite!')
    
    bite = animec.Waifu.bite()
    
    bite_embed=discord.Embed(title = 'Bite!', description = f'{member.mention} just got bitten by {ctx.author.mention}!!',url = bite, color = ctx.author.color)
    bite_embed.set_image(url = bite)
    await ctx.send(embed=bite_embed)

@client.command()
async def kill(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to kill!!')

    kill = animec.Waifu.kill()

    kill_embed = discord.Embed(title = 'Kill!', description = f"{ctx.author.mention} Killed {member.mention}!!", url = kill, color = ctx.author.color)
    kill_embed.set_image(url = kill)
    await ctx.send(embed= kill_embed)

@client.command()
async def k(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to kick!!')

    kick = animec.Waifu.kick()

    kick_embed = discord.Embed(title = 'Kick!!', description = f"{ctx.author.mention} Just kicked {member.mention}!!", url = kick, color = ctx.author.color)
    kick_embed.set_image(url = kick)
    await ctx.send(embed= kick_embed)                     

@client.command()
async def happy(ctx):
    happy = animec.Waifu.happy()
    
    happy_embed=discord.Embed(title = 'Happy!', description = f"{ctx.author.mention} Is happy!", url = happy, color = ctx.author.color)
    happy_embed.set_image(url = happy)
    happy_embed.set_footer(text = 'How cute <3!')
    await ctx.send(embed=happy_embed)

@client.command()
async def wink(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to wink to!!')

    wink = animec.Waifu.wink()

    wink_embed = discord.Embed(title = 'Wink!!', description = f"{ctx.author.mention} Just Winked to {member.mention}!!", url = wink, color = ctx.author.color)
    wink_embed.set_image(url = wink)
    await ctx.send(embed= wink_embed)

@client.command()
async def poke(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to poke!!')

    poke = animec.Waifu.poke()

    poke_embed = discord.Embed(title = 'Poke!!', description = f"{ctx.author.mention} Just Poked {member.mention}!!", url = poke, color = ctx.author.color)
    poke_embed.set_image(url = poke)
    await ctx.send(embed= poke_embed)         

@client.command()
async def nom(ctx):
    nom = animec.Waifu.nom()
    
    nom_embed=discord.Embed(title = 'NOM NOM!', description = f"{ctx.author.mention} Nom Nom!", url = nom, color = ctx.author.color)
    nom_embed.set_image(url = nom)
    await ctx.send(embed=nom_embed)

@client.command()
async def dance(ctx):
    dance = animec.Waifu.dance()
    
    dance_embed=discord.Embed(title = 'Dance!', description = f"{ctx.author.mention} Is Dancing!", url = dance, color = ctx.author.color)
    dance_embed.set_image(url = dance)
    await ctx.send(embed=dance_embed)

@client.command()
async def yeet(ctx, *, member : discord.Member = None):
    if member == None:
        await ctx.send('Mention a member to yeet!!')

    yeet = animec.Waifu.yeet()

    yeet_embed = discord.Embed(title = 'Yeet!!', description = f"{ctx.author.mention} Just Yeeted {member.mention}!!", url = yeet, color = ctx.author.color)
    yeet_embed.set_image(url = yeet)
    await ctx.send(embed= yeet_embed) 

@client.command(aliases=['8ball','8Ball','8b','8B'])
async def _8ball(ctx,*,question):
    responses = [
        'Hell no.',
        'Propably not.',
        'Idk bro.',
        'Probably.',
        'Hell yeah.',
        'It is certain.',
        'It is decidedly so.',
        'Without a Doubt.',
        'Yes - Definitaly.',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Outlook Good.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't Count on it.",
        'My reply is No.',
        'My sources say No.',
        'Outlook not so good.',
        'Very Doubtful']

    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')


@client.command(aliases=['cf','Cf','Coinflip','COINFLIP'])
async def coinflip(ctx,*,question):
    cf_list = ['Heads','Tails']
    await ctx.send(f'{ctx.author.mention} {random.choice(cf_list)}!')

@client.command(aliases=['Kick','KICK'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member,*, reason = None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('You cant do that, bruh.')
        return

    if reason == None:
        await ctx.send("Write a reason, I don't think they going to be happy if you dont give them the reason")
        return

    else:
        await ctx.send("Idk why but i can't do that okay")       

    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked, reason: {reason}, get rekt bozo :skull:')

    

@client.command(aliases=['Ban','BAN'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member,*,reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You cant do that, bruh.')
        return
    
    if reason == None:
        await ctx.send("Write a reason, I don't think they going to be happy if you dont give them the reason")
        return

    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned, reason: {reason}, get rekt bozo :skull:')

@client.group(invoke_without_command = True)
async def help(ctx):
    help_embed = discord.Embed(title = 'Need some help?', description = 'Use !help <command> for more information about that command. ***(coming soon)***', timestamp = ctx.message.created_at, color = discord.Color.random(), inline = False)

    help_embed.add_field(name = 'Moderation :gear:', value = 'ban, unban, kick, clear, slowmode, mute, unmute', inline = False)
    help_embed.add_field(name = 'Fun :video_game:', value = '8ball, coinflip, howgay, dadjoke, howlesbi, howcute, pp, howpro, meme, meme2, emojify, say, avatar, cat, dog, funfact, randomquestion, rickroll', inline = False)
    help_embed.add_field(name = 'Anime', value = 'bite, character, animenews, anime, dance, cuddle, cry, cool, happy, glomp, kiss, lick, handhold, awoo,bully,kill, k, waifu, neko, nom, pat, poke, slap, smile, smug, wink, yeet, bonk, hug', inline = False)
    help_embed.add_field(name = 'Others', value = 'gcreate, poll, ping, afk, serverinfo, userinfo, botinfo, time, calc', inline = False)
    help_embed.set_footer(text = f'Requested by {ctx.author}')
    help_embed.set_thumbnail(url = client.user.avatar_url) 

    await ctx.send(embed = help_embed)

@help.command()
async def ban(ctx):
    embed = discord.Embed(title="Ban Command", description="**Command syntax: !ban <member mention> <reason>\n \n Use: this command is used to ban members, what did u except**",  timestamp=ctx.message.created_at)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url) 
    
    await ctx.send(embed = embed)

@help.command()
async def unban(ctx):
    embed = discord.Embed(title="unban Command", description="**Command syntax: !unban <member mention> <reason>\n \n Use: this command is used to unban members, what did u except**",  timestamp=ctx.message.created_at)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

    await ctx.send(embed = embed)  

@help.command()
async def slowmode(ctx):
    embed = discord.Embed(title="Slowmode Command", description="**Command syntax: !slowmode <amount>\n \n Use: Haha slowmode**",  timestamp=ctx.message.created_at)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)   

    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You cant do that, bruh.')
        return
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')


@client.command(aliases=['Purge','Clear','purge'])
async def clear(ctx, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        error_embed = discord.Embed(title = ':x:', description = f"{ctx.author.mention} **ur dumb**", timestamp = ctx.message.created_at)
        await ctx.send(embed = error_embed)
        return
    if amount > 1000:
        await ctx.send('Can not delete more than 1000 messages.')
        return

    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages.")

@client.command()
async def slowmode(ctx,time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You cant do that, bruh.')
        return
    try:
        if time == 0:
            await ctx.send(':white_check_mark: Slowmode turned off')
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            await ctx.send(':x: You can not set the slowmode above 6 hours')
            return
        else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(f':white_check_mark: Slowmode has been set to {time} seconds')

    except Exception:
        await print('Oops!')

@client.command()
async def afk(ctx):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} is now AFK.")
    await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")


@client.command()
async def say(ctx, saymsg=None):
    if saymsg == None:
        return await ctx.send('You must tell me something to say, Onii-chan! >-<')
    sayEmbed = discord.Embed(timestamp = ctx.message.created_at,title = f'{ctx.author} Says:', description = f'**{saymsg}**')
    await ctx.send(embed = sayEmbed)


@client.command()
async def serverinfo(ctx):
    embed = discord.Embed(
        color = ctx.guild.owner.top_role.color
    )
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url = str(ctx.guild.icon_url))
    embed.add_field(name = f"Information About **{ctx.guild.name}**: ", value = f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{ctx.guild.region}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
    await ctx.send(embed=embed)

@client.command(aliases=['A','a','Avatar','AVATAR'])
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author
    memberAvatar = member.avatar_url
    avatarEmbed = discord.Embed(timestamp = ctx.message.created_at,title = f"{member.name}'s Cool avatar")
    avatarEmbed.set_image(url = memberAvatar)
    await ctx.send(embed = avatarEmbed)

@client.command(aliases=['giveaway'])
async def gcreate(ctx, time=None, *, prize=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You cant do that, bruh.')
        return
    if time == None:
        return await ctx.send('Please include the time!')
    elif prize == None:
        return await ctx.send('Please include the prize!')

    giveaway_embed = discord.Embed(timestamp = ctx.message.created_at,title = 'New Giveaway!', description=f'{ctx.author.mention} is giving away **{prize}**!!!')
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    giveaway_embed.set_footer(text=f'Giveaway ends in {time}')
    gaw_msg = await ctx.send (embed = giveaway_embed)

    await gaw_msg.add_reaction('🎉')
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f'YAYYYY!!! {winner.mention} has won the giveaway for **{prize}**!!!')


@client.command()
async def userinfo(ctx, *, user: discord.Member = None): 
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

 



@client.command()
async def emojify(ctx,*,text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)

    await ctx.send(''.join(emojis))                

@client.event 
async def on_member_remove(member):
    guild = member.guild
    if guild.system_channel is not None:
        left_embed = discord.Embed(title='Whaaat someone just left?', color=0x9208ea, description=(f'{member.name} Just left the server'))
        left_embed.set_footer(text='BYE BYE')
        await guild.system_channel.send(embed = left_embed)
        


@client.event 
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        joined_embed = discord.Embed(title = 'Whaaat someone just joined?', color=0x9208ea, description=f'{member.name} Just joined the server')
        joined_embed.set_footer(text='Very EPIC!!')
        await guild.system_channel.send(embed = joined_embed)



@client.command()
async def poll(ctx, *, question=None):
    if (not ctx.author.guild_permissions.manage_messages):

        x_embed = discord.Embed(title = ':x:', description = "**You can't do that.**")

        await ctx.send(embed = x_embed)
        return
    if question == None:
        await ctx.send("Write a poll!")
        return
 
    icon_url = ctx.author.avatar_url 
    
    pollEmbed = discord.Embed(title = "Voting Time!", description = f"**{question}**")
    
    pollEmbed.set_footer(text = f"Poll given by {ctx.author}", icon_url = ctx.author.avatar_url)
    
    pollEmbed.timestamp = ctx.message.created_at

    pollEmbed.set_thumbnail(url = icon_url) 
    
    await ctx.message.delete()
    
    poll_msg = await ctx.send(embed = pollEmbed)
    
    await poll_msg.add_reaction("✅")
    await poll_msg.add_reaction("❌")




@client.command()
async def invite(ctx):
    invite_embed = discord.Embed(title = 'Invite Link', description = 'Thats very pog of you :heart:', color = 0x9208ea)
    invite_embed.set_footer(text = 'Requested by {}'.format(ctx.author))
    invite_embed.set_thumbnail(url = client.user.avatar_url)
    invite_embed.url = 'https://discordapp.com/oauth2/authorize?client_id=716098454888126464&permissions=8&scope=bot'
    await ctx.send(embed = invite_embed)



@help.command()
async def kick(ctx):
    embed = discord.Embed(title="Kick Command", description="**Command syntax: !kick <member mention> <reason>\n \n Use: this command is used to kick members, what did u except**",  timestamp=ctx.message.created_at)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)   

    await ctx.send(embed = embed)
       

           
@client.command()
async def calc(ctx, *, equation):
        try:
            result = eval(equation)
            embed = discord.Embed(title=f'Calculator', color=ctx.author.color)
            embed.add_field(name='Equation', value=equation, inline=False)
            embed.add_field(name='Result', value=result, inline=False)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        except:
            await ctx.send('Invalid equation!')

@client.command()
async def randomquestion(ctx):
    question = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
    embed = discord.Embed(title=f'Question', color=ctx.author.color)
    embed.add_field(name='Question', value=question.json()['results'][0]['question'], inline=False)
    embed.add_field(name='Answer', value=question.json()['results'][0]['correct_answer'], inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def dog(ctx):
    dog = requests.get('https://dog.ceo/api/breeds/image/random')
    embed = discord.Embed(title=f'Dog', color=ctx.author.color)
    embed.set_image(url=dog.json()['message'])
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def cat(ctx):
    cat = requests.get('https://aws.random.cat/meow')
    embed = discord.Embed(title=f'Cat', color=ctx.author.color)
    embed.set_image(url=cat.json()['file'])
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
                      

@client.command()
async def meme2(ctx):
    meme = requests.get('https://meme-api.herokuapp.com/gimme')
    embed = discord.Embed(title=f'Meme', color=ctx.author.color)
    embed.set_image(url=meme.json()['url'])
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def funfact(ctx):
    fact = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    embed = discord.Embed(title=f'Fact', color=ctx.author.color)
    embed.add_field(name='Fact', value=fact.json()['text'], inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)    
        
@client.command()
async def dadjoke(ctx):
    joke = requests.get('https://icanhazdadjoke.com/', headers={"Accept":"application/json"})
    embed = discord.Embed(title=f'Joke', color=ctx.author.color)
    embed.add_field(name='Joke', value=joke.json()['joke'], inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def mute(ctx, user: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.mute_members:
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await user.add_roles(role)
        await ctx.send(f'{user} has been muted!')
    else:
        await ctx.send('You do not have permission to mute members!')

@client.command()
async def unmute(ctx, user: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.mute_members:
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await user.remove_roles(role)
        await ctx.send(f'{user} has been unmuted!')
    else:
        await ctx.send('You do not have permission to unmute members!')


@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title=f'{client.user.name}', color=ctx.author.color)
    embed.add_field(name='**Prefix:exclamation:**', value='!')
    embed.add_field(name='**Servers:desktop:**', value=len(client.guilds), inline=False)
    embed.add_field(name='**Users**', value=len(client.users), inline=False)
    embed.add_field(name='**Ping:ping_pong:**', value=round(client.latency * 1000), inline=False)
    embed.add_field(name = '**Invite**', value = 'https://discordapp.com/api/oauth2/authorize?client_id=723990989841003520&permissions=8&scope=bot', inline = False)
    embed.add_field(name = '**Lines of code:technologist:**', value = '1093!', inline = False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)                    




       
 

@client.command()
async def thing(ctx):
    await ctx.send('Nothing')

client.run(TOKEN)
