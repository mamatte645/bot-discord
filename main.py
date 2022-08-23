credits="""



      
ADD ME ON DISCORD  Tokyru_#0001 BOT PRINCIPALE
OU REJOIGNEZ LE SERVEUR DISCORD https://discord.gg/ZPXrpjUJkC
SI VOUS VOULEZ UN MEILLEUR BOT, NOUS POUVONS VOUS LE FOURNIR. CECI EST GRATUIT ET PEU DE TRAVAIL Y A ETE MIS
"""







#ACCOUNT FILE NAMES NEED TO BE LOWERCASED
print(credits)
import discord,json,os,random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

with open("config.json") as file: # Load the config file
    info = json.load(file)
    token = info["token"]
    delete = info["autodelete"]
    prefix = info["prefix"]

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("[+] Bot Running!")
@bot.command() # Stock command
async def stock(ctx):
    stockmenu = discord.Embed(title="Account Stock",description="") # Define the embed
    for filename in os.listdir("Accounts"):
        with open("Accounts//"+filename) as f: # Open every file in the accounts folder
            ammount = len(f.read().splitlines()) # Get the ammount of lines
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") #Make the name look nice
            stockmenu.description += f"*{name}* - {ammount}\n" # Add to the embed
    await ctx.send(embed=stockmenu) # Send the embed


@bot.command() #Gen command
async def gen(ctx,name=None):
    if name == None:
        await ctx.send("Spécifiez le compte que vous souhaitez!") # Say error if no name specified
    else:
        name = name.lower()+".txt" #Add the .txt ext
        if name not in os.listdir("Accounts"): # If the name not in the directory
            await ctx.send(f"Le compte n'existe pas. Veuillez utiliser la commande : `{prefix}stock`")
        else:
            with open("Accounts//"+name) as file:
                lines = file.read().splitlines() #Read the lines in the file
            if len(lines) == 0: # If the file is empty
                await ctx.send("Ces comptes sont en rupture de stock") #Send error if lines = 0
            else:
                with open("Accounts//"+name) as file:
                    account = random.choice(lines) # Get a random line
                try: #Try to send the account to the sender
                    await ctx.author.send(f"`{str(account)}`\n\nCe message sera pas supprimé dans 0 secondes!",delete_after=delete)
                except: # If it failed send a message in the chat
                    await ctx.send("Échec de l'envoi ! Activez vos messages directs")
                else: # If it sent the account, say so then remove the account from the file
                    await ctx.send("Envois du compte dans vos MP")
                    with open("Accounts//"+name,"w") as file:
                        file.write("") #Clear the file
                    with open("Accounts//"+name,"a") as file:
                        for line in lines: #Add the lines back
                            if line != account: #Dont add the account back to the file
                                file.write(line+"\n") # Add other lines to file

bot.remove_command('help')

@bot.command() #command
async def help(ctx):
    embed=discord.Embed(
        title="Page d'aide 1/1",
        description="Vous trouverez ici toutes les commandes du bot !",
        color=0x0AAB1D
    )
    embed.add_field(
        name="Pour gen des comptes",
        value="Faites : .gen <lenomdugen>",
    )
    embed.add_field(
        name="Pour voir le stock des comptes",
        value="Faites : .stock"
    )
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.guild:  # If message in guild
            await bot.process_commands(message)  # Process command
        else:
            return await message.author.send("Desole, mais je ne traite pas les commandes sur les messages directs...")

bot.run(token)
