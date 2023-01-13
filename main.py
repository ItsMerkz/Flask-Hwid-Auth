import discord 
from discord.ext import commands 
import json 
import asyncio
import requests 

intents = discord.Intents.default()
intents.message_content = True

config = json.load(open("config.json", encoding="utf-8"))
client = commands.Bot(command_prefix=config["Discord"]["prefix"], description="Hwid Discord Bot!", help_command=None, intents=intents)
hwids = open("Auth/hwids.txt")

liness = [line.strip("\n") for line in hwids if line != "\n"]
amount = len(liness)

class Utils:
    def __init__(self):
        from main import Utils 
    
    @staticmethod
    def checkifowner(id: int):
        if id in config["Discord"]["owner_ids"]:
            return True 
        else:
            return False

@client.event
async def on_ready():
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%shelp | Auth Bot!' % config["Discord"]["prefix"]))
        await asyncio.sleep(0.5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%shelp | Authed %s Users!' % (config["Discord"]["prefix"], amount)))

@client.command()
async def hwid(ctx, message):
    if Utils().checkifowner(ctx.author.id):
        await ctx.send("Adding User To The Auth")
        if(message in hwids.read()):
            await ctx.send("Cannot Add User To Auth! User Already Authed!")
        else:
            with open("Auth/hwids.txt", "a") as f:
                f.write(f"{message}\n")
                f.close()
            await ctx.send("User Now Authed!")
    if Utils().checkifowner(ctx.author.id) != True:
        await ctx.send("Only <@%s> Can Auth Users!" % config["Discord"]["owner_ids"])
        

@client.command()
async def checkuser(ctx, message):
    if(message in hwids.read()):
        await ctx.send("This User Is Already Authed!")
    else:
        await ctx.send("This User Is Not Authed!")

@client.command()
async def remove(ctx, message):
    if Utils().checkifowner(ctx.author.id):
        lines = open("Auth/hwids.txt").read().splitlines()
        for i in range(len(lines)):
            l = lines[i]
            if l == message:
                lines.pop(i)
        open("Auth/hwids.txt", "w").write("") # remove all lines
        for line in lines:
            open("Auth/removed.txt", "a").write(message + "\n")
        await ctx.send("Removed User %*&$! Sucessfully!")
    if Utils().checkifowner(ctx.author.id) != True:
        await ctx.send("Only <@%s> Can Remove Users!" % config["Discord"]["owner_ids"])

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Command!", description="**%shelp** - Can Be Used By Anyone, Returns This Message\n**%shwid** - Can Only Be Used By Owner, Adds User To Auth\n**%scheckuser** - Can Be Used By Anyone, Checks Hwid To See If Its Authed!\n**%sremove** - Can Only Be Used By Owner, Removes A Hwid From Auth!\n**%sstatus** - Can Be Used By Anyone, Checks If Server Is Online And Informs You Of It's Status!" % (config["Discord"]["prefix"], config["Discord"]["prefix"], config["Discord"]["prefix"], config["Discord"]["prefix"], config["Discord"]["prefix"]))
    await ctx.send(embed=embed)

@client.command()
async def status(ctx):
    response = requests.get("%s/status" % (config["Server"]["Url"]))
    if response.text == "Auth Is Online!":
        await ctx.send("Server Is Online")
    else:
        await ctx.send("Server is currently offline or experiencing technical difficulties")

@client.command()
async def owners(ctx):
    await ctx.send("%s" % (config["Discord"]["owner_ids"]))

if __name__ == '__main__':
    client.run(config["Discord"]["token"])
