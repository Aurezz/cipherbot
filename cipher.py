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
    292690616285134850
]

@bot.event
async def on_ready():
  print("Bot is on.")
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
                                    f"`c!embedsay` | Bot repeats message in embed form!`\n")
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
async def embedsay(ctx, *, words: str):
  embd = discord.Embed(color=discord.Color(value=0x0086b3))
  embd.description = words
  await ctx.send(embed=embd)
  await ctx.message.delete()
    
@bot.command()
async def invite(ctx):
  await ctx.send("Invite Link Coming Soon...")
    
@bot.command(pass_context=True, hidden=True, name='eval')
async def _eval(ctx, *, body: str):
        """Evaluates a code"""
        if ctx.author.id not in bot.developers: return
        
        env = {
                'bot': bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
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
                await ctx.send(f'```py\n{value}{ret}\n```')


bot.run(os.environ.get("TOKEN"))
