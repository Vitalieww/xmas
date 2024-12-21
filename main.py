from typing import Final
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, ContextTypes
TOKEN: Final = "8113622873:AAGj-tYISqoP-RBe_ZJQcWD2BG10g2FC_2gY"
BOT_USRENAME: Final = "@Reality_checker_bot"


#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am a bot that can check the reality of the news you send me. Just send me the news and I will tell you if it is real or fake.")
    

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("If you have any questions, feel free to ask me. I am here to help you.")
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")
    
#Responses

def handle_response(text: str) -> str:
    return "This is a response to the user's input."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message_type 
    pass
    


