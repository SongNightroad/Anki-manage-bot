# Anki-manage-bot
A bot wich will help you to manage your Anki deck remotely.

The working version is not deployed yet, the first version is currently developing in the dev-01 brunch. 

# Python Telegram Bot

This Python-based Telegram bot uses the `aiotg` library for asynchronous interaction with the Telegram Bot API. 

## Functionality

The bot currently supports the following commands:

- `/start`: The bot responds with a welcoming message.
- `/help`: The bot provides information about available commands.
- `/caps`: Converts the following message text to uppercase.
- Non-command text: The bot activates an "echo mode" upon receiving a `/add` command, where it will echo back any non-command text message it receives. This mode is deactivated upon receiving a `/stop-add` command.

## Deployment Instructions

1. **Set up your Python environment**: Ensure you have Python 3.7 or higher installed on your system. It's also recommended to create a virtual environment for this project.

2. **Install the necessary Python libraries**: Install the `aiotg` library using pip:
    ```
    pip install aiotg
    ```
3. **Clone the bot code**: Clone the bot code from the repository or download it to your local system.

4. **Get a Bot Token from Telegram**: To use the Telegram Bot API, you will need a bot token. You can get this from the BotFather bot on Telegram. Save this token into a file named "token" in the same directory as your bot script.

5. **Run the bot**: Execute the bot script using Python. The bot should now be running and ready to receive messages.
    ```
    python bot.py
    ```
6. **Interact with the bot**: Start a chat with your bot on Telegram. You should be able to interact with it using the commands described above.

Remember to replace the token in the deployment instructions with your own Telegram Bot API token.


