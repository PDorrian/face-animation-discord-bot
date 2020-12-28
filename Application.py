import discord
from discord.ext import commands
import aiohttp
import aiofiles

from Deep import Deep

if __name__ == '__main__':
    with open('key.txt') as k:
        key = k.readline()

    client = discord.Client()
    bot = commands.Bot(command_prefix='.', description='QuibBot')
    bot.add_cog(Deep(bot))
    bot.run(key, bot=True, reconnect=True)

    @bot.event
    async def on_message(message):
        if message.attachments and not message.author.bot:
            attachment = message.attachments[0]
            print("Attachment received: " + attachment.url)
            # Save attachment
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open('image.png', mode='wb')
                        await f.write(await resp.read())
                        await f.close()

        await bot.process_commands(message)




