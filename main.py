import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging module, so you will know when (and why) things don't work as expected.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# This function will be used as a callback for the /start command.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message to the chat id that issued the /start command.
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# This function is a callback for the echo command. It sends back the same message that the user sent.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.bot.send_message is a method that sends a message to a user.
    # chat_id is the id of the chat where the command was issued.
    # text is the text to be sent. Here we are simply echoing the text the user sent.
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# This function is a callback for the caps command. It converts the input text to uppercase and sends it back.
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ' '.join(context.args) joins all the arguments into a single string.
    # .upper() converts the string to uppercase.
    text_caps = ' '.join(context.args).upper()
    # Send the uppercase string back to the user.
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# This function is a callback for unknown commands. It sends a message to the user saying that the command was not understood.
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message to the user saying that the command was not understood.
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    file_directory = os.path.dirname(__file__)
    # Change the current working directory to the file's directory
    os.chdir(file_directory)

    # Open the file and read the token.
    with open('./token', 'r') as f:
        token = f.read().strip()  # The strip() function removes any leading/trailing whitespace.

    # Create an Application object.
    application = ApplicationBuilder().token(token).build()
    
    # CommandHandler is a handler subclass that handles Telegram commands.
    # CommandHandler instances are used to register command callback functions in the Application.
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    # Register the handler in the Application.
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)

    # Start the application and run it until you hit CTRL+C.
    application.run_polling()
