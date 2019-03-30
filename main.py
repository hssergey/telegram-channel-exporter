import settings
from telethon.client.telegramclient import TelegramClient
from telethon import events
import os
import traceback
import datetime

client = None

if settings.use_proxy:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash, proxy = settings.proxy_data).start()
else:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash).start()


@client.on(events.NewMessage(incoming=True))
async def handle_new_mesage(event):
	chat = await event.get_input_chat()
	try:
		channel_id = chat.channel_id
# 		print("from: %s" % channel_id)
# 		print(event.text)
		if channel_id:
			channel_folder = "%s/%s" % (settings.channels_folder, channel_id)
			if not os.path.isdir(channel_folder):
				os.mkdir(channel_folder)
			timestamp = datetime.datetime.now().strftime('%s')
			file = open("%s/%s.txt" % (channel_folder, timestamp), "w")
			file.write(event.text)
			file.close()
	except Exception as ex:
		traceback.print_exc()
		
	

print("Telegram Channel Exporter is running")
client.run_until_disconnected()

	