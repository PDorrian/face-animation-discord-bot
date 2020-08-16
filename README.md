# DeepBot for Discord
This is a bot for creating deepfake memes on Discord.

## Installation
This application supports ``python3``.
```git clone https://github.com/PDorrian/DeepBot --recursive```

### Requirements
```pip install -r requirements.txt```
You will also need to install ffmpeg (and add it to PATH if on Windows).

### Pre-trained Checkpoint
Download ``vox-adv-cpk.pth.tar`` from one of the following links: [google-drive](https://drive.google.com/open?id=1PyQJmkdCsAkOYwUyaj_l-l0as-iLDgeH) or [yandex-disk](https://yadi.sk/d/lEw8uRm140L_eQ).
Place the file within the ``/checkpoints/`` folder.

### Attach to Bot
Create ``key.txt`` within the main directory and include your Bot Token in this file.

### Run
``python Application.py``

## Using the Bot
Simply message ``.deep help`` in any Discord channel to see a list of commands.