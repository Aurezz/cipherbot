'''
MIT License
Copyright (c) 2017 Free TNT , Aurezz
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
import sys
import os
import io
from discord.ext import commands
import traceback
import textwrap
from contextlib import redirect_stdout

bot = commands.Bot(command_prefix='c!', description="A multipurpose bot by Aurez and Free TNT#5796")
bot.remove_command("help")

devs = [
    133867153890869248,
    292690616285134850,
    323242528566673408
]

@bot.event
async def on_ready():
  print("Bot is on.")
  bot._last_result = None
  guilds = len(bot.guilds)
  print(guilds)

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')
  
  
  
  
@bot.command()
async def help(ctx):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title = "Cipher Commands: "
  embd.description = "A discord bot being made with love! Join support server [here](https://discord.gg/N25KSSY)"
  embd.add_field(name="Bot: ", value=f"`c!invite | Invite Cipher to your server!.`\n"
                                    f"`c!ping | Pong!`\n"
                                    f"`c!embedsay | Bot repeats message in embed form!`")
  embd.add_field(name="Mod: ", value=f"`c!kick | Kick user outta server`\n"
                                    f"`c!ban | Ban user from the server`\n"
                                    f"`c!warn | Warn user`")
  embd.add_field(name="Calculator: ", value=f"`c!add | Add numbers!`\n"
                                            f"`c!subtract | Subtract numbers!`\n"
                                            f"`c!divide | Divide numbers!`\n"
                                            f"`c!getremainder | Get remainder!`")
  embd.set_footer(text="CipherBot Commands!")
  embd.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png") 
  await ctx.send(embed=embd)                                   
                                    
  




@bot.command()
async def ping(ctx):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title = "Ping"
  embd.description = "Pong!"
  await ctx.send(embed=embd)
    


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member):
    try:
        await user.kick()
        await ctx.send(f"I have kicked **{user}** out of the server!")
    except discord.Forbidden:
        await ctx.send("Either **me** or **you** do not have enough permissions to kick user!")
    
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.Member):
    try:
        await user.ban()
        await ctx.send(f"I have banned **{user}** from the server!")
    except discord.Forbidden:
        await ctx.send("Either **me** or **you** do not have enough permissions to ban user!")
    

@bot.command()
@commands.has_permissions(ban_members = True)
async def warn(ctx, user: discord.Member, *, reason: str):
    warning = f"You've been warned in **{ctx.author.guild}** by **{ctx.message.author}**\n**Reason:** {reason}"
    await user.send(warning)
    await ctx.send(f"**{user}** has been warned")
    
    
  
    
@bot.command()
async def embedsay(ctx, *, words: str):
    embd = discord.Embed(color=discord.Color(value=0x0086b3))
    embd.description = words
    await ctx.send(embed=embd)
    await ctx.message.delete()
    
@bot.command()
async def invite(ctx):
    emoji = bot.get_emoji(386596923332624384)
    embd = discord.Embed(color=discord.Color(value=0x0086b3))
    embd.title = (f"Invite Cipherbot {emoji}")
    embd.description = "Click [here](https://discordapp.com/api/oauth2/authorize?client_id=385787711203704832&scope=bot&permissions=1) to invite **CipherBot!**"
    await ctx.send(embed=embd)

    
"""Calculator commands"""

@bot.command()
async def add(ctx, a:int, opr: str ,b:int):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title= "Add"
  embd.description = f'Your answer is: **{a+b}**'
  await ctx.send(embed=embd)

  
@bot.command()
async def subtract(ctx, a:int, opr:str ,b:int):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title= "Subtract"
  embd.description = f'Your answer is: **{a-b}**'
  await ctx.send(embed=embd)
  
  
@bot.command()
async def divide(ctx, a:int, opr:str ,b:int):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title= "Divide"
  embd.description = f'Your answer is: **{a/b}**'
  await ctx.send(embed=embd)
  
@bot.command()
async def multiply(ctx, a:int, opr:str ,b:int):
  await ctx.send(a*b)

  
@bot.command()
async def getremainder(ctx, a:int, opr:str ,b:int):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.title= "Getremainder"
  embd.description = f'Your answer is: **{a%b}**'
  await ctx.send(embed=embd)
    
    
    
    
    
    
@bot.command(pass_context=True, hidden=True, name='eval')
async def _eval(ctx, *, body: str):
        """Evaluates a code"""
        if ctx.author.id not in devs: return
        
        env = {
                'bot': bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': bot._last_result
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                bot._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


bot.run(os.environ.get("TOKEN"))
