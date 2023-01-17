import os
import re
import discord
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
rex = re.compile(r'Wordle [0-9]{3,}')
fivegreens = "🟩🟩🟩🟩🟩"
padline = "❌❌❌❌❌"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def transform_message(message):
    author = message.author.name
    #print(author)
    if re.search(rex,message.content).start() == 0: # no starting word, straight wordle paste
        if re.search(fivegreens,message.content) != None: # not X/6
            formatted_message = author + '\n'
            header = message.content.split('\n')[0]
            slindex = header.find("/")
            formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
            formatted_message += "||"+re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[0]
            formatted_message += fivegreens+"\n"
            for i in range(5-len(re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                formatted_message+=padline+'\n'
            formatted_message += re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[1]+"||"
            return formatted_message
        else: # failed, so no padding
            formatted_message = author + '\n'
            header = message.content.split('\n')[0]
            slindex = header.find("/")
            formatted_message += header[:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
            formatted_message += "||"+re.split(rex,message.content)[1].split('\n\n')[1]+"||"
            return formatted_message
    else: # has a leading word
        if re.search(fivegreens,message.content) != None: # not X/6
            formatted_message = author + " " + re.split(rex,message.content)[0].strip().upper()+'\n'
            header = message.content.split('\n')[0]
            slindex = header.find("/")
            windex = header.find("Wordle")
            formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
            formatted_message += "||"+re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[0]
            formatted_message += fivegreens+"\n"
            for i in range(5-len(re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[0].strip().split('\n'))):
                formatted_message+=padline+'\n'
            formatted_message += re.split(rex,message.content)[1].split('\n\n')[1].split(fivegreens)[1]+"||"
            return formatted_message
        else: # failed, so no padding
            formatted_message = author + " " + re.split(rex,message.content)[0].strip().upper()+'\n'
            header = message.content.split('\n')[0]
            slindex = header.find("/")
            windex = header.find("Wordle")
            formatted_message += header[windex:slindex-2]+" ||"+header[slindex-1]+"||"+header[slindex:]+'\n\n'
            formatted_message += "||"+re.split(rex,message.content)[1].split('\n\n')[1]+"||"
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
        formatted_message = transform_message(message)
        #print(formatted_message)
        fmh_wordle = client.get_channel(1064641280791019623)
        rta_general = client.get_channel(692795745409171589)
        if not message.guild: # is DM?
            try:
                await fmh_wordle.send(formatted_message)
                await rta_general.send(formatted_message)
            except discord.errors.Forbidden:
                pass
        else: # not DM
            if message.channel.id == 1064641280791019623: #fmh wordle
                try:
                    await rta_general.send(formatted_message)
                except discord.errors.Forbidden:
                    pass
            if message.channel.id == 692795745409171589: #rt2a general
                try:
                    await fmh_wordle.send(formatted_message)
                except discord.errors.Forbidden:
                    pass
    else:
        print("not wordle message")
        pass

client.run(BOT_TOKEN)
