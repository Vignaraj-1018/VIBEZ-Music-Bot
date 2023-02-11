import discord
import youtube_dl

from player import *
from config import *

bot = discord.Bot()

@bot.event
async def on_ready():
    print("bot ready")

# @bot.event
# async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):

#     print(error)
#     if isinstance(error,Exception):
#         # await ctx.send('Please Connect to a Voice Channel')
#         print("Ignoring")
#     else:
#         print(error)


@bot.slash_command(name='hello',description='Responds Hello')
async def hello(ctx):
    await ctx.respond("Hello")


@bot.slash_command(name='play',description='Play a song')
async def play(ctx,msg):
    
    await ctx.respond('Command Success')
    
    if not ctx.author.voice:
        await ctx.send("Please Connect to a Voice Channel!")
        return

    if not playerHandler.voice_client:
        playerHandler.voice_client = await ctx.author.voice.channel.connect()

    if not playerHandler.voice_client.is_connected():
        await playerHandler.voice_client.connect(reconnect=True,timeout=60)
    
    playerHandler.author=ctx.author
    
    link_type=get_link_type(msg)

    if link_type=='YouTube' or link_type=='YouTube-Playlist':
        
        if link_type=='YouTube-Playlist':
            await ctx.send("Please wait While I Process the Playlist")
        info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f'{msg}', download=False)

        if '_type' in info and info['_type']=='playlist':
            playlist=info['entries']
            
            if playerHandler.voice_client.is_playing():
                playerHandler.add_song(playlist[0])
            else:
                playerHandler.add_song(playlist[0])
                playerHandler.get_song()
                await ctx.send(f"Playing {msg}")
                await playerHandler.play_song(ctx)

            for i in playlist[1:]:
                playerHandler.add_song(i)
            
            await ctx.send("Playlist Processing Done!")
            
        else:
            if playerHandler.voice_client.is_playing():
                playerHandler.add_song(info)
                await ctx.send(f"{info['title']} is added to Queue")
            else:
                playerHandler.add_song(info)
                playerHandler.get_song()
                await ctx.send(f"Playing {msg}")
                await playerHandler.play_song(ctx)
        

    elif link_type=='Spotify-Track' or link_type=='Song Name':
        if link_type=='Spotify-Track':
            track=sp.track(msg.split('/')[-1].split('?')[0])
            search=f"{track['name']} {track['album']['artists'][0]['name']}"
            msg=search
        
        info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f'ytsearch:{msg}', download=False)
        info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f"https://youtu.be/{info['entries'][0]['id']}", download=False)
        
        if playerHandler.voice_client.is_playing():
            playerHandler.add_song(info)
            await ctx.send(f"{info['title']} is added to Queue")
        else:
            playerHandler.add_song(info)
            playerHandler.get_song()
            await ctx.send(f"Playing {msg}")
            await playerHandler.play_song(ctx)
    
    elif link_type=='Spotify-Playlist':
        sp_playlist=sp.playlist(msg)
        playlist=[]
        for i in sp_playlist['tracks']['items']:
            artists=[_['name'] for _ in i['track']['artists']]
            playlist.append(f"{i['track']['name']}, {''.join(artists)}")
        
        info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f'ytsearch:{playlist[0]}', download=False)
        info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f"https://youtu.be/{info['entries'][0]['id']}", download=False)
        if playerHandler.voice_client.is_playing():
                playerHandler.add_song(info)
        else:
            playerHandler.add_song(info)
            playerHandler.get_song()
            await ctx.send(f"Playing {msg}")
            await playerHandler.play_song(ctx)

        for i in playlist[1:]:
            info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f'ytsearch:{i}', download=False)
            info = youtube_dl.YoutubeDL(ydl_opts).extract_info(f"https://youtu.be/{info['entries'][0]['id']}", download=False)
            playerHandler.add_song(info)

        await ctx.send("Playlist Processing Done!")

    else:
        await ctx.send(f"Invalid Link: {msg}")
        return

        
    
    # if not playerHandler.voice_client.is_playing():
    #     playerHandler.add_song(info)
    #     f=playerHandler.get_song()
    #     if not f:
    #         await ctx.send('Queue is empty!')
    #         return
    #     await ctx.send(f"Playing {msg}")
    #     await playerHandler.play_song(ctx)
    #     return
    
    # if playerHandler.voice_client.is_playing():
    #     playerHandler.add_song(info)
    #     await ctx.send(f"{info['title']} is added to Queue")
    if not playerHandler.f:
        bot.loop.create_task(playerHandler.player_loop())
        playerHandler.f=True


