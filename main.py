import discord 
from discord.ext import commands 
import json 
import asyncio

config = json.load(open("config.json", encoding="utf-8"))
client = commands.Bot(command_prefix=config["prefix"], description="Hwid Discord Bot!", help_command=None)
hwids = open("Auth/hwids.txt")

liness = [line.strip("\n") for line in hwids if line != "\n"]
amount = len(liness)

@client.event
async def on_ready():
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%shelp | Auth Bot!' % config["prefix"]))
        await asyncio.sleep(0.5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%shelp | Authed %s Users!' % (config["prefix"], amount)))

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
        await ctx.send("Only <@%s> Can Auth Users!" % config["ownerid"])

@client.command()
async def checkuser(ctx, message):
    if(message in hwids.read()):
        await ctx.send("This User Is Already Authed!")
    else:
        await ctx.send("This User Is Not Authed!")

@client.command()
async def remove(ctx, message):
    if ctx.author.id == int(config["ownerid"]) and (message in hwids.read()):
        lines = open("Auth/hwids.txt").read().splitlines()
        for i in range(len(lines)):
            l = lines[i]
            if l == message:
                lines.pop(i)
        open("Auth/hwids.txt", "w").write("") # remove all lines
        for line in lines:
            open("Auth/removed.txt", "a").write(line + "\n")
        await ctx.send("Removed User %s Sucessfully!" % message)
    else:
        await ctx.send("Only <@%s> Can Remove Users!" % config["ownerid"])

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Command!", description="**%shelp** - Can Be Used By Anyone, Returns This Message\n**%shwid** - Can Only Be Used By Owner, Adds User To Auth\n**%scheckuser** - Can Be Used By Anyone, Checks Hwid To See If Its Authed!\n**%sremove** - Can Only Be Used By Owner, Removes A Hwid From Auth!" % (config["prefix"], config["prefix"], config["prefix"], config["prefix"]))
    await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(config["token"])
