import discord
from discord.ext import commands

ANK = commands.Bot(command_prefix='/')

@ANK.event
async def on_ready():
    await ANK.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="ANKARA"))
    print(f'{ANK.user.name} - ONLINE')

async def x(ctx, title, description, image_url=None):
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    if image_url:
        embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@ANK.command()
@commands.has_permissions(administrator=True)
async def aide(ctx):
    message = ("Salut c'est ANKARA ! Voici mes commandes :\n"
               "/nuke - Supprime tous les salons\n"
               "/ban [member] [reason] - Banni un membre\n"
               "/unban [member] - Débanni un membre\n"
               "/warn [member] [reason] - Avertir un membre\n"
               "/aide - Affiche cette aide\n"
               "/textall [message] - Envoie un message dans tous les salons\n"
               "/kick [member] [reason] - Expulse un membre\n"
               "/mute [member] [reason] - Réduit au silence un membre\n"
               "/unmute [member] - Restaure la parole d'un membre\n"
               "/poll [question] - Crée un sondage\n"
               "/announce [message] - Fait une annonce avec @everyone\n"
               "/clear [number] - Efface un nombre spécifique de messages\n"
               "/ping - Vérifie la latence du bot\n"
               "/addrole [member] [role] - Ajoute un rôle à un membre\n"
               "/removerole [member] [role] - Retire un rôle d'un membre\n"
               "/roleinfo [role] - Affiche des informations sur un rôle\n"
               "/userinfo [member] - Affiche des informations sur un utilisateur\n")
    await x(ctx, "Commandes disponibles", message)

@ANK.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    guild = ctx.guild
    channels = guild.text_channels
    for channel in channels:
        await channel.delete()
    await x(ctx, "Nuke Effectué", "Tous les salons ont été effacés...")

@ANK.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await x(ctx, "Membre Banni", f'{member} a été banni par ANKARA ! Raison : {reason}')

@ANK.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: discord.User):
    await ctx.guild.unban(member)
    await x(ctx, "Membre Débanni", f'Le membre {member.mention} a été débanni par ANKARA !')

@ANK.command()
@commands.has_permissions(manage_roles=True)
async def warn(ctx, member: discord.Member, *, reason):
    await x(ctx, "Avertissement", f'{member} a été averti par ANKARA pour : {reason}')

@ANK.command()
@commands.has_permissions(administrator=True)
async def textall(ctx, *, message: str):
    for channel in ctx.guild.text_channels:
        await channel.send(message)

@ANK.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await x(ctx, "Membre Expulsé", f'{member} a été expulsé par ANKARA ! Raison : {reason}')

@ANK.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)
    await member.add_roles(mute_role, reason=reason)
    await x(ctx, "Membre Réduit au Silence", f'{member} a été réduit au silence par ANKARA ! Raison : {reason}')

@ANK.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mute_role)
    await x(ctx, "Membre Réactivé", f'{member} a retrouvé sa voix grâce à ANKARA !')

@ANK.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Sondage", description=question, color=discord.Color.green())
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

@ANK.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message: str):
    await x(ctx, "Annonce", f'@everyone {message}')

@ANK.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await x(ctx, "Messages Effacés", f'{amount} messages ont été supprimés par ANKARA !')

@ANK.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await x(ctx, "Rôle Ajouté", f'Le rôle {role.name} a été ajouté à {member.name} par ANKARA !')

@ANK.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await x(ctx, "Rôle Retiré", f'Le rôle {role.name} a été retiré à {member.name} par ANKARA !')

@ANK.command()
async def roleinfo(ctx, *, role: discord.Role):
    embed = discord.Embed(title="Informations sur le Rôle", color=discord.Color.purple())
    embed.add_field(name="Nom", value=role.name, inline=False)
    embed.add_field(name="ID", value=role.id, inline=False)
    embed.add_field(name="Couleur", value=str(role.color), inline=False)
    embed.add_field(name="Mention", value=role.mention, inline=False)
    embed.add_field(name="Position", value=role.position, inline=False)
    embed.add_field(name="Nombre de membres", value=len(role.members), inline=False)
    embed.add_field(name="Créé le", value=role.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    await ctx.send(embed=embed)

@ANK.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="Informations sur l'Utilisateur", color=discord.Color.blue())
    embed.add_field(name="Nom d'utilisateur", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Status", value=member.status, inline=False)
    embed.add_field(name="Rôles", value=', '.join(role.name for role in member.roles if role.name != '@everyone'), inline=False)
    embed.add_field(name="Créé le", value=member.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    embed.add_field(name="Rejoint le", value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    await ctx.send(embed=embed)

ANK.run('')
