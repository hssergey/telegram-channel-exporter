import settings
from telethon.client.telegramclient import TelegramClient
from telethon import events
import os
import traceback
import datetime
import urllib.parse
import re
from re import RegexFlag
import json
import random
from telethon.utils import get_peer_id

client = None

pattern = re.compile('[^\d\w\s,_\-\+=\<\>\.!\?\*;\%@\&\(\)\[\]\'\"\$:\\\/\#]', RegexFlag.IGNORECASE)

if settings.use_proxy:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash, proxy = settings.proxy_data).start()
else:
	client = TelegramClient('telegramChannelExporter', settings.api_id, settings.api_hash).start()


@client.on(events.NewMessage)
async def handle_new_mesage(event):
	chat = await event.get_input_chat()
	try:
		try:
			channel_id = chat.channel_id
		except Exception:
			channel_id = get_peer_id(chat)
		msg_from = None
		# Check if the message is a forwarded message
		if event.message.fwd_from:
			fwd = event.message.fwd_from
			# Check if the forward header contains a from_id reference
			if fwd.from_id:
				# Retrieve the entity for the original sender (if it was a channel, this is a PeerChannel)
				original_entity = await client.get_entity(fwd.from_id)
				# Many channel entities have a title attribute
				if hasattr(original_entity, 'title'):
					msg_from = original_entity.title
				else:
					# Fallback: sometimes the fwd_from header contains a from_name attribute
					if fwd.from_name:
						msg_from = fwd.from_name
		print(f'from: {channel_id}, {msg_from}')
		print(event.text)
		if channel_id:
			channel_folder = "%s/%s" % (settings.channels_folder, channel_id)
			if not os.path.isdir(channel_folder):
				os.mkdir(channel_folder)
			messages = []
			text = event.text
			if msg_from:
				text = f'{text}\n\nForwarded from: {msg_from}'
			text = text.replace("«", "\"")
			text = text.replace("»", "\"")
			text = pattern.sub('', text)
			messages.append(text)
			if event.media:
				try:
					filename = await client.download_media(event.media, file = settings.media_folder)
					basename = urllib.parse.quote(os.path.basename(filename))
					url = "%s%s" % (settings.url_start, basename)
					messages.append("\n")
					messages.append(url)
				except Exception as ex:
					traceback.print_exc()				
			timestamp = datetime.datetime.now().strftime('%s')
			file = open("%s/%s-%s.txt" % (channel_folder, timestamp, random.randint(100000, 999999)), "w")
			for message in messages:
				file.write(message)
			file.close()
				
	except Exception as ex:
		traceback.print_exc()
		
	

print("Telegram Channel Exporter is running")
client.run_until_disconnected()

	
