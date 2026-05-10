import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from agents.chief_of_staff import handle_message

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Chief of Staff online as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.name != "general":
        return

    async with message.channel.typing():
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, handle_message, message.content)
        for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
            await message.channel.send(chunk)

    await bot.process_commands(message)


if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not set in .env")
    bot.run(token)
