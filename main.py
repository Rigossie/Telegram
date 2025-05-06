from telethon import TelegramClient, events
import re
import os
from dotenv import load_dotenv

# Laad de .env variabelen
load_dotenv()

# API info
api_id = int(os.getenv("API_ID"))  # API ID uit .env
api_hash = os.getenv("API_HASH")  # API Hash uit .env

# Telegram channels
source_channel = 'Siralphagems_bot'
target_channel = 'paris_trojanbot'

# Telefoonnummer (hardcoded)
phone_number = '+31653319421'

# Start client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message.message

    try:
        lines = message.split('\n')
        if len(lines) < 2:
            return  # Geen geldig bericht

        contract = lines[1].strip()  # Tweede regel = Solana CA adres

        # Zoek en parse overige variabelen
        created_match = re.search(r'Created at: (\d+)m', message)
        smart_buyers = int(re.search(r'💸 (\d+) smart money have bought', message).group(1))
        still_holding = int(re.search(r'Still Holding: (\d+)', message).group(1))
        gt_2_sol = int(re.search(r'Greater Than 2 SOL: (\d+)', message).group(1))
        bot_buyer = int(re.search(r'Bot Buyer: (\d+)', message).group(1))
        trades_match = re.search(r'5min Trades: (\d+) Buys, (\d+) Sells', message)
        buys = int(trades_match.group(1))
        sells = int(trades_match.group(2))

        # Filterregels toepassen
        if (
            created_match and int(created_match.group(1)) <= 20
            and smart_buyers >= 20
            and still_holding >= 11
            and gt_2_sol >= 14
            and bot_buyer >= 100
            and buys >= 2000
            and sells >= 1500
        ):
            await client.send_message(target_channel, contract)

    except Exception as e:
        print(f"[!] Fout bij parsen of doorsturen: {e}")

async def start_client():
    await client.start(phone_number=phone_number)  # Start de client met je telefoonnummer
    client.run_until_disconnected()  # Houd de client actief

# Voer het script uit
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(start_client())
