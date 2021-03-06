import random
import discord
import asyncio
import aiohttp
import json
import asyncio
import sqlite3
import mysql.connector
import operator

from datetime import datetime
from discord import Game
from bs4 import BeautifulSoup
from discord.ext.commands import Bot



TOKEN = "" #setup enviroment variables (this is not secure)
BOT_PREFIX = "."


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.command(pass_context=True)
async def search(ctx, * args):
    gamertag = ' '.join(args) # creating a space withing the arguments
    urltag = '_'.join(args) # formatting the url so its clickable in discord and in the embed
    async with aiohttp.ClientSession()as session:
        url = "https://forum.project-contingency.com/index.php"
        response = await session.get(f'https://statcore01.pcon.statrepo.com/api/players/{gamertag}')
        resp_json = await response.json() # coverting the data into json
        level = resp_json["Progression"]["Level"]
        totalexp = resp_json["Progression"]["TotalXP"]
        medals = resp_json["Medals"]
        words = ["Games", "Won", "Lost", "Draw", "Kills", "Assists", "Deaths", "Suicides", "Betrayals"]
        statsSummary = ""
        for i in range(8):
            data = words[i] # iterating thru the words by numnber index
            record = resp_json["Summary"][data] # player stats using the words from the word list
            statsSummary += str(data) + ": " + str(record) + "\n"
        kills = resp_json["Summary"]["Kills"]
        deaths = resp_json["Summary"]["Deaths"]
        wins = resp_json["Summary"]["Won"]
        lost = resp_json["Summary"]["Lost"]
        try:
            kdRatio = kills / deaths
        except:
            kdRatio = 0
        kd = (round(kdRatio, 2))
        try:
            winloss = wins / lost
        except:
            winloss = 0
        wlratio = (round(winloss, 2))
        keylist = []
        decendingMedalOrder = sorted(medals.items(), key=lambda x: x[1], reverse=True)
        medaldict = dict(decendingMedalOrder)
        for key in medaldict:
            keylist.append(key)
        topMedals = ""
        for i in range(8):
            data = keylist[i]
            record = medaldict[data]
            topMedals += str(data) + ": " + str(record) + "\n"
        embed = discord.Embed(title=f"COMBAT SERVICE RECORD: {gamertag}", description=" ", url=url, color =0xdd3d20)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/154194845513023489/c5843527cc190b3fcc4c991366072945.webp?size=240")
        embed.add_field(name="Stats Summary", value=f'{statsSummary}', inline=True)
        embed.add_field(name="Top Medals", value=f'{topMedals}', inline=True)
        embed.add_field(name="Level", value=f'Level: {level}\nExperence: {totalexp}', inline=False)
        embed.add_field(name="KD Ratio", value=f'{kd}', inline=True)
        embed.add_field(name="Win Loss Ratio", value=f'{wlratio}', inline=True)
        await ctx.send(embed=embed)

client.run(TOKEN)
