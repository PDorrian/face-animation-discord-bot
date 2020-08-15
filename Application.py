import discord
import aiohttp
import aiofiles
import os
import yaml

client = discord.Client()

@client.event
async def on_message(message):
    # Ignore if message is from the Bot itself
    if message.author == client.user:
        return

    # Check if message contains attachment
    if message.attachments:
        attachment = message.attachments[0]
        print("Attachment received: " + attachment.url)
        # Save attachment
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open('image.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

    if message.content.startswith('.deepfake') or message.content.startswith('.deep'):
        contents = message.content.split()
        command = contents[1]

        if command == 'addreference':
            new_command = contents[2]
            youtube_link = contents[3]

            if 'youtube.com' not in youtube_link and 'youtu.be' not in youtube_link:
                await message.channel.send("ERROR: Video reference must be a YouTube URL.")
                await message.channel.send(".deep addreference <.name> <YouTube URL> [Start Timestamp] [End Timestamp]")

            elif new_command in my_list:
                await message.channel.send("ERROR: Command with that name already exists. Try using another name.")

            else:
                timestamp1 = '00:00:00'
                timestamp2 = ''
                valid_input = True

                if len(contents) > 4:
                    timestamp1 = contents[4]
                    if len(timestamp1) != 8:
                        await message.channel.send("ERROR: Timestamp must be in format hh:mm:ss. Aborting.")
                        valid_input = False

                if len(contents) > 5:
                    timestamp2 = contents[5]
                    if len(timestamp2) != 8:
                        await message.channel.send("ERROR: Timestamp must be in format hh:mm:ss. Aborting.")
                        valid_input = False

                if valid_input:
                    await message.channel.send("Creating new reference...")
                    # Download video
                    os.system('youtube-dl -f worst --output "video/raw.mp4" --recode-video mp4 ' + youtube_link)
                    # Cut to size
                    if timestamp2 == '':
                        os.system('ffmpeg -ss ' + timestamp1 + ' -i video/raw.mp4 video/cut.mp4 -y')
                    else:
                        os.system('ffmpeg -ss ' + timestamp1 + ' -to ' + timestamp2 + ' -i video/raw.mp4 video/cut.mp4 -y')
                    # Crop for deepfake algorithm
                    out = os.popen('python crop-video.py --inp video/cut.mp4').read()
                    os.system(out + ' -y')
                    print(out)
                    # Create driving video and audio files
                    os.system('ffmpeg -i crop.mp4 -q:a 0 -map a driving_video/' + new_command + '_sound.mp3')
                    os.system('ffmpeg -i crop.mp4 -c copy driving_video/' + new_command + '.mp4 -y')

                    os.remove("video/raw.mp4")
                    os.remove("video/cut.mp4")
                    os.remove("crop.mp4")

                    print('New Reference Created')
                    await message.channel.send("New reference created, " + new_command)

                    with open('list.yaml', 'r') as file:
                        up_list = yaml.load(file, Loader=yaml.FullLoader)
                        up_list.append(new_command)
                        my_list.append(new_command)
                        print(up_list)

                    with open('list.yaml', 'w') as file:
                        yaml.dump(up_list, file)

        if command == 'help':
            e = {
                "title": "DeepBot Help",
                "description": "**See list of available reference videos**\n```.deep list```\n**Create a deepfake video**\nPost an image and then use the following command: \n```.deep <name of reference>```\n**Create a new reference video**\nCreate a new reference from a YouTube video, and crop it using optional timestamp parameters.\n```.deep addreference <name> <YouTube URL> [timestamp1] [timestamp2]```\n",
                "color": 14071166,
                "author": "Quibble"
            }
            embed = discord.Embed(title=e["title"], description=e["description"], color=e["color"], author=e["author"])
            await message.channel.send(embed=embed)

        if command == 'list':
            await message.channel.send('\n'+'\n'.join(my_list))

        if command in my_list:
            await message.channel.send("Processing...")
            print("Beginning video")
            os.system("python demo.py  --config config/vox-adv-256.yaml --driving_video driving_video/"+command+".mp4 --source_image image.png --checkpoint checkpoints/vox-adv-cpk.pth.tar --relative --adapt_scale")
            print("Video done")
            os.system("ffmpeg -i result.mp4 -i driving_video/"+command+"_sound.mp3 -vcodec copy -acodec copy final.mp4 -y")
            print("Audio added")
            await message.channel.send(file=discord.File('final.mp4'))

if __name__ == '__main__':
    with open('list.yaml', 'r') as file:
        my_list = yaml.load(file, Loader=yaml.FullLoader)
        print('\n'.join(my_list))

    client.run('NzM4NzY0NDA0MjAzNDU0NDg2.XyQp9w.bmn4B1sl1Y6y0-iBj5X72fZGlbY')

