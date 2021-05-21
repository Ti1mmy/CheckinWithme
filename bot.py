#!/usr/bin/env python3
import discord
from discord.ext import commands, tasks
import datetime
from pytz import timezone
import json
from mood import tone_result
import random
from motivation import get_motivation
from connect_database import update_mood

TEST = True

announcement_channels_list = []

try:
    #  conf = json.load(open("config.json"))
    with open('config.json') as config_file:
        conf = json.load(config_file)
    if conf['token'] is None:
        raise Exception
    token = conf['token']
    if TEST:
        token = conf['token_test']


except Exception:
    print("Failed to open config, check it exists and is valid.")

bot = commands.Bot(command_prefix='>', description="CheckinWithMe")


dmfailed = discord.Embed(
    title="DM Failed",
    description='',
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.from_rgb(240, 71, 71)
)


# Static

def update_announcement_list():
    global announcement_channels_list
    announcement_channels_list = []
    for guild in bot.guilds:
        print(guild)
        for channel in guild.channels:
            print(channel)
            print(channel.type)
            print(type(channel.type))
            if str(channel.type) == 'text':
                print(channel)
                if str(channel.name) == "daily-check-in":
                    announcement_channels_list.append(channel)
    print(announcement_channels_list)   


# Commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def pingdm(ctx):
    try:
        await ctx.author.send('pong')
    except discord.Forbidden:
        await ctx.send(embed=dmfailed)


@bot.command(pass_context=True)
async def checkin(ctx,*,message):
    tone = tone_result(message)
    # save_result(tone)
    if tone:
        my_tone = tone['tone_id']
        update_mood(ctx.message.author.id, my_tone)
        await ctx.send(tone)
    else:
        embed = discord.Embed(title="Oops!", description="Sorry! I couldn't quite pinpoint how you are feeling. Feel free to send me another message and I'll try to figure out how you are feeling!", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(0, 128, 128))
        embed.add_field(name=">rate", value="You can also let me know how you are feeling with >rate!")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Usage:", value="`>rate <Anger | Fear | Joy | Sadness>`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Example", value="If I'm feeling happy, I would `>rate Joy` 😊")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
        await ctx.send(embed=embed)

    # do something about mood    


@bot.command(pass_context=True)
async def rate(ctx,*,message):
    rating = message.strip().lower()
    if rating in ["anger", "fear", 'joy', 'sadness']:
        tone = tone_result(rating)
        my_tone = tone['tone_id']
        update_mood(ctx.message.author.id, my_tone)
        await ctx.send(tone)
    else:
        embed = discord.Embed(title="Oops!", description="Sorry! I couldn't quite pinpoint how you are feeling. Feel free to send me another message and I'll try to figure out how you are feeling!", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(0, 128, 128))
        embed.add_field(name="Usage:", value="`>rate <Anger | Fear | Joy | Sadness>`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Example", value="If I'm feeling happy, I would `>rate Joy` 😊")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
        await ctx.send(embed=embed)
    # save_result(rating)
    
    # do something about mood


@bot.command(pass_context=True) # Shows the list of commands the user can use
async def commands(ctx):
    
    embed = discord.Embed(title="List of Commands", description="To use these commands, type '>' with the corresponding command.", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(0, 128, 128))
    embed.add_field(name=">rate", value="You can also let me know how you are feeling with >rate!")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Usage:", value="`>rate <Anger | Fear | Joy | Sadness>`")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Example", value="If I'm feeling happy, I would `>rate Joy` 😊")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    await ctx.send(embed=embed)


@bot.command()
async def motivation(ctx):
    motivation_url = get_motivation()
    await ctx.send(motivation_url)

    #  motivational_messages = ["You're cool!"]   #add more later
    #  await ctx.send(random.choice(motivational_messages))

# Events

@bot.event
async def on_guild_join(guild):
    await guild.create_text_channel('daily-check-in')   
    update_announcement_list()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Listening for your feelings | prefix: >'), status="online")
    update_announcement_list()

    print('Bot Initialized')




@bot.listen()
async def on_message(message):
    message_content = message.content
    try:
        if message_content == "Hello" and not message.author.bot:
            await message.channel.send("Hello")    
    except TypeError:
        return None


# Tasks

@tasks.loop(seconds=30)
async def checkin_announcement():
    day_of_week = datetime.datetime.today().weekday()
    for channel in announcement_channels_list:
        embed = discord.Embed(title=f"⭐Happy {day_of_week}!⭐", description="", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(255, 223, 0))
        embed.add_field(name="Usage:", value="`>rate <Anger | Fear | Joy | Sadness>`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Example", value="If I'm feeling happy, I would `>rate Joy` 😊")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
        await ctx.send(embed=embed)

checkin_announcement.start()
bot.run(token)