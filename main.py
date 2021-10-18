import os
import discord
import requests
from keep_alive import keep_alive
from spellchecker import SpellChecker
import random
from consts import first, second, third
import re
from replit import db

# accepted_words = ["mannan", "LMAO"]
# db["accepted_words"] = ["mannan", "LMAO"]


discord_key = os.environ['discordkey']
splash_key = os.environ['splashapikey']
url = "https://api.unsplash.com/photos/random?client_id="

client = discord.Client()
spell = SpellChecker()
# spell.word_frequency.load_words(accepted_words)

def addAccpetedWord(word):
  if "accepted_words" in db.keys():
    accepted_words = db["accepted_words"]
    accepted_words.append(word)
    db["accepted_words"] = accepted_words
    spell.word_frequency.load_words(accepted_words)
  else:
    db["accepted_words"] = [word]
    spell.word_frequency.load_words([word])

def callApi():
  response = requests.get(url + splash_key)
  if(response.status_code == 200):
    jres = (response.json())
    imageLink = jres["urls"]["raw"]
    return imageLink
  return

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  

@client.event
async def on_message(message):
  if message.author == client.user:
    return


  msg = message.content
  if msg.startswith("!pic"):
    await message.channel.send(callApi())
    return

  if msg.startswith("!add"):
      word = msg.split("!add ",1)[1]
      print(word)
      addAccpetedWord(word)
      await message.channel.send("New word "+ word + " added.")
      return

  if msg.startswith("!accepted"):
    accepted_words = []
    if "accepted_words" in db.keys():
      accepted_words = db["accepted_words"]
    await message.channel.send(accepted_words.value)
    return


  #Checking if user has role spell
  # dont do anything if not
  roles = message.author.roles
  name = message.author.name
  
  check = False
  for role in roles:
    if role.name == "spell":
      check = True
  if not check: return
 

  #checking for punctuation
  tokenized = msg.split()
  for i,strr in enumerate(tokenized):
    lastChar = strr[-1]
    if lastChar == "?" or lastChar == "," or lastChar == "!" or lastChar == ".":
      tokenized[i] = strr[:-1]
      
    x = re.search("<a:.+?:\d+>|<:.+?:\d+>", strr)
    if x:
      tokenized[i] = "match"

    if(strr.startswith("@")): 
       tokenized[i] = "tag"

    if len(strr) == 1:
      ascii = ord(strr)
      if ascii < 0 or ascii > 140:
        tokenized[i] = "emote"
      # tokenized[i] = ""
      

  misspelled = spell.unknown(tokenized)
  text = name + ", "
  for word in misspelled:
    corrected = spell.correction(word)
    if corrected == word:
      text += word + " is misspelled. The word was spelled so poorly that no suggestions were found.\n"
    else:
      text += word + " is misspelled. I think you meant "+ spell.correction(word) +"\n"
    # await message.channel.send(text)
  if len(misspelled) > 0:
    random.randint(0,9)
    await message.channel.send(text + "Learn to spell, you " + first[random.randint(0,len(first)-1)] + " " +second[random.randint(0,len(second)-1)] + " "+ third[random.randint(0,len(third)-1)] + ".")


keep_alive()
client.run(discord_key)