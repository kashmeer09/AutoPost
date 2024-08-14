import discord
from discord.ext import tasks
from datetime import datetime
import asyncio
from embedd import create_embed
from channel import CHANNEL_IDS

BOT_TOKEN = 'BOT TOKEN HERE'

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

last_messages = {}

time_units = {
    'seconds': 1,
    'minutes': 60,
    'hours': 3600,
    'days': 86400,
    'weeks': 604800,
    'months': 2592000
}

async def send_message():
    global last_messages

    embed = create_embed()

    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            if channel_id in last_messages and last_messages[channel_id]:
                await last_messages[channel_id].delete()

            last_messages[channel_id] = await channel.send(embed=embed)

@tasks.loop(seconds=60)
async def autopost_task(ctx, time_interval):
    while True:
        await send_message()
        await asyncio.sleep(time_interval)

async def start_autopost(ctx, interval, unit):
    """Start the autopost with a specified interval and time unit."""
    unit = unit.lower()
    
    if unit not in time_units:
        print("Invalid time unit. Please use one of the following: seconds, minutes, hours, days, months.")
        return
    
    time_interval = interval * time_units[unit]
    
    print(f"Auto Post Has Started Upload Time Sets To: {interval} {unit}(s).")
    autopost_task.change_interval(seconds=time_interval)
    await autopost_task.start(ctx, time_interval)

async def stop_autopost(ctx):
    """Stop the autopost."""
    autopost_task.cancel()
    print("The Auto Post Has Been Interrupted!!!")
    
    global last_messages
    for channel_id, message in last_messages.items():
        if message:
            await message.delete()
    last_messages = {}

async def main():
    print("Bot is running. Use the following commands to control it:")
    print("start [interval] [unit] - to start the auto-posting")
    print("stop - to stop the auto-posting")

    while True:
        command = input("Enter Command Here: ").strip().lower()
        if command.startswith("start"):
            try:
                _, interval, unit = command.split()
                interval = int(interval)
                await start_autopost(bot.get_channel(CHANNEL_IDS[0]), interval, unit)
            except ValueError:
                print("Invalid command format. Use: start [interval] [unit]")
        elif command == "stop":
            await stop_autopost(bot.get_channel(CHANNEL_IDS[0]))
        else:
            print("Unknown command. Please use 'start' or 'stop'.")

@bot.event
async def on_ready():
    print(f'[@kshmrzz] Bot has been connected as: {bot.user}')
    await main()

bot.run(BOT_TOKEN)