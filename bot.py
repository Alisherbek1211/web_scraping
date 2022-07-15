import logging
from bs4 import BeautifulSoup as BS
import requests

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Andijan"),KeyboardButton("Namangan")],
        [KeyboardButton("Nukus"),KeyboardButton("Qarshi")],
        [KeyboardButton("Samarkand"),KeyboardButton("Uchkuduk")],
        [KeyboardButton("Tashkent")]
    
    ]
    )
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Assalomu Alaykum {user.mention_markdown_v2()}\! \n\n Ob\-havo bo\'timizga xush kelibsiz\.Menudan birini tanlang\.',
        reply_markup=menu,
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def get_url(update: Update, context: CallbackContext) -> None:
    URL = f"https://www.timeanddate.com/weather/uzbekistan/{update.message.text}/ext"
    page = requests.get(URL)
    soup = BS(page.content, "html.parser")
    posts = soup.find_all("div", class_="row pdflexi")
    # titles = []
    # for post in posts:
        # titles.append(post.find("td",class_="small").text)
    posts = soup.find_all("div", class_="row pdflexi")[0].find("td",class_="small").text
    # print(posts)  

    update.message.reply_text(posts)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5470778624:AAHzp7Vp9Kod3wgFkvreaGDx7PqWnogM1ko")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()