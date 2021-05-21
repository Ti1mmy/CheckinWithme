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
    with open('config/config.json') as config_file:
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
        embed = discord.Embed(title="Oops!", description="Sorry! I couldn't quite pinpoint how you are feeling. Feel free to send me another message and I'll try to figure out how you are feeling!", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(6, 81, 37))
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
        embed = discord.Embed(title="Oops!", description="Sorry! I couldn't quite pinpoint how you are feeling. Feel free to send me another message and I'll try to figure out how you are feeling!", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(13, 151, 172))
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
    embed = discord.Embed(title="List of Commands", description="To use these commands, type '>' with the corresponding command.", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(226, 83, 47))
    embed.add_field(name="checkin", value="""Let me know how you're feeling with the 'checkin' command!\nFor instance, you could type `>checkin I'm feeling pretty happy today` or any other feelings you have. 
    Your mood will then be categorized into one of four categories (anger, fear, joy, and sadness) and will be compiled in a weekly summary for you to view at anytime.""")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="rate", value="""You can also let me know how you are feeling with the 'rate' command! Please include one of the following: | Anger | Fear | Joy | Sadness | with the command.
    This provides a more direct and accurate method for our systems to track your mood.""")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="motivation", value="Sends motivational messages to cheer you on to bigger and better.")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="resource", value="Generates a random resource to help you develop your mental health!")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    await ctx.send(embed=embed)


@bot.command()
async def motivation(ctx):
    motivation_url = get_motivation()
    await ctx.send(motivation_url)


@bot.command()
async def resource(ctx):
    resources = [
        "https://www.mindful.org/",
        "https://www.youtube.com/watch?v=inpok4MKVLM",
        "https://gratefulness.org/",
        "https://www.helpguide.org/articles/healthy-living/the-mental-health-benefits-of-exercise.htm",
        "https://www.youtube.com/c/HealthyGamerGG/videos"
    ]
    resource = random.choice(resources)
    embed = discord.Embed(title="Random Resource", description=resource, timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(226, 83, 47))
    await ctx.send(embed=embed)


# Events

@bot.event
async def on_guild_join(guild):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True),
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(send_messages=True),
    }
    await guild.create_text_channel('daily-check-in', overwrites=overwrites)   
    update_announcement_list()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Let's check in! | prefix: >"), status="online")
    global bot_tag
    bot_tag = bot.user
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


@bot.listen()
async def on_message(message):
    content = message.content
    try:
        if content == ">dm" and not message.author.bot:
            message.author.send("response")
    except TypeError:
        return None

# Tasks


@tasks.loop(seconds=10)
async def checkin_announcement():
    day_of_week = datetime.datetime.today().weekday() #returns a number from 0 to 6
    daily_motivation = [
        "Hey, I know it's Monday. But it's also a new day and a new week. And in that lies a new opportunity for something special to happen.",
        "Tuesday isn't so bad... It's a sign that I've somehow survived Monday.",
        "Wednesday is like small friday; half way to the weekend.",
        "Thankful Thursday, it's not happy people who are thankful. It's thankful people who are happy. Always look on the bright side of life",
        "TGIF!", #can add later probably
        "Happy Saturday.",
        "Sunday: A day to refuel your soul and be grateful for your blessings. Take a deep breath and realx. Enjoy your family, your friends and a cup of coffee."
    ]
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for channel in announcement_channels_list:
        embed = discord.Embed(title=f"⭐Happy {days_of_the_week[day_of_week]}!⭐", description="Yesterday is history. Tomorrow is a mystery, but today is a gift! That is why it is called the present.", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(221, 160, 51))
        embed.add_field(name="Check in With Me!", value=f"{bot_tag.mention}")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Daily Motivation", value=daily_motivation[day_of_week])
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
        await channel.send(embed=embed)


checkin_announcement.start()
bot.run(token)