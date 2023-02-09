from time import localtime, strftime
import asyncio
from collections import deque
import discord

emoji_list={'playpause':'\u23EF','prev':'\u23EE','stop':'\u23F9','next':'\u23ED','plus':'🔊','minus':'🔉'}

class player:
    def __init__(self,vc=None):
        self.stack=deque()
        self.queue=deque()
        self.curr=None
        self.voice_client = vc
        self.ctx=None
        self.source=None
        self.f=False
    
    def add_song(self,source):
        self.queue.append(source)
        
    
    def get_song(self):
        if not len(self.queue):
            return 0
        self.curr = self.queue.popleft()
        self.stack.append(self.curr)
        return 1
    
    def get_prev_song(self):
        if not len(self.stack):
            return 0
        self.queue.appendleft(self.curr)
        self.curr = self.stack.pop()
        return 1
    
    def clear_player(self):
        self.stack.clear()
        self.queue.clear()
        self.curr=None
        self.source=None
    
    async def play_song(self,ctx,author):
        
        self.ctx=ctx

        self.source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.curr['url']))
        playerHandler.voice_client.play(self.source)
        self.source.volume=0.75

        duration=self.curr['duration']
        embeds=discord.Embed(title="Now Playing",description=self.curr['title'],color=discord.Color.red())
        embeds.add_field(name='Requested by',value=author,inline=True)
        embeds.add_field(name='Duration',value=f'{ duration /60:0>2.0f}:{duration%60:0>2.0f}',inline=True)
        embeds.add_field(name='Artist',value=self.curr['uploader'],inline=True)
        embeds.set_thumbnail(url=self.curr['thumbnail'])
        embeds.set_footer(text=f"{strftime('%H:%M:%S',localtime()) }")
        
        msg=await ctx.send(embed=embeds)
        for i in emoji_list.values():
            await msg.add_reaction(i)
        
    
    async def play_next_song(self,ctx,author):
        self.ctx=ctx
        f=self.get_song()
        if not f:
            await ctx.send('Queue is empty!')
            return 0
        playerHandler.voice_client.stop()
        await self.play_song(ctx,author)
        return 1
        # await ctx.send("Playing Next Song")
        

    async def play_prev_song(self,ctx,author):
        self.ctx=ctx
        f=self.get_prev_song()
        if not f:
            await ctx.send('No Previous Song!')
            return
        playerHandler.voice_client.stop()
        await self.play_song(ctx,author)
        # await ctx.send("Playing Previous Song")
    
    async def player_loop(self):

        while True:

            if self.voice_client.is_playing() or self.voice_client.is_paused():
                await asyncio.sleep(3)
            else:
                f=await self.play_next_song(self.ctx,self.ctx.author)
                if not f:
                    return
                await asyncio.sleep(3)

playerHandler = player()
