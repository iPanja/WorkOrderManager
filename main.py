import discord
from discord.ext import commands
import config

#Discord API
discordToken = config.discord["key"]
bot = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='Reddit discord bot request')

modules = [
    'cogs.Manager'
]

for cog in modules:
    try:
        bot.load_extension(cog)
    except Exception as e:
        message = 'Failed to load module {0}\n{1} : {2}'.format(cog, type(e).__name__, e)
        bot.send_message("368100617543221260", message)
        print(message)

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after);
        return;
    if isinstance(error, commands.CommandNotFound):
        return
    raise error;

bot.run(discordToken)