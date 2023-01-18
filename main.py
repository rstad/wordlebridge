import os
import re
import discord
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
rex = re.compile(r'Wordle [0-9]{3,}')
botrex = re.compile(r'WordleBot\nSkill')
fivegreens = "🟩🟩🟩🟩🟩"
padline = "❌❌❌❌❌"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

def get_server_nick(server,author):
    try:
        member = server.get_member(author.id)
        if member.display_name:
            return member.display_name
        else:
            return author.name
    except:
        return author.name

def transform_message(message):
    if re.search(rex,message).start() == 0: # no starting word, straight wordle paste
        if re.search(fivegreens,message) != None: # not X/6
            if re.search(botrex,message) != None: # has wordlebot scores
                formatted_message = ""
                header = message.split('\n')[0]
                slindex = header.find("/")
                formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0]
                formatted_message += fivegreens+"\n"
                for i in range(5-len(re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                    formatted_message+=padline+'\n'
                formatted_message += '||\nWordleBot\n'
                formatted_message += re.split(rex,message)[1].split('\n\nWordleBot\n')[1]
                return formatted_message
            else: # straight paste, solved, no wordlebot
                formatted_message = ""
                header = message.split('\n')[0]
                slindex = header.find("/")
                formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0]
                formatted_message += fivegreens+"\n"
                for i in range(5-len(re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                    formatted_message+=padline+'\n'
                formatted_message = formatted_message.strip()
                formatted_message += re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[1]+"||"
                return formatted_message
        else: # straight paste, failed
            if re.search(botrex,message) != None: # has wordlebot scores
                formatted_message = ""
                header = message.split('\n')[0]
                slindex = header.find("/")
                formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1]+"||"
                formatted_message += '\n\nWordleBot\n'
                formatted_message += re.split(rex,message)[1].split('\n\nWordleBot\n')[1]
                return formatted_message
            else: # no wordlebot score, straight paste, failed
                formatted_message = ""
                header = message.split('\n')[0]
                slindex = header.find("/")
                formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1]+"||"
                return formatted_message
    else: # has a leading word
        if re.search(fivegreens,message) != None: # not X/6
            if re.search(botrex,message) != None: # has wordlebot scores
                formatted_message = re.split(rex,message)[0].strip().upper()+'\n'
                header = message.split('\n')[0]
                slindex = header.find("/")
                windex = header.find("Wordle")
                formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0]
                formatted_message += fivegreens+"\n"
                for i in range(5-len(re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                    formatted_message+=padline+'\n'
                formatted_message += '||\nWordleBot\n'
                formatted_message += re.split(rex,message)[1].split('\n\nWordleBot\n')[1]
                return formatted_message
            else:
                formatted_message = re.split(rex,message)[0].strip().upper()+'\n'
                header = message.split('\n')[0]
                slindex = header.find("/")
                windex = header.find("Wordle")
                formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1]+'\n'
                for i in range(5-len(re.split(rex,message)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                    formatted_message+=padline+'\n'
                formatted_message = formatted_message.strip()+"||"
                return formatted_message
        else:
            if re.search(botrex,message) != None: # has wordlebot scores
                formatted_message = re.split(rex,message)[0].strip().upper()+'\n'
                header = message.split('\n')[0]
                slindex = header.find("/")
                windex = header.find("Wordle")
                formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1]+"||"
                formatted_message += '\n\nWordleBot\n'
                formatted_message += re.split(rex,message)[1].split('\n\nWordleBot\n')[1]
                return formatted_message
            else: # failed, so no padding
                formatted_message = re.split(rex,message)[0].strip().upper()+'\n'
                header = message.split('\n')[0]
                slindex = header.find("/")
                windex = header.find("Wordle")
                formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
                formatted_message += "||"+re.split(rex,message)[1].split('\n\n')[1]+"||"
                return formatted_message

def is_wordle_message(message):
    if re.search(rex,str(message)):
        return True
    else:
        return False

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user: #ignore self messages
        return
    #print(str(message.content))
    if is_wordle_message(message.content):
        print("is wordle message")
        formatted_message = transform_message(message.content)
        fmh_wordle = client.get_channel(1064641280791019623)
        rta_general = client.get_channel(692795745409171589)
        rta_guild = client.get_guild(692795745409171586)
        print(message)
        print(message.content)
        print(get_server_nick(rta_guild,message.author))
        print(formatted_message)
        if not message.guild: # is DM?
            try:
                await rta_general.send(get_server_nick(rta_guild,message.author)+" "+formatted_message)
                await fmh_wordle.send(get_server_nick(rta_guild,message.author)+" "+formatted_message)
            except discord.errors.Forbidden:
                pass
        else: # not DM
            if message.channel.id == 1064641280791019623: #fmh wordle
                try:
                    await rta_general.send(get_server_nick(rta_guild,message.author)+" "+formatted_message)
                except discord.errors.Forbidden:
                    pass
            if message.channel.id == 692795745409171589: #rt2a general
                try:
                    await fmh_wordle.send(get_server_nick(rta_guild,message.author)+" "+formatted_message)
                except discord.errors.Forbidden:
                    pass
    else:
        print("not wordle message")
        pass

client.run(BOT_TOKEN)
