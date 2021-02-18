import asyncio
import datetime
import shutil
import os
import traceback
import ctypes
import discord
from discord.ext import commands

#Embed color values
pingPongRed = 0xC00003
errorRed = 0xff0000
unloadedOrange = 0xf0410f
loadedGreen = 0x00ff00
mixedBlue = 0x0a55c8
bloodshotRed = 0xb10010

#set title of console.
#ctypes.windll.kernel32.SetConsoleTitleW("Sentinel Bot | Bot API Version: 1.0.0")

#Setting boot time.
timeBoot = datetime.datetime.now().strftime("%H:%M %m-%d-%Y")

bot = commands.Bot(command_prefix='>',
                      description='Assisting the users!',
                      owner_id=416043861950070784,
                      case_insensitive=True)
bot.remove_command('help')

debugMode = False

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for >"))
    print(f'[INFO]: Logged in as {bot.user.name} | ID: {bot.user.id}')
    print(f'[INFO]: {bot.user.name} online and booted as of {timeBoot}.')
    print('-'*60)


@bot.event
async def on_command_error(ctx, error):
    """Error Handler"""

    #This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.UserInputError)

    #Allows us to check for original exceptions raised and sent to CommandInvokeError.
    #If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    #Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.', delete_after=10)

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except:
            return await ctx.author.send('exception error')

    #For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            return await ctx.send('I could not find that member. Please try again.', delete_after=10)

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.message.content)
        embed = discord.Embed(title='**Missing Required Argument**', color=errorRed)
        await ctx.send(embed=embed, delete_after=10)

    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        embed = discord.Embed(title=f'**Slow down! \n`{ctx.command}` is currently on cooldown!**', color=errorRed)
        return await ctx.send(embed=embed, delete_after=10)

    #if isinstance(error, commands.CommandNotFound):
        #embed = discord.Embed(title=f'**Uh-Oh \n I could not issue that command. Was it spelled correctly? **', color=errorRed)
        #return await ctx.send(embed=embed)
    #All other Errors not returned come here... And we can just print the default TraceBack.
    else:
        if debugMode == True:
            print('[ERROR]: Ignoring exception in command {}:'.format(ctx.command))
            traceback.print_exception(type(error), error, error.__traceback__)
        else:
            print("[ERROR]: An unexpected error has occured!")

    if isinstance(error, AttributeError):
        return

#End Error Handler and startup variable initialization
#Begin Cog Loading and clean up previous downloads:
#Used for Automatic load of modules on startup
print("[INFO]: Attempting to wipe Radio cache...")
try:
    shutil.rmtree('./downloads')
    print("[INFO]: Radio cache wiped successfully!")
except:
    print("[WARN]: Radio cache was not present, continuing...")

print("[INFO]: Initializing cogs...")
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'[INFO]: {filename[:-3]} initialized successfully!')

#restricts load permissions to everyone other than administrators.
@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    """ can only be used by an admin! """
    await ctx.channel.purge(limit=1)
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} Loaded!', delete_after=10)
    print(f'[INFO]: {extension} Loaded!')


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    """ can only be used by an admin! """
    await ctx.channel.purge(limit=1)
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} Unloaded!', delete_after=10)
    print(f'[INFO]: {extension} Unloaded!')


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    """ can only be used by an admin! """
    await ctx.channel.purge(limit=1)
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} Reloaded!', delete_after=10)
    print(f'[INFO]: {extension} Reloaded!')
#Essential functionality has loaded by this point excluding login to discord's api using the token.

#Base commands.
@bot.command()
async def Version(ctx):
    embed = discord.Embed(title=f'Hello **{ctx.author}!**\n I am currently in production release phase. The current build string is: (1.0.0)', color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member : discord.Member = None, * , text : str = ""):
    '''DMs a user'''
    await ctx.channel.purge(limit=1)
    await member.send(f"{text}")


bot.run(os.environ['DISCORD_TOKEN'], reconnect=True)
#bot.run(devToken, reconnect=True)
