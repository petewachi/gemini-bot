import configs.DefaultConfig as config
import utils.DiscordUtil as discord_utils

import asyncio
import discord
from discord.ext import commands
from LLM.GeminiImageBE import GeminiAgent

# Configure bot intents
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Bot is now online.")

@bot.event
async def on_member_join(member):
    print("A new member has joined.")
    guild = member.guild
    guild_name = guild.name
    dm_channel = await member.create_dm()
    await dm_channel.send(f"Welcome to {guild_name}! Feel free to ask me questions here.")

@bot.command(aliases=["about"])
async def help(ctx):
    embed = discord.Embed(
        title="Commands",
        description="These are the commands you can use with this bot. In a private message with the bot, you can interact without issuing commands.",
        color=discord.Color.dark_purple()
    )
    embed.set_thumbnail(url="https://th.bing.com/th/id/OIG.UmTcTiD5tJbm7V26YTp.?w=270&h=270&c=6&r=0&o=5&pid=ImgGn")
    embed.add_field(name="!query", value="Use this command to communicate with the Gemini AI Bot on the server. Wrap your questions in quotation marks.", inline=False)
    embed.add_field(name="!pm", value="Use this command to send a private message to the Gemini AI Bot.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.check(discord_utils.is_me)
async def unload_gemini(ctx):
    await bot.remove_cog('GeminiAgent')

@bot.command()
@commands.check(discord_utils.is_me)
async def reload_gemini(ctx):
    await bot.add_cog(GeminiAgent(bot))

async def start_cogs():
    await bot.add_cog(GeminiAgent(bot))

# Run the bot
asyncio.run(start_cogs())
bot.run(config.DISCORD_SDK_TOKEN)
