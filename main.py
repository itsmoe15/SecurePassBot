import os
import discord
from discord.ext import commands
import hashlib
import requests
import random
import string
import time
import dotenv

dotenv.load_dotenv()

prefix = os.getenv('DISCORD_PREFIX') # Replace with your bot prefix in .env file
token = os.getenv('DISCORD_TOKEN') # Replace with your bot token in .env file

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

# define a function to check the password
def check_password(password):
    # Hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Query the HIBP API with the first 5 characters of the password hash
    response = requests.get(f'https://api.pwnedpasswords.com/range/{sha1_password[:5]}')

    # Check if the full password hash appears in the response
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if sha1_password[5:] == hash_suffix:
            return int(count)
    return 0

@client.event
async def on_ready():
    print('The Bot is up and running!.')




def generate_password(length=12):
    """Generate a random password with the specified length."""
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password




tipsJar = ["Use strong and unique passwords: Create long, complex passwords that are difficult to guess or crack. Avoid using the same password for multiple accounts, as this can make it easier for hackers to gain access to multiple accounts if one password is compromised.",
           "Enable two-factor authentication: Two-factor authentication adds an extra layer of security to your accounts by requiring a second form of authentication, such as a code sent to your phone or an app on your device.",
           "Update your passwords regularly: Change your passwords periodically to reduce the risk of your account being compromised. Consider changing your passwords every few months or whenever there is a security breach at a website or service you use.",
           "Use a password manager: Password managers can help you generate and store strong, unique passwords for all your accounts. This can make it easier to remember and manage your passwords while also keeping them secure.",
           "Be careful with your personal information: Avoid sharing personal information, such as your email address or phone number, with unknown or untrusted sources. Be cautious about clicking on links or downloading attachments from emails or messages that you don't recognize.",
           "Use a mix of character types: Include a mix of uppercase and lowercase letters, numbers, and symbols in your passwords. This can make them more difficult to guess or crack.",
           "Avoid common words and patterns: Don't use common words or phrases in your passwords, and avoid using patterns or sequences (such as '1234' or 'abcd'). These can be easy for hackers to guess or crack.",
           "Make your passwords long: The longer your password is, the harder it is to guess or crack. Aim for a minimum of 12 characters, and consider using a passphrase made up of multiple words.",
           "Avoid personal information: Don't use personal information, such as your name, birthdate, or address, in your passwords. This information can be easily obtained by hackers or identity thieves.",
           "Don't reuse passwords: Avoid using the same password for multiple accounts, as this can make it easier for hackers to gain access to multiple accounts if one password is compromised."]

tip = lambda: random.choice(tipsJar)

#use command ?pwd
@client.event
async def on_message(message):
    if message.content.lower() == "generate":
        await message.reply(f"🔒 Here\`s a good 12 charecter long password you can use: `{generate_password()}` !.")
    else:
        if message.author == client.user:
            return
        elif isinstance(message.channel, discord.DMChannel): # A leak has been detected
            password = message.content.strip()
            count = check_password(password)
            shaPassword = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            if count:
                embed = discord.Embed(title="**:warning: Password Leaked**", description="**The password associated with the following hash has been compromised and is no longer valid for use**.", color=discord.Color.red()) 
                # embed.add_field(name="Password", value=f"**`{password}`**", inline=False)
                embed.set_image(url="https://media.discordapp.net/attachments/1106911003121291295/1106941835684872292/leaked.png")
                embed.add_field(name="🗝️ **Hash:**", value=f"**`{shaPassword}`**", inline=False)
                embed.add_field(name=f"🌡️ **And it has been leaked:** ***{format(count, ',')}*** **times!**", value="", inline=False)
                embed.add_field(name="**\n❓ What Should i do?**", value="**There are** a few things you should do to protect yourself. \n\n**First**, never use that password again. \n\n**Second**, if you've used that password before, change it immediately. \n\n**Finally**, consider enabling two-factor authentication on your accounts for extra security.", inline=False)
                embed.add_field(name="🧠 Remember:", value="If you DM me the word `generate`, I will create a strong, secure, and safe-to-use password for you 😉")
                embed.set_footer(text="🔌 Powered by haveibeenpwned.com", icon_url="https://cdn.discordapp.com/attachments/1106911003121291295/1106926579013144576/SocialLogo.webp")
                await message.reply(embed=embed)

                Safepassword = generate_password()

                await message.channel.send(f"🔑 Since the password you entered has been leaked, I have generated a new password for you. \n🔒 This new password is **safe**, **secure** and have never been **leaked** before: `{Safepassword}` . \n👍 You may use this password instead of the one you provided.")
            
            
            else: #good password
                embed = discord.Embed(title="**:white_check_mark: Password Safe**", description="**The password associated with the following hash has not been compromised and is safe for use**.", color=discord.Color.green())
                embed.set_image(url="https://media.discordapp.net/attachments/1106911003121291295/1106941835332558908/good.png")
                embed.add_field(name="🗝️ **Hash:**", value=f"**`{shaPassword}`**", inline=False)
                embed.add_field(name="💡 Tips to keep your password safe:", value=f"{tip()}", inline=False)
                embed.add_field(name="🧠 Remember:", value="If you send me a DM with the word `generate`, I will create a strong, secure, and safe-to-use password for you 😉")
                embed.set_footer(text="🔌 Powered by haveibeenpwned.com", icon_url="https://cdn.discordapp.com/attachments/1106911003121291295/1106926579013144576/SocialLogo.webp")
                await message.reply(embed=embed)



client.run(token)