from discord.ext import commands
import discord
import os
import yaml


class Deep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Create list if it does not already exist
        with open('list.yaml', 'a+') as file:
            file.close()

        # Parse list
        with open('list.yaml', 'r') as file:
            self.my_list = yaml.load(file, Loader=yaml.FullLoader) or []
            if self.my_list != []:
                print('\n'.join(self.my_list))

    @commands.command()
    async def deep(self, message, *args):
        cmd = args[0]

        if cmd == 'list':
            await self.show_list(message)

        elif cmd == 'create':
            if len(args) == 3:
                await self.create_reference(message, args[1], args[2])
            elif len(args) == 4:
                await self.create_reference(message, args[1], args[2], args[3])
            elif len(args) == 5:
                await self.create_reference(message, args[1], args[2], args[3], args[4])
            else:
                await message.channel.send("ERROR: Invalid number of arguments. Do ``.deep help`` for more information.")

        elif cmd == 'delete':
            await self.delete_reference(message, args[1])

        elif cmd == 'help':
            await self.help(message)

        elif cmd in self.my_list:
            await self.deep_create(message, cmd)

        else:
            await message.channel.send("Unrecognised command.")

    async def show_list(self, message):
        if self.my_list:
            await message.channel.send('\n'.join(self.my_list))
        else:
            await message.channel.send("There are currently no references created.")

    async def create_reference(self, message, new_command, youtube_link, timestamp1='00:00:00', timestamp2=''):

        # Check for valid YouTube link
        if 'youtube.com' not in youtube_link and 'youtu.be' not in youtube_link:
            await message.channel.send("ERROR: Video reference must be a YouTube URL.")
            await message.channel.send(".deep addreference <.name> <YouTube URL> [Start Timestamp] [End Timestamp]")

        # Check if command already exists
        elif new_command in self.my_list:
            await message.channel.send("ERROR: Command with that name already exists. Try using another name.")

        else:
            valid_input = True

            # Check start timestamp format
            if len(timestamp1) != 8:
                await message.channel.send("ERROR: Timestamp must be in format hh:mm:ss. Aborting.")
                valid_input = False

            # Check end timestamp format
            if timestamp2 != '' and len(timestamp2) != 8:
                await message.channel.send("ERROR: Timestamp must be in format hh:mm:ss. Aborting.")
                valid_input = False

            if valid_input:
                await message.channel.send("Creating new reference...")
                # Download video
                os.system('youtube-dl -f worst --output "video/raw.mp4" --recode-video mp4 ' + youtube_link)
                # Cut to length
                if timestamp2 == '':
                    os.system('ffmpeg -ss ' + timestamp1 + ' -i video/raw.mp4 video/cut.mp4 -y')
                else:
                    os.system('ffmpeg -ss ' + timestamp1 + ' -to ' + timestamp2 + ' -i video/raw.mp4 video/cut.mp4 -y')

                # Crop for best face alignment
                # Suggest potential crops
                out = os.popen('python crop-video.py --inp video/cut.mp4')
                crops = out.read().split('\n')
                crops[:] = [x for x in crops if x]
                print(crops)

                # Analyse suggestions
                if crops:
                    hi = 0
                    indx = 0
                    for i in range(len(crops)):
                        crop = crops[i].split()
                        if crop:
                            # Choose best fit
                            if float(crop[6]) > hi:
                                hi = float(crop[6])
                                indx = i
                                print(hi, indx)

                    # Crop video
                    new_crop = crops[indx].split()[8][6:-1]
                    print('New crop: ' + new_crop)
                    os.system('ffmpeg -i video/cut.mp4 -filter:v "crop='+ new_crop +', scale=256:256" crop.mp4 -y')

                    # Save new reference
                    os.system('ffmpeg -i crop.mp4 -q:a 0 -map a driving_video/' + new_command + '_sound.mp3')
                    os.system('ffmpeg -i crop.mp4 -c copy driving_video/' + new_command + '.mp4 -y')

                    # Save new reference
                    with open('list.yaml', 'r') as file:
                        up_list = yaml.load(file, Loader=yaml.FullLoader)
                        up_list.append(new_command)
                        self.my_list.append(new_command)
                        print(up_list)
                    with open('list.yaml', 'w') as file:
                        yaml.dump(up_list, file)

                    print('New Reference Created')
                    await message.channel.send("New reference created, " + new_command)

                # No suitable crops found
                else:
                    await message.channel.send('No faces recognised in clip. The clip may be too short or contain too many cuts.')

                # Clean up unnecessary resources
                os.remove("crop.mp4")
                os.remove("video/raw.mp4")
                os.remove("video/cut.mp4")

    async def delete_reference(self, message, reference):
        # Check if reference exists
        if reference in self.my_list:
            # Update list
            with open('list.yaml', 'r') as file:
                up_list = yaml.load(file, Loader=yaml.FullLoader)
                up_list.remove(reference)
                self.my_list.remove(reference)
                print(up_list)

            with open('list.yaml', 'w') as file:
                yaml.dump(up_list, file)

            # Delete files
            try:
                os.remove('driving_video/' + reference + '.mp4')
                os.remove('driving_video/' + reference + '_sound.mp3')
            except OSError as e:
                print("Failed with:", e.strerror)

            await message.channel.send("Reference deleted, ``" + reference + "``.")

        else:
            await message.channel.send("No reference found with name ``" + reference + "``.")

    @staticmethod
    async def help(message):
        e = {
            "title": "DeepBot Help",
            "description": "**See list of available reference videos**\n```.deep list```\n**Create a deepfake video**\nPost an image and then use the following command: \n```.deep <name of reference>```\n**Create a new reference video**\nCreate a new reference from a YouTube video, and crop it using optional timestamp parameters.\n```.deep create <name> <YouTube URL> [timestamp1] [timestamp2]``` \n**Delete an existing reference video**. \n```.deep delete <reference name>```\n",
            "color": 14071166,
            "author": "Quibble"
        }
        embed = discord.Embed(title=e["title"], description=e["description"], color=e["color"], author=e["author"])
        await message.channel.send(embed=embed)

    @staticmethod
    async def deep_create(message, cmd):
        await message.channel.send("Processing...")
        print("Beginning video")
        # python demo.py  --config config/vox-adv-256.yaml --driving_video driving_video/stop.mp4 --source_image image.png --checkpoint checkpoints/vox-adv-cpk.pth.tar --relative --adapt_scale
        os.system(
            "python demo.py  --config config/vox-adv-256.yaml --driving_video driving_video/" + cmd + ".mp4 --source_image image.png --checkpoint checkpoints/vox-adv-cpk.pth.tar --relative --adapt_scale")
        print("Video done")
        os.system(
            "ffmpeg -i result.mp4 -i driving_video/" + cmd + "_sound.mp3 -vcodec copy -acodec copy final.mp4 -y")
        print("Audio added")
        await message.channel.send(file=discord.File('final.mp4'))
