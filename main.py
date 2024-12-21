from typing import Final
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from algocop import text_analysis, api_key

TOKEN: Final = "8072728393:AAEv6-XZ7e2JRIa0Pt9hTyur6Z3OIef_7uI"
BOT_USRENAME: Final = "@reality_checkerbot"

user_input_variable: str = ""  # Declare a variable to store the user's input

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = (
        "Hello! I am a bot that can check the reality of the news you send me.\n"
        "Just send me the news and I will tell you if it is real or fake.\n\n"
        "Here are some commands you can use:\n"
        "/start - Start the bot and see this message\n"
        "You can also just send me any news article or text, and I will analyze it for you."
    )
    await update.message.reply_text(start_message)

async def save_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_input_variable  # Declare the variable as global to modify it
    user_input_variable = update.message.text  # Save the user's text to the variable
    print(f"Saved user input: {user_input_variable}")  # Print the saved input for confirmation
    await update.message.reply_text(f"Your input has been saved")  # Await the reply_text coroutine
    await update.message.reply_text(f"Searching for the reality of the news...")  # Await the reply_text coroutine

    response = text_analysis(user_input_variable, api_key)  # Call the text_analysis function with the user's input
    await update.message.reply_text(response)  # Await the reply_text coroutine with the response
    

# Responses
def handle_response(text: str) -> str:
    if "news" in text:
        return "This is a response to the user's news."
    return "This is a response to the user's input."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f"User ({update.message.chat.id}) in {message_type}: {text}")
    
    if message_type == "group":
        if BOT_USRENAME in text:
            next_text: str = text.replace(BOT_USRENAME, "")
            response: str = handle_response(next_text)
        else:
            return
    else:
        response : str = handle_response(text)
        
    print("Bot: ", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, save_user_input))
    
    print("Polling...")
    app.run_polling()