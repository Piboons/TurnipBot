import discord
from discord.ext import commands
import gspread
from gspread.utils import rowcol_to_a1

bot = commands.Bot(command_prefix='!')

clientG = gspread.service_account("secret_client.json")
calcNavet = clientG.open("le navé!!!").sheet1

listeDates = {"lunm":"Lun. matin", "luna": "Lun. aprem", "marm":"Mar. matin", "mara": "Mar. aprem", "merm":"Mer. matin", "mera": "Mer. aprem","jeum":"Jeu. matin", "jeua": "Jeu. aprem", "venm":"Ven. matin", "vena": "Ven. aprem", "samm":"Sam. matin", "sama": "Sam. aprem", "dim":"Prix navet"}

def verifPrix(prix=""):
    try:
        if int(prix) <0:
            int("a")
        else:
            return True
    except:
        return False

def lireJoueurs():
    lsJoueurs = calcNavet.row_values(1, value_render_option="UNFORMATTED_VALUE")
    lsJoueurs = [joueur.lower() for joueur in lsJoueurs]
    return lsJoueurs

@bot.event
async def on_ready():
    print("c bon")

@bot.command()
async def lire(ctx, date="", joueur=""):
    listeJoueurs = lireJoueurs()
    if joueur != "":
        if date.lower() in listeDates and joueur.lower() in listeJoueurs:
            ligne = calcNavet.find(listeDates.get(date.lower())).row
            colonne = calcNavet.find(joueur.capitalize()).col
            valeur = str(calcNavet.cell(ligne, colonne, "UNFORMATTED_VALUE").value)
            if valeur != "":
                await ctx.send(listeDates.get(date.lower())+ ": " + valeur + " clochettes le navet chez "+ joueur.capitalize())
            else:
                await ctx.send("Non renseigné (ono)")
        else:
            await ctx.send("tié fada mino?? date ou nom de joueur invalide, !aide pour plus de détails sur la syntaxe")
    else:
        if date.lower() in listeDates:
            ligne = calcNavet.find(listeDates.get(date)).row
            valeurs = calcNavet.row_values(ligne, value_render_option="UNFORMATTED_VALUE")
            del valeurs[0]
            i = 1
            for val in valeurs:
                if val != "":
                    await ctx.send(listeJoueurs[i].capitalize() + ": " + str(val))
                i+=1
            await ctx.send("voala")

@bot.command()
async def ajouter(ctx, date="", joueur="", prix=""):
    listeJoueurs = lireJoueurs()
    if date.lower() in listeDates and joueur.lower() in listeJoueurs and verifPrix(prix):
        ligne = calcNavet.find(listeDates.get(date.lower())).row
        colonne = calcNavet.find(joueur.capitalize()).col
        calcNavet.update(rowcol_to_a1(ligne, colonne), prix)
        await ctx.send("c bon!!")
    else:
        await ctx.send("ola fraté tia serré?? date, nom de joueur ou prix invalide go !aide pour plus de détails sur la syntaxe")

@bot.command()
async def dates(ctx):
    retour = ""
    for raccourci in listeDates.keys():
        retour += str(listeDates.get(raccourci) + ": " + raccourci + "\n")
    await ctx.send(retour)

@bot.command()
async def joueurs(ctx):
    retour=""
    lsJoueurs = calcNavet.row_values(1, value_render_option="UNFORMATTED_VALUE")
    for joueur in lsJoueurs:
        retour += str(joueur + "\n")
    await ctx.send(retour)

@bot.command()
async def aide(ctx, commande=""):
    if commande=="":
        await ctx.send("cc! bi1venu dan l'aide!! Pour obtenir de l'aide sur une commande, !aide + le nom de la commande (lire, ajouter)")
    elif commande == "lire":
        await ctx.send("Deux options possibles pour cette commande:\n*obtenir les prix pour une date donnée\nSyntaxe: !lire <date>\n*obtenir les prix pour une date et un joueur donnés\nSyntaxe: !lire <date> <joueur>\n\nAttention: les dates et joueurs doivent faire partie des listes !dates et !joueurs")
    elif commande == "ajouter":
        await ctx.send("Syntaxe: !ajouter <date> <joueur> <prix>\nAttention: les dates et joueurs doivent faire partie des listes !dates et !joueurs, et les prix doivent être valides")

discordToken = open("secret_discord.txt", "r")
bot.run(discordToken.read())