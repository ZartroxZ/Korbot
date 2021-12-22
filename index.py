import discord
from discord.ext import commands
import youtube_dl
import asyncio
import urllib.parse, urllib.request


bot = commands.Bot(command_prefix="<0 ", description = "Préfix = <0 ", case_insensitive=True)
musics = {}
ytdl = youtube_dl.YoutubeDL()


@bot.event
async def on_ready():
	print("Ready")

#Musique

class Video:
	def __init__(self, link):
		with ytdl as ydl:
		        try:
		        	get(link)
		        except:
		        	video = ydl.extract_info(f"ytsearch:{link}", download=False)['entries'][0]
		        else:
		        	video = ydl.extract_info(link, download=False)

		video_format = video["formats"][0]
		self.url = video["webpage_url"]
		self.stream_url = video_format["url"]



@bot.command()
async def volume(ctx, vol):
	client = ctx.guild.voice_client
	user_vol_input = float(vol)
	if 0 <= user_vol_input <= 100:
		volume = user_vol_input/100
		client.source.volume = volume
	else:
	 	await ctx.send(' <0 <( Le volume doit être compris entre 0 et 100 )')


@bot.command(aliases=['l'])
async def leave(ctx):
	client = ctx.guild.voice_client
	await client.disconnect()
	musics[ctx.guild] = []

@bot.command(aliases=['1'])
async def resume(ctx):
	client = ctx.guild.voice_client
	if client.is_paused():
		client.resume()

@bot.command(aliases=['0'])
async def pause(ctx):
	client = ctx.guild.voice_client
	if not client.is_paused():
		client.pause()

@bot.command(aliases=['s'])
async def skip(ctx):
	client = ctx.guild.voice_client
	client.stop()
	

def play_song(client, queue, song):
	source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options= "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), volume = 0.5)

	def next(_):
		if len(queue) > 0:
			new_song = queue[0]
			del queue[0]
			play_song(client, queue, new_song)
		else:
			asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

	client.play(source, after=next)


@bot.command(aliases=['p'])
async def play(ctx, *, url):
	print("play")
	client = ctx.guild.voice_client

	if client and client.channel:
		video = Video(url)
		musics[ctx.guild].append(video)
		await ctx.send("<0 <( C'est ajouté à la queue ! )")
	else:
		channel = ctx.author.voice.channel
		video = Video(url)
		musics[ctx.guild] = []
		client = await channel.connect()
		await ctx.send(f"<0 <( Musique ! )")
		play_song(client, musics[ctx.guild], video)

#Moderation
#Random
#Troll

@bot.command(aliases=['Salut', 'Bjr', 'Slt', 'Wesh', 'Hey', 'Heya', 'Eh', 'Eeh', 'Ehh'])
async def Bonjour(ctx):
	await ctx.send('<0 <( KWAK !)')

bot.run("OTIzMjkzMzM5MDQ0OTU4MjQ4.YcN57Q.Va0ODBZfvdoWftxXN3PGU2RyJy8")