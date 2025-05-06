import os
import re
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_channel = 'Siralphagems_bot'  # bronkanaal
destination_channel = 'paris_trojanbot'  # doelkanaal

# Regex om Solana-adres te extraheren (43-44 tekens, base58-compatible)
solana_regex = r'\b[1-9A-HJ-NP-Za-km-z]{43,44}\b'

with TelegramClient('session', api_id, api_hash) as client:
    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        message_text = event.message.message
        if "SOL" in message_text.upper() and "LP" in message_text.upper():
            matches = re.findall(solana_regex, message_text)
            if matches:
                for sol_address in matches:
                    await client.send_message(destination_channel, sol_address)

    print("Bot is gestart en luistert naar nieuwe berichten...")
    client.run_until_disconnected()