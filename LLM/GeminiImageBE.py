import configs.DefaultConfig as config
from discord.ext import commands
import google.generativeai as genai

# Configure generative AI
genai.configure(api_key=config.GEMINI_API)
DISCORD_MAX_MESSAGE_LENGTH = 2000
ERROR_MESSAGE = 'There was an issue with your question, please try again.'

class GeminiAgent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if msg.content == "ping gemini-agent":
                await msg.channel.send("Agent is connected.")
            elif 'Direct Message' in str(msg.channel) and not msg.author.bot:
                response = self.generate_gemini_content(msg.content)
                dm_channel = await msg.author.create_dm()
                await self.send_message_in_chunks(dm_channel, response)
        except Exception as e:
            await msg.channel.send(ERROR_MESSAGE + str(e))

    @commands.command()
    async def query(self, ctx, question):
        try:
            response = self.generate_gemini_content(question)
            await self.send_message_in_chunks(ctx, response)
        except Exception as e:
            await ctx.send(ERROR_MESSAGE + str(e))

    @commands.command()
    async def pm(self, ctx):
        dm_channel = await ctx.author.create_dm()
        await dm_channel.send('Hi, how can I assist you today?')

    def generate_gemini_content(self, content):
        try:
            response = self.model.generate_content(content, stream=True)
            return response
        except Exception as e:
            return ERROR_MESSAGE + str(e)

    async def send_message_in_chunks(self, ctx, response):
        message = ""
        for chunk in response:
            message += chunk.text
            if len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extra_message = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extra_message
        if len(message) > 0:
            while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extra_message = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extra_message
            await ctx.send(message)