@bot.slash_command(name='pause',description='Pause the current playing song')
async def pause(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client and playerHandler.voice_client.is_playing():
        playerHandler.voice_client.pause()
        await ctx.send("Song Paused")
    else:
        await ctx.send("No Song is Playing")


@bot.slash_command(name='next',description='Plays the next song')
async def next(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client:
        await playerHandler.play_next_song(ctx)
        

@bot.slash_command(name='previous',description='Plays the previous song')
async def previous(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client:
        await playerHandler.play_prev_song(ctx)
        

@bot.slash_command(name='resume',description='Resumes the song')
async def resume(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client and playerHandler.voice_client.is_paused():
        playerHandler.voice_client.resume()
        await ctx.send("Song Resumed")
    
    else:
        await ctx.send("No Song is Playing")


@bot.slash_command(name='stop',description='Stops the song')
async def stop(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client and playerHandler.voice_client.is_playing():
        playerHandler.voice_client.stop()
        playerHandler.clear_player()
        await ctx.send("Song Stopped")
    else:
        await ctx.send("No Song is Playing")

@bot.slash_command(name='disconnect',description='Disconnects from the Voice Channel')
async def disconnect(ctx):

    await ctx.respond('Command Success')

    if playerHandler.voice_client:
        await playerHandler.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel in this server.")

@bot.slash_command(name='queue',description='Displays the Queue')
async def queue(ctx):
    
    await ctx.respond('Command Success')

    embed = discord.Embed(title="Music Queue", description="List of songs in the queue:",color=discord.Color.red())
    for i, song in enumerate(playerHandler.queue):
        embed.add_field(name=f"Song {i+1}: ", value=song['title'], inline=True)

    await ctx.send(embed=embed)
    

@bot.event
async def on_reaction_add(reaction, user):
    
    if not user.bot:
        message = reaction.message
        ctx=await bot.get_application_context(message)
        print(user)
        if reaction.emoji==emoji_list['playpause']:
            if playerHandler.voice_client.is_playing():
                print('Pause')
                if playerHandler.voice_client and playerHandler.voice_client.is_playing():
                    playerHandler.voice_client.pause()
                    await ctx.send("Song Paused")
                else:
                    await ctx.send("No Song is Playing")
            else:
                print('Play')
                if playerHandler.voice_client and playerHandler.voice_client.is_paused():
                    playerHandler.voice_client.resume()
                    await ctx.send("Song Resumed")
                
                else:
                    await ctx.send("No Song is Playing")

        elif reaction.emoji==emoji_list['prev']:
            print("Previous")
            if playerHandler.voice_client:
                await playerHandler.play_prev_song(ctx)
        
        elif reaction.emoji==emoji_list['stop']:
            print("Stop")
            if playerHandler.voice_client and playerHandler.voice_client.is_playing():
                playerHandler.voice_client.stop()
                playerHandler.clear_player()
                await ctx.send("Song Stopped")
            else:
                await ctx.send("No Song is Playing")
        
        elif reaction.emoji==emoji_list['next']:
            print("Next")
            if playerHandler.voice_client:
                await playerHandler.play_next_song(ctx)
        
        elif reaction.emoji==emoji_list['plus']:

            if playerHandler.source.volume<1.0:
                playerHandler.source.volume+=0.1
            
            print(playerHandler.source.volume)

        elif reaction.emoji==emoji_list['minus']:

            if playerHandler.source.volume>0.0:
                playerHandler.source.volume-=0.1
            
            print(playerHandler.source.volume)

        await reaction.message.remove_reaction(reaction.emoji,user)

bot.run(DISCORD_TOKEN)