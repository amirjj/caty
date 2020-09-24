from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, requests
from bot_config import BotConf

token = BotConf.token

updater = Updater(token=token, use_context=True)
disparcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cat(update, context):
	resp = requests.get('https://api.thecatapi.com/v1/images/search')
	if resp.status_code != 200:
		return False
	for item in resp.json():
		url = item.get('url')
		print(url)
		context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text='This is test!')

def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
	start_handler = CommandHandler('start', start)
	get_cat_handler = CommandHandler('get',get_cat)
	echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

	disparcher.add_handler(start_handler)
	disparcher.add_handler(echo_handler)
	disparcher.add_handler(get_cat_handler)

	updater.start_polling()
	updater.idle()
	# updater.stop()

if __name__ == '__main__':
	main()