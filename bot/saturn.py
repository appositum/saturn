#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import json
import asyncio

from discord.ext.commands import Bot

if not 'TOKEN' in os.environ:
  print('Token not found, exiting...')
  raise SystemExit
  
if not 'LOG' in os.environ:
  print('Log channel id missing, exiting...')
  raise SystemExit

token = os.environ.get('TOKEN')
log = os.environ.get('LOG')

invite_pattern = re.compile(r'(?:discord\.gg/|discordapp\.com/invite/)([^\s|^\W+$]+)')
last = None

bot = Bot(command_prefix='+')

tex_dict = {
  'ta': r'=tex \rotatebox{180}{$\forall\bot$}'
}

@bot.event
async def on_ready():
  print(f'\n\nLogged in as {bot.user.name} [{bot.user.id}]\n\n')

@bot.event
async def on_message(e):
  global last
  if e.author.id == bot.user.id: return

  if bot.user.id in [x.id for x in e.mentions]:
    await bot.send_file(e.channel, '../media/sanic.png')

  if e.type == 7:
    last = e

  await bot.process_commands(e)

@bot.event
async def on_member_join(member):
  global last
  if invite_pattern.match(member.name) is not None:
    
    while last == None:
      await asyncio.sleep(0.5)

    await bot.delete_message(last)
    await bot.ban(member)

    em = discord.Embed(
      color = 0x36393F,
      title = 'Blocked invite and banned user.'
    )
    em.add_field(
      name = 'Member',
      value = f'<@{member.id}>'
    )
    em.add_field(
      name = 'Invite',  
      value = ''.join(invite_pattern.findall(member.name))
    )

    await bot.send_message(bot.get_channel(log), embed=em)

    last = None

@bot.command(pass_context=True)
async def tex(ctx, key):
  content = tex_dict.get(key)
  if content == None:
    return await bot.say("fodase puta")

  await bot.delete_message(ctx.message)
  msg = await bot.say(content)
  return await bot.delete_message(msg)

bot.run(token)
