# Vibez - Discord Music Bot
Vibez is a Discord music bot built using Python and the Discord API that allows users to listen to music when connected to a voice channel in the server. Users can access the bot using the prefix '/'. Vibez can play songs based on the song name or link from YouTube and Spotify.

# Installation

1. Clone this repository to your local machine.
`git clone https://github.com/<your_username>/Vibez.git`

2. Install the necessary packages using pip.
`pip install -r requirements.txt`

3. Create a new bot on the Discord developer portal and add it to your Discord server. Refer to the Discord API documentation for detailed instructions on how to do this.

4. Rename .env.example to .env and add your bot token to the file.

5. Run the bot.py file to start the bot.
`python bot.py`

# Commands
## Vibez supports the following commands:

- /play <song name/link> - plays the requested song in the voice channel.
- /pause - pauses the current song.
- /resume - resumes the current song.
- /skip - skips the current song.
- /stop - stops playing music and clears the queue.
- /queue - shows the current song queue.
- /volume <value> - sets the volume of the bot (0-100).

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more details.
