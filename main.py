import asyncio
import os
import time

import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add it in Railway Variables.")

CHANNEL_ID = os.getenv("CHANNEL_ID")
if not CHANNEL_ID:
    raise RuntimeError("CHANNEL_ID is missing. Set the Discord channel ID where you want commands to be sent.")

PREFIX = os.getenv("OWO_PREFIX", "owo ")
COMMAND_INTERVAL = int(os.getenv("COMMAND_INTERVAL_SECONDS", "10"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
TARGET_CHANNEL_ID = int(CHANNEL_ID)


async def send_owo_command(command: str) -> None:
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(TARGET_CHANNEL_ID)

    if channel is None:
        print(f"Channel {TARGET_CHANNEL_ID} not found. Verify CHANNEL_ID.")
        return

    await channel.send(f"{PREFIX}{command}")
    print(f"[{time.strftime('%H:%M:%S')}] Sent: {PREFIX}{command}")


@tasks.loop(seconds=COMMAND_INTERVAL)
async def owo_loop() -> None:
    await send_owo_command("h")
    await asyncio.sleep(1)
    await send_owo_command("b")


@owo_loop.before_loop
async def before_owo_loop() -> None:
    await bot.wait_until_ready()


@bot.event
async def on_ready() -> None:
    print(f"✅ Logged in as {bot.user}")
    print(f"📍 Target channel ID: {TARGET_CHANNEL_ID}")
    print(f"⏱️ Every {COMMAND_INTERVAL} seconds: {PREFIX}h then {PREFIX}b")
    print("🚀 Automation started!")


@bot.command(name="status")
async def status(ctx: commands.Context) -> None:
    await ctx.send(
        f"Prefix: `{PREFIX}`\n"
        f"Channel ID: `{TARGET_CHANNEL_ID}`\n"
        f"Interval: `{COMMAND_INTERVAL}` seconds\n"
        f"Sequence: `owo h` -> wait 1s -> `owo b`"
    )


if __name__ == "__main__":
    bot.run(TOKEN)
