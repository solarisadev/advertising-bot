import discord
from discord.ext import commands
from colorama import Fore
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

with open('data.json' , 'r') as f:
    config = json.load(f)
token = config['bot_token']
title = config['title']
field_value = config["field_value"]
field_name = config["field_name"]
icon_url = config["icon_url"]
with open('embed_description' , 'r') as f:
    description = f.read()

@bot.event
async def on_ready():
    print(Fore.LIGHTGREEN_EX + f"Logged in as {bot.user.name}")

bot.remove_command('help')
print(Fore.BLUE + "")

@bot.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
    embed = discord.Embed(title="" , description = '''## List Of All Commands
**!embed\n`See Embed Message`
!normal_dm <@user> mmessage\n`Dm Targeted User With Message`
!massdmall message\n`Dm All Server Members With Message`
!embed_dm \n`Dm Targeted User With Embed Message`
!embed_dm_all\n`Dm All Server Members With Embed Message`**''' , color=discord.Color.yellow())
    embed.add_field(name="How To Create Embed ?" , value="You Can Edit Config With Title/Field info / icon url And You Can Drop Your Message In embed_description File")
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    if ctx.author.avatar:
        embed.set_footer(icon_url=ctx.author.avatar.url , text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)


async def embed_creater(ctx):
    embed = discord.Embed(
    title="Embed Creator",
    description=description,
    color=discord.Color.blurple()
)
    if field_name and field_value:
        embed.add_field(name=field_name,value=field_value,inline=False)
    embed.set_thumbnail(url=icon_url)
    return embed

@bot.command()
@commands.has_permissions(administrator=True)
async def embed(ctx):
    embed = await embed_creater(ctx)
    await ctx.send("Here Is The Embed You Can Set Custom Title / Description / Etc By YourSelf" ,embed=embed)
    print(Fore.LIGHTMAGENTA_EX + f"{ctx.author.name} Used Command Embed")


@bot.command()
@commands.has_permissions(administrator=True)
async def embed_dm(ctx , member:discord.Member):
    embed = await embed_creater(ctx)
    try:
        await member.send(embed=embed,view=HelpView())
        print(Fore.BLUE + f"Your message was sent to {member.name}")
    except Exception as e:
        print(f"There was an error sending a message to {member.name}")
    
@bot.command()
@commands.has_permissions(administrator=True)
async def embed_dm_all(ctx):
    embed = await embed_creater(ctx)
    for xD in ctx.guild.members:
        try:
            await xD.send(embed=embed,view=HelpView())
            print(Fore.LIGHTBLUE_EX + f'Your message was sent to {xD.name}')
        except Exception as e:
            print(Fore.RED + f"There was an error sending a message to {xD.name}")
    
@bot.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(administrator=True)
async def massdmall(ctx , * , message):
    for xD in ctx.guild.members:
        try:
            await xD.send(message)
        except Exception as e:
            print(Fore.RED + f"There was an error sending a message to {xD.name}")
    
@bot.command()
@commands.has_permissions(administrator=True)
async def normal_dm(ctx , member:discord.Member ,* , message):
    try:
        await member.send(message)
        print(Fore.BLUE + f"Your message was sent to {member.name}")
    except Exception as e:
        print(f"There was an error sending a message to {member.name}")
    
bot.run(token)
