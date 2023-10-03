from inspect import indentsize
import discord
from discord.ext import commands
import youtube_dl
import requests
import random

# Initialize bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=indentsize)

# Moderation Commands
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# Music Commands
@bot.command()
async def play(ctx, url):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name='Music')
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(url2))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = 0.07

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()

# Currency System
users = {}

@bot.command()
async def balance(ctx):
    user = ctx.author
    if user.id not in users:
        users[user.id] = 1000
    await ctx.send(f'Your balance is {users[user.id]} credits.')

@bot.command()
async def gamble(ctx, amount: int):
    user = ctx.author
    if user.id not in users:
        users[user.id] = 1000
    if amount <= users[user.id]:
        # Simulate a 50/50 chance of winning
        import random
        if random.choice([True, False]):
            users[user.id] += amount
            await ctx.send(f'Congratulations! You won {amount} credits. Your balance is now {users[user.id]} credits.')
        else:
            users[user.id] -= amount
            await ctx.send(f'Oops! You lost {amount} credits. Your balance is now {users[user.id]} credits.')
    else:
        await ctx.send('Insufficient funds.')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    await ctx.send(f'Server Name: {server.name}\nTotal Members: {server.member_count}')

@bot.command()
async def assignrole(ctx, role: discord.Role, member: discord.Member):
    await member.add_roles(role)
    await ctx.send(f'{member.mention} has been given the {role.name} role.')

@bot.command()
async def removerole(ctx, role: discord.Role, member: discord.Member):
    await member.remove_roles(role)
    await ctx.send(f'{role.name} role has been removed from {member.mention}.')

@bot.command()
async def weather(ctx, city: str):
    api_key = 'YOUR_WEATHER_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        await ctx.send(f'The weather in {city} is {weather_description} with a temperature of {temperature}°C.')
    else:
        await ctx.send('Invalid city name. Please try again.')

@bot.command()
async def quote(ctx):
    response = requests.get('https://api.quotable.io/random')
    data = response.json()
    quote = data['content']
    author = data['author']
    await ctx.send(f'"{quote}" - {author}')



@bot.command()
async def showinfo(ctx):
    embed = discord.Embed(title='Bot Information', description='This is a complex Discord bot!', color=discord.Color.green())
    embed.add_field(name='Creator', value='Your Name', inline=False)
    embed.add_field(name='Version', value='1.0', inline=False)
    embed.set_footer(text='Custom Footer')
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, question, *options):
    if len(options) > 10:
        await ctx.send("Error: You can only provide up to 10 options.")
    else:
        formatted_options = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
        poll_message = await ctx.send(f"**Poll Question:** {question}\n**Options:**\n{formatted_options}")
        for i in range(len(options)):
            await poll_message.add_reaction(chr(0x1F1E6 + i))

@bot.command()
async def randomnum(ctx, min_num: int, max_num: int):
    random_number = random.randint(min_num, max_num)
    await ctx.send(f"Random Number: {random_number}")

@bot.command()
async def joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    joke_setup = data["setup"]
    joke_punchline = data["punchline"]
    await ctx.send(f"**Setup:** {joke_setup}\n**Punchline:** {joke_punchline}")

@bot.command()
async def define(ctx, word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    data = response.json()
    if isinstance(data, list):
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        await ctx.send(f"**Definition of {word}:** {meaning}")
    else:
        await ctx.send("Word not found. Please try another word.")

@bot.command()
async def roll(ctx):
    dice_result = random.randint(1, 6)
    await ctx.send(f"🎲 You rolled a {dice_result}!")

@bot.command()
async def github(ctx, user, repo):
    response = requests.get(f"https://api.github.com/repos/{user}/{repo}")
    data = response.json()
    if 'message' not in data:
        stars = data['stargazers_count']
        forks = data['forks_count']
        issues = data['open_issues_count']
        await ctx.send(f"**Repository:** {user}/{repo}\n**Stars:** {stars}\n**Forks:** {forks}\n**Open Issues:** {issues}")
    else:
        await ctx.send("Repository not found.")

@bot.command()
async def cute(ctx):
    response = requests.get("https://aws.random.cat/meow")
    data = response.json()
    image_url = data['file']
    await ctx.send(f"Here's a cute animal picture: {image_url}")



# Run the bot
bot.run('YOUR_DISCORD_TOKEN')
