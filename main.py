import discord 
from discord.ext import commands 
import json 

config = json.load(open("config.json", encoding="utf-8"))
client = commands.Bot(command_prefix=config["prefix"], description="Hwid Discord Bot!", help_command=None)
hwids = open("Auth/hwids.txt")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%shelp | Auth Bot' % config["prefix"]))

@client.command()
async def hwid(ctx, message):
    if ctx.author.id == int(config["ownerid"]):
        await ctx.send("Adding User To The Auth")
        if(message in hwids.read()):
            await ctx.send("Cannot Add User To Auth! User Already Authed!")
        else:
            with open("Auth/hwids.txt", "a") as f:
                f.write(f"{message}\n")
                f.close()
            await ctx.send("User Now Authed!")
    if ctx.author.id != int(config["ownerid"]):
        await ctx.send("Only <@%s> Can Auth Members!" % config["ownerid"])

@client.command()
async def checkuser(ctx, message):
    if(message in hwids.read()):
        await ctx.send("This User Is Already Authed!")
    else:
        await ctx.send("This User Is Not Authed!")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Command!", description="%shelp - Can Be Used By Anyone, Returns This Message\n%shwid - Can Only Be Used By Owner, Adds User To Auth\n%scheckuser - Can Be Used By Anyone, Checks Hwid To See If Its Authed!" % (config["prefix"], config["prefix"], config["prefix"]))
    await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(config["token"])
