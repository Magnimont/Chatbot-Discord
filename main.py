=import discord
from discord.ext import commands
import json
import aiohttp
import os
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='*', intents = discord.Intents.all(), case_insensitive=True)


# Add coloring to logs:
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'


# ----------- INITIALIZE BOT ---------- #

# Commands to be run on boot:
@bot.event
async def on_ready():
    # Booting info:
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKGREEN + bcolors.BOLD + "Successful Login! " + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + "Logged in as: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_username}".format(
            bot_username=bot.user.name) + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + "Bot ID: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_user_id}".format(
            bot_user_id=bot.user.id) + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO] Bot Made By" + bcolors.ENDC + bcolors.OKGREEN + bcolors.BOLD + " Saizuo and Albert " + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKGREEN + bcolors.BOLD + "Successful Login! " + bcolors.ENDC)
    # Set bot's status
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name="Ping me with a message to talk to me!"))
    print(bcolors.FAIL + "[INFO]: " + bcolors.ENDC + bcolors.OKBLUE + "Copyright NoError Studios™" + bcolors.ENDC)
    print('----------------------------------------------------------------------')  # Just a hyphen seperator


CHAT_BID = os.environ['BrainID']
CHAT_API_KEY = os.environ['APIKEY']
BASE_URL = f"http://api.brainshop.ai/get?bid={CHAT_BID}&key={CHAT_API_KEY}"

@bot.command(help="Chat with me! >~<")
@commands.cooldown(3, 8, commands.BucketType.user)
async def chat(ctx: commands.Context, *, message: str = None):
        
        async with ctx.channel.typing():
            if message is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(
                    f"Hello! In order to chat with me use: `{ctx.clean_prefix}chat <message>`"
                )
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}&uid={ctx.author.id}&msg={discord.utils.escape_mentions(message)}") as r:
                    if r.status != 200:
                        return await ctx.reply("An error occured while accessing the chat API!")
                    j = await r.json()
                    await ctx.reply(j['cnt'], mention_author=True)
@bot.command()
@commands.has_permissions(manage_guild = True)
async def setup(ctx, *, channel: discord.TextChannel):
    try:
        with open('channels.json') as f:
            channels = json.load(f)
        if channel.id in channels:
            embed = discord.Embed(title="Bruh", description="This channel is already setup", color=discord.Color.red())
            embed.set_footer(text= "Copyright NoError Studios™")
            embed.set_thumbnail(url=bot.user.avatar_url)
            await ctx.reply(embed=embed)
        else:
          channels.append(channel.id)
          with open('channels.json', 'w') as f:
              json.dump(channels, f, indent = 4)
          embed = discord.Embed(title = "Setup Successful", description = f"Channel {channel.mention} has been added to the setup", color = discord.Color.green())
          embed.set_footer(text= "Copyright NoError Studios™")
          embed.set_thumbnail(url=bot.user.avatar_url)
          await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(title = "Setup Failed", description = f"Channel not found or a random error occured.", color = discord.Color.red())
        embed.set_footer(text= "Copyright NoError Studios™")
        embed.set_thumbnail(url=bot.user.avatar_url)
        await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(manage_guild = True)
async def remove(ctx, *, channel: discord.TextChannel):
    try:
        with open('channels.json') as f:
            channels = json.load(f)
        if channel.id in channels:
            channels.remove(channel.id)
            with open('channels.json', 'w') as f:
                json.dump(channels, f, indent = 4)
            embed = discord.Embed(title = "Removed Successfully", description = f"Channel {channel.mention} has been removed from the setup", color = discord.Color.green())
            embed.set_footer(text= "Copyright NoError Studios™")
            embed.set_thumbnail(url=bot.user.avatar_url)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title = "Remove Failed", description = f"Channel not found or a random error occured.", color = discord.Color.red())
            embed.set_footer(text= "Copyright NoError Studios™")
            embed.set_thumbnail(url=bot.user.avatar_url)
            await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(title = "Remove Failed", description = f"Channel not found or a random error occured.", color = discord.Color.red())
        embed.set_footer(text= "Copyright NoError Studios™")
        embed.set_thumbnail(url=bot.user.avatar_url)
        await ctx.reply(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    with open('channels.json') as f:
        channels = json.load(f)
    if message.channel.id in channels:
        if message.channel.slowmode_delay < 5:
            try:
                await message.channel.edit(slowmode_delay=5)
            except Exception:
                bucket_pain = bot.cb_spam_prevention.get_bucket(message)
                retry_after = bucket_pain.update_rate_limit()
                if not retry_after:
                    await message.channel.send("This channel needs to have slowmode of atleast **5 seconds** for chatbot to work!")
                return
        if message.author.id != bot.user.id and not message.author.bot:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}&uid={message.author.id}&msg={message.content}") as r:
                    if r.status != 200:
                        return await message.reply("An error occured while accessing the chat API!")
                    j = await r.json()
                    message.channel.typing()
                    await message.reply(j['cnt'], mention_author=True)
                
    else:
        await bot.process_commands(message)

keep_alive()
bot.run(os.environ['TOKEN'])
