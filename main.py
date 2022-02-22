import os
import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.presences = True
rage = commands.Bot(
	command_prefix="",  # Change to desired prefix
	case_insensitive=True,
  intents=intents  # Commands aren't case-sensitive
)



rage.author_id = 472100676407656448  # Change to your discord id!!!

@rage.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(rage.user)
    guilds = len(rage.guilds)
    users = len(rage.users)
    #please dont do anything in on_ready ....
    game = discord.Game(f" I'm protecting {guilds} guilds| watching {users} users")
    await rage.change_presence(status=discord.Status, activity=game)
      # Prints the bot's username and identifier
    while True:
      await asyncio.sleep(8)
      with open("spam_detect.txt", "r+") as file:
        file.truncate(0)

@rage.event
async def on_message(message):
  counter = 0
  with open("spam_detect.txt", "r+") as file:
    for lines in file:
      if lines.strip("\n") == str(message.author.id):
        counter+=1
    
    file.writelines(f"{str(message.author.id)}\n")
    if counter > 5:
      await message.guild.ban(message.author, reason="spam")
      await asyncio.sleep(1)
      await message.guild.unban(message.author)
      print("uh oh")





@rage.command()
async def ping(ctx):
  await ctx.send("pong")


@rage.command()
async def serverlist(ctx):
    """List the servers that the bot is active on."""
    x = ', '.join([str(server) for server in rage.guilds])
    y = len(rage.guilds)
    print("Server list: " + x)
    if y > 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description=config.err_mesg_generic + "```json\nCan't display more than 40 servers!```", colour=0xFFFFF)
        return await ctx.send(embed=embed)
    elif y < 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description="```json\n" + x + "```", colour=0xFFFFF)
        return await ctx.send(embed=embed)


@rage.command()
async def invite(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=902217465583501412&permissions=8&scope=bot")



@rage.command()
@commands.is_owner()
async def leave(ctx, guild_id):
    await rage.get_guild(int(guild_id)).leave()
    await ctx.send(f"I left: {guild_id}")



keep_alive()
 # Starts a webserver to be pinged.
token = os.environ.get("rage") 
rage.run(token)  # Starts the bot
