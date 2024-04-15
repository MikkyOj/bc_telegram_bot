from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from faq_bot import *
from api import *
from naija_api import *

with open("telegram_token.txt") as file:
    token = file.read()
    
botUsername = '@B_Crystalbot'


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am B_Crystal. Thanks for choosing BananaCrystal 😊. How can I help you? ")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = help_info()
    await update.message.reply_text(responses)



async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This will be improved with time...")

async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = """BananaCrystal Conversion Rates

Note: conversion is against USD

Enter the currency and amount to convert (Eg. EUR 500)"""
    await update.message.reply_text(responses)
    
    
# handle responses and logic
def handle_response(utterance: str) -> str:
    user_input = utterance.strip().split()  # Split user input
    if len(user_input) == 2:
        return handle_conversion(utterance)

    utterance = utterance.lower()
    if utterance.endswith("?") or utterance.endswith(".") or utterance.endswith(" "):
            utterance = utterance[0:len(utterance)-1]      
    if goodbye_intention(utterance):
            return """Goodbye! 
It was nice having a chat with you. See ya"""
    elif start_chat_intention(utterance):
            return hello_intention_response()
    elif re.findall(r'help', utterance):
        return help_info()
    else:
        intent = understand(utterance)
        return generate(intent)

#  handle messages and chatting with them
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    utterance: str = update.message.text
    
    print(f'User {update.message.chat.id} in {message_type}: {utterance}')
    
    if message_type == 'group':
        if botUsername in utterance:
            new_utterance = utterance.replace(botUsername, "").strip()
            reponse: str = handle_response(new_utterance)
        else:
            return
    else:
        reponse: str = handle_response(utterance)
        
    print("Bot: ", reponse)
    await update.message.reply_text(reponse)
        
        
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print (f'Update: {update} caused error {context.error}')
  
  
# Handler for processing the conversion request
def handle_conversion(utterance):
    user_input = utterance.strip().split()  # Split user input
    
    try:
        amount = float(user_input[1])  # Extract amount
        target_currency = user_input[0].upper()  # Extract target currency and convert to uppercase
    except ValueError:
        intent = understand(utterance)
        return generate(intent)
    
    base_currency = 'USD'  # Base currency

    if target_currency not in exchange_rates:
        return "Sorry, conversion for this currency is not supported."

    if target_currency == 'NGN':
        print (exchange_rate)
        rate = exchange_rate[target_currency]
    else:
        rate = exchange_rates[target_currency]
        
    converted_amount = amount / rate
    converted_amount = format(converted_amount, '.2f')
    
    print (exchange_rates['NGN'])
    
    response = f"""{amount} {target_currency} = {converted_amount} {base_currency}
    
At {rate} {target_currency} per {base_currency}"""
    return response
    
    
async def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print ("Starting Bot")
    app = Application.builder().token(token).build()
    
    # commands
    app.add_handler(CommandHandler('start', start_command))    
    app.add_handler(CommandHandler('help', help_command))    
    app.add_handler(CommandHandler('custom', custom_command)) 
    app.add_handler(CommandHandler('convert', convert_command)) 
    
    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message)) 
    
    # errpr
    app.add_error_handler(error)
    
    #  check for updates
    print ("Polling")
    app.run_polling(poll_interval=3)