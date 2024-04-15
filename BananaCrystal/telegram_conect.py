"""
This is a simple discord bot that connects to the discord server and implements functions from the faq_bot_skeleton to interact with a user, understand intent and give appropraite reponse

Michael Oj, January 2024
"""
import telegram
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes
from faq_bot import *

botUsername = '@B_CrystalBot'
## MYClient Class Definition

class MyClient(telegram.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = telegram.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves and other bots
        if message.author == self.user or message.author.bot:
            return

        # get the utterance and generate the response
        utterance = message.content
        utterance = utterance.lower()
        if utterance.endswith("?") or utterance.endswith(".") or utterance.endswith(" "):
            utterance = utterance[0:len(utterance)-1]
        
        if goodbye_intention(utterance):
            response = """Goodbye! 
It was nice having a chat with you. See ya"""
           
        elif start_chat_intention(utterance):
            response = hello_intention_response()
        elif re.findall(r'help', utterance):
            response = help_info()
        else:
            intent = understand(utterance)
            response = generate(intent)
            print(response)

        # send the response
        await message.channel.send(response)

client = MyClient()
with open("telegram_token.txt") as file:
    token = file.read()
client.run(token)