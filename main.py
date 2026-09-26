import asyncio
import os
import random

import discord
from discord.ext import commands, tasks


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add it in Railway Variables.")

CHANNEL_ID = os.getenv("CHANNEL_ID")
if not CHANNEL_ID:
    raise RuntimeError("CHANNEL_ID is missing. Set the Discord channel ID where you want commands to be sent.")

PREFIX = os.getenv("OWO_PREFIX", "owo ")
BASE_DELAY = max(10, int(os.getenv("COMMAND_INTERVAL_SECONDS", "30")))
ENABLE_PRAY = os.getenv("ENABLE_PRAY", "true").lower() == "true"
ENABLE_RANDOM = os.getenv("ENABLE_RANDOM_COMMANDS", "true").lower() == "true"

DEFAULT_COMMANDS = ["hunt", "battle"]
if ENABLE_PRAY:
    DEFAULT_COMMANDS.append("pray")

if ENABLE_RANDOM:
    DEFAULT_COMMANDS.extend(["inv", "cash", "z", "q", "cl", "my", "team", "top", "top 25 c"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
TARGET_CHANNEL_ID = int(CHANNEL_ID)


def pick_command() -> str:
    """Choose a command with a bias toward hunt and battle."""
    weighted = [
        "hunt",
        "battle",
        "hunt",
        "battle",
        "hunt",
        "battle",
    ]
    if ENABLE_PRAY:
        weighted.append("pray")
    if ENABLE_RANDOM:
        weighted.extend(["inv", "cash", "z", "q", "cl", "my", "team", "top", "top 25 c"])
    return random.choice(weighted)


async def send_owo_command(command: str) -> None:
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(TARGET_CHANNEL_ID)

    if channel is None:
        print(f"Channel {TARGET_CHANNEL_ID} not found. Verify CHANNEL_ID.")
        return

    await channel.send(f"{PREFIX}{command}")
    print(f"Sent: {PREFIX}{command} to #{channel.name}")


@tasks.loop(seconds=BASE_DELAY)
async def owo_loop() -> None:
    command = pick_command()
    await send_owo_command(command)


@owo_loop.before_loop
async def before_owo_loop() -> None:
    await bot.wait_until_ready()


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Target channel ID: {TARGET_CHANNEL_ID}")
    print("OwO automation loop started.")
    owo_loop.start()


@bot.command(name="owo")
async def manual_owo(ctx: commands.Context, *args: str) -> None:
    """Send a command manually to the configured channel."""
    if not args:
        await ctx.send("Usage: `!owo hunt` or `!owo battle`")
        return

    command = " ".join(args)
    await send_owo_command(command)
    await ctx.send(f"Queued command: `{PREFIX}{command}`")


@bot.command(name="status")
async def status(ctx: commands.Context) -> None:
    await ctx.send(
        f"OwO prefix: `{PREFIX}`\n"
        f"Channel ID: `{TARGET_CHANNEL_ID}`\n"
        f"Interval: `{BASE_DELAY}` seconds\n"
        f"Enabled commands: `{", ".join(DEFAULT_COMMANDS)}`"
    )


if __name__ == "__main__":
    bot.run(TOKEN)
