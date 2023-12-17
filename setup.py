import discord
from discord.ext import commands
import asyncio
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load bot token from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    BOT_TOKEN = config.get('token', '')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def setup(ctx, server_id: int, num_channels: int, channel_name_template: str, *, message_content: str):
    # Check if the user has the appropriate permissions to run the command
    if ctx.author.guild_permissions.administrator:
        guild = bot.get_guild(server_id)
        if guild:
            await delete_all_text_channels(guild)

            tasks = []
            for i in range(num_channels):
                channel_name = f'{channel_name_template}-{i + 1}'
                tasks.append(create_channel_and_messages(ctx, guild, channel_name, message_content, 50))

                if len(tasks) >= 50:
                    await asyncio.gather(*tasks)
                    tasks = []

            if tasks:
                await asyncio.gather(*tasks)
            await ctx.send("setup setup complete.")
        else:
            await ctx.send("Invalid server ID.")
    else:
        await ctx.send("You don't have permission to run this command.")

async def delete_all_text_channels(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.delete()

async def create_channel_and_messages(ctx, guild, channel_name, message_content, num_messages):
    channel = await guild.create_text_channel(channel_name)
    for _ in range(num_messages):
        await channel.send(message_content)

bot.run(BOT_TOKEN)
