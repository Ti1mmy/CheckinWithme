#!/usr/bin/env python3
import discord
from discord.ext import commands, tasks
import datetime
from pytz import timezone
import json
from mood import tone_result

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
        await ctx.send(tone)
    else:
        await ctx.send("Sorry! I couldn't exactly pinpoint your mood. Rate how you feel from a scale of 1-10 (using the >rate command).")

    # do something about mood    


@bot.command(pass_context=True)
async def rate(ctx,*,message):
    rating = tone_result(message)
    # save_result(rating)

    # do something about mood


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

"""@bot.command()
async def motivation(ctx):
    motivational_message = []   """


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
   
    for channel in announcement_channels_list:
        print(channel)
        await channel.send("This announcement was scheduled to send every 10 seconds")

checkin_announcement.start()
bot.run(token)