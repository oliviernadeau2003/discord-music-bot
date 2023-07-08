# import discord

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#   print("We have logged in as {0.user}".format(client))


# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return

#   if message.content.startswith("!hello"):
#     await message.channel.send("Hi ! \nHow are you {0}".format(message.author))

#   if message.content.startswith("!creator"):
#     await message.channel.send(
#       "Hi {0} ! \nMy creator is Mr.SkyzZ#5790,\nTell him thank you for making me alive. I am happy to serve my good lord."
#       .format(message.author))
#   if message.content.startswith("!commands"):
#      await message.channel.send("Hey Humans,\nThese are my commands:\n!hello\n!creator")

# client.run("TOKEN")

# -------------------------------------------

import os
import discord
from pytube import YouTube
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

song_queue = []



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()

    voice_client = ctx.guild.voice_client

    # try:
    #     video = YouTube(url)
    #     audio_stream = video.streams.filter(only_audio=True).first()
    #     file_path = f"./{video.video_id}.mp4"
    #     audio_stream.download(output_path="./", filename=video.video_id)
    #     # Rest of the code...
    

    #     if os.path.exists(file_path):
    #         # Renommer le fichier uniquement s'il existe
    #         os.rename(file_path, file_path + ".mp4")
    #         file_path = file_path + ".mp4"
    #         # Ajout de la musique à la liste d'attente
    #         song_queue.append((file_path, video.title))

    #         if len(song_queue) == 1:
    #             # Si la liste d'attente est vide, commence la lecture immédiatement
    #             await play_song(ctx, voice_client)
    #     else:
    #         await ctx.send("An error occurred while downloading the video.")
    
    # except Exception as e:
    #     await ctx.send(f"An error occurred while downloading the video: {str(e)}")
    
    
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    file_path = f"./{video.video_id}.mp4"
    audio_stream.download(output_path="./", filename=video.video_id + ".mp4")


    if os.path.exists(file_path):
        # Ajout de la musique à la liste d'attente
        song_queue.append((file_path, video.title))

        if len(song_queue) == 1:
            # Si la liste d'attente est vide, commence la lecture immédiatement
            await play_song(ctx, voice_client)
    # else:
    #     await ctx.send("An error occurred while downloading the video.")



async def play_song(ctx, voice_client):
    if len(song_queue) == 0:
        return

    file_path, song_title = song_queue[0]

    # if voice_client.is_playing() or voice_client.is_paused():
    #     # Si le bot est déjà en train de jouer de l'audio, ne rien faire
    #     return

    # Jouer la musique
    voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: bot.loop.create_task(on_song_end(ctx, voice_client, file_path)))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)

    # Afficher le titre de la musique en cours de lecture
    await ctx.send(f'Now playing: {song_title}')

    # Retirer la musique de la liste d'attente
    if len(song_queue) > 0:
        song_queue.pop(0)



async def on_song_end(ctx, voice_client, file_path):
    # Supprimer le fichier audio de la musique
    os.remove(file_path)

    if len(song_queue) > 0:
        # S'il y a encore des musiques dans la liste d'attente, jouer la prochaine
        await play_song(ctx, voice_client)
    else:
        # S'il n'y a plus de musiques dans la liste d'attente, déconnecter le bot
        await voice_client.disconnect()



@bot.command()
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Music skipped.')

    if voice_client.is_playing() or voice_client.is_paused():
        return

    if len(song_queue) > 0:
        # S'il y a encore des musiques dans la liste d'attente, jouer la prochaine
        await play_song(ctx, voice_client)
    else:
        # S'il n'y a plus de musiques dans la liste d'attente, déconnecter le bot
        await voice_client.disconnect()

    if len(song_queue) > 0:
        await cleanup_song(song_queue[0][0])



@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()



@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()
        await ctx.send('Music stopped.')

        if len(song_queue) > 0:
            await cleanup_song(song_queue[0][0])



@bot.command()
async def queue(ctx):
    # Construction du message de la file d'attente
    song_queue_message = "Current Song Queue:\n"
    for index, music in enumerate(song_queue, start=0):
        song_title = music[1]
        song_queue_message += f"{index+1}. {song_title}\n" 

    # Envoi du message de file d'attente dans le canal où la commande a été exécutée
    await ctx.send(song_queue_message)



async def cleanup_song(file_path):
    # Supprimer le fichier audio de la musique
    os.remove(file_path)



bot.run(os.getenv("TOKEN"))
# bot.run("")




