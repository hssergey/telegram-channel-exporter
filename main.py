import settings
from telethon.client.telegramclient import TelegramClient
from telethon import events

client = None

if settings.use_proxy:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash, proxy = settings.proxy_data).start()
else:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash).start()


@client.on(events.NewMessage(incoming=True))
async def handle_new_mesage(event):
	chat = await event.get_input_chat()
	print("from: %s" % chat.channel_id)
	print(event.text)
	

print("Telegram Channel Exporter is running")
client.run_until_disconnected()

	