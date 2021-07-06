import discord
import os
import requests
import json
import random
from replit import db
from awake import keep_alive


client = discord.Client()

# *****----------- Responds -----------*****
mad_words = ['pissed', 'mad', 'retarded', 'curse']
mad_emotes = ['🤬', '😡', '😠', '😾']
sad_words = ['sad', 'depressed', 'sucks', 'feeling sick', 'sad life', 'cry']
sad_emotes = ['😞', '😦', '😔', '😟', '🙁', '😭', '😢', '🥺', '😩', '😫', '😖', '😣', '😿']
sad_replies = ["Don't be sad!, Here have a choco :chocolate_bar:", "Awww, *hugs* ", "Want some coffee?",
               "Hang in there! ", "You okay ?",
               "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif?itemid=5166500",
               "https://media1.tenor.com/images/af76e9a0652575b414251b6490509a36/tenor.gif?itemid=5640885",
               "https://media1.tenor.com/images/7822479112cf7625937e8c56ff5824b4/tenor.gif?itemid=20994171",
               "https://tenor.com/view/kanna-kamui-pat-head-pat-gif-12018819",
               "https://tenor.com/view/rascal-does-not-dream-of-bunny-girl-senpai-seishun-buta-yar%c5%8d-anime-head"
               "-pat-rest-gif-17747839", 
               "https://tenor.com/view/aqua-kawaii-anime-headpat-gif-18563260",
               "https://tenor.com/view/pat-head-gif-10947495"]

mad_replies = ["Calm Down", "Someone hold me back!", "Take a chill pill",
               "https://media1.tenor.com/images/434e6240d0e6e088561ab65315fba4cd/tenor.gif?itemid=4587974",
               "https://media1.tenor.com/images/e836480caeb3c6e86643ede4e017c6b1/tenor.gif?itemid=15459499",
               "https://media1.tenor.com/images/26c7733e0c85c23b3f27580a4a67393b/tenor.gif?itemid=7936649",
               "https://media1.tenor.com/images/3723ddd625070248a6ef93632f1e813f/tenor.gif?itemid=14106751",
               "https://media1.tenor.com/images/f6222cfc5a127c9a4c30545c440479d2/tenor.gif?itemid=17436390",
               "https://media1.tenor.com/images/21476e4e1122a86df09fd944a5368d9e/tenor.gif?itemid=10525006"]
inspiring = ['inspire', 'inspiring', 'inspiration', 'motivate', 'motivation', 'encourage', 'cheer']
# *****----------- Responds -----------*****

# Set Respond
if "responding" not in db.keys():
    db["responding"] = True


# Get Quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


# update encouraging message
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


# delete encouraging message
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        encouragements.remove(encouragements[index])
        db["encouragements"] = encouragements


# Bot Connected
@client.event
async def on_ready():
    print("{0.user} in the system.".format(client))


# Reading messages
@client.event
async def on_message(message):
    msg = str.lower(message.content)

    # Check user
    if message.author == client.user:
        return

    # Modify Replies
    options = sad_replies
    if "encouragements" in db.keys():
        options = options + list(db["encouragements"])

    # show list
    if msg.startswith('*getlist'):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    #  update message function
    if msg.startswith('*new '):
        encouraging_message = msg.split("*new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("Message added Bro :thumbsup:")

    # delete message function
    if msg.startswith('*del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("*del", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    # Set respond on/off/status
    if msg.startswith("*responding"):
        value = msg.split("*responding ", 1)[1]
        if value.lower() == "on":
            db["responding"] = True
            await message.channel.send('now responding! :thumbsup: ')
        elif value.lower() == "off":
            db["responding"] = False
            await message.channel.send('not responding! :thumbsup: ')
        elif value == "?":
            await message.channel.send(db["responding"])
        else:
          db["responding"] = False

          
    if db["responding"]:

        # send motivational quotes
        if any(ins in msg for ins in inspiring):
            quote = get_quote()
            await message.channel.send(quote)

        # happy
        if msg.startswith('happy'):
            await message.channel.send('Yay!')
        if msg.startswith('yay'):
            await message.channel.send('Cheers! :coffee: ')

        # choose from list for sad
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))
        # time.sleep(3)
        if any(emote in message.content for emote in sad_emotes):
            await message.channel.send(random.choice(options))

        #  choose from list for mad
        if any(word in msg for word in mad_words):
            await message.channel.send(random.choice(mad_replies))
        # time.sleep(3)
        if any(emote in message.content for emote in mad_emotes):
            await message.channel.send(random.choice(mad_replies))

        # fixed values for random
        if message.content.startswith('<@!860537488749494343>'):
            await message.channel.send("https://tenor.com/view/popcat-cat-dance-vibes-gif-19916705")
        
        # Server specific 
        if msg.startswith('bonk'):
            await message.channel.send('<:bonk:860761495125753857>')
        if msg.startswith('good morning'):
            await message.channel.send('Ohayo!')
        if msg.startswith('uwu'):
            await message.channel.send('<:UwU:860765307722793000>')
        if message.content.startswith('<:UwU:860765307722793000>'):
            await message.channel.send("(ᵘ ꒳ ᵘ) nyaa")
        if message.content.startswith('<:LewdMegumin:860398275252191243>'):
            await message.channel.send("That's it! You are going to Horny Jail")

keep_alive()
client.run(os.environ['TOKEN'])
