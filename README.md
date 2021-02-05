# Face Animation Bot for Discord
This is a bot for creating "deepfake" memes on Discord.<br>
It provides a convenient I/O interface for the First Order Motion Model library. Users can easily create new references from YouTube links as well as animate images.<br>
<br>
This repository contains code from [First Order Motion Model for Image Animation](https://github.com/AliaksandrSiarohin/first-order-model) by Aliaksandr Siarohin, Stéphane Lathuilière, Sergey Tulyakov, Elisa Ricci and Nicu Sebe.<br>

---

## Demo
![Visual Demonstration](https://github.com/PDorrian/face-animation-discord-bot/blob/master/demo.gif)

---

## How to Install
This application supports ``python3``.<br>
```git clone https://github.com/PDorrian/face-animation-discord-bot.git --recursive```

### Requirements
```pip install -r requirements.txt```<br>
You will also need to install ffmpeg (and add it to PATH if on Windows).

### Pre-trained Checkpoint
Download ``vox-adv-cpk.pth.tar`` from one of the following links: [google-drive](https://drive.google.com/open?id=1PyQJmkdCsAkOYwUyaj_l-l0as-iLDgeH) or [yandex-disk](https://yadi.sk/d/lEw8uRm140L_eQ).<br>
Place the file within the ``/checkpoints/`` folder.

### Attach to Bot
Create ``key.txt`` within the main directory and include your Bot Token in this file.

### Run
``python Application.py``

---

## How to Use
Simply message ``.deep help`` in any Discord channel to see a list of commands.

> #### See list of available reference videos
> ```.deep list```
>
> #### Create a deepfake video
> Post an image and then use the following command: .deep <reference name>
>
> #### Create a new reference video
> Create a new reference from a YouTube video, and crop it using optional timestamp parameters. .deep create <reference name> <YouTube URL> [timestamp1] [timestamp2]

> #### Delete an existing reference video.
> .deep delete <reference name>