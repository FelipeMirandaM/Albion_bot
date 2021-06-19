import asyncio
from configparser import ConfigParser
import discord
from discord.ext import commands, tasks
from discord.utils import get
import CargarMiembros
from Funciones import Util
from Funciones import VerificarMiembro
import pandas as pd
from datetime import datetime, timedelta

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "D!", intents = intents, case_insensitive=True)
config_object = ConfigParser()
config_object.read("config.ini")
botConfig = config_object["BOTCONFIG"]

first_run = True
def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()



@client.command()
@commands.dm_only()
async def viewadv(ctx):
    war_list = Util.get_active_war(ctx.author.id)
    if war_list:
        for war in war_list:
            embed = discord.Embed(
                title = 'Advertencia',
                colour = discord.Colour.red()

            )
            embed.add_field(name= 'razon: ', value=war[3], inline=True)
            embed.add_field(name= 'termina el dia: ', value=war[4], inline=True)
            await ctx.send(embed=embed)
    else:
        await ctx.send("No tienes advertencias activas")

@commands.is_owner()
@client.command()
async def FullCheck(ctx):
    members = ctx.message.guild.members
    rol = ctx.message.guild.get_role(628015708009398308)
    Util.full_check(members,rol)

@commands.is_owner()
@client.command()
async def cta(ctx):
    chat_excepts = [752348797119496235, 752348798411604053]
    if not is_connected(ctx):
        await ctx.send("Voy")
        channels = (c for c in ctx.message.guild.channels if c.type == discord.ChannelType.voice)
        for channel in channels:

            if len(channel.members) > 0 and channel.id not in chat_excepts:
                print("Entrando a" + channel.name)
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio('cta.ogg'))
                await asyncio.sleep(3)
                await vc.disconnect(force=True)
        await ctx.send("Termine")
    else:
        await ctx.send("Ya estoy trabajando")


@client.command()
async def adv(ctx, args, *, args2):
    if ctx.channel.id == 832841655987208233:
        await ctx.message.delete()
        error = False
        photo = ""
        if len(ctx.message.attachments) > 0:
            photo = ctx.message.attachments[0].url
        character_name = args
        reason = args2
        offender_info = Util.search_personaje(character_name)
        creator_info = Util.search_user(ctx.author.id)
        ment = ctx.message.author.mention
        if len(offender_info) == 0:
            error = True
            await ctx.send(f"{ment} " + "El personaje no existe o no esta registrado", delete_after=10)
        if len(creator_info) == 0:
            error = True
            await ctx.send(f"{ment} " + "No estas registrado", delete_after=10)

        if not error:
            ment_offender = await ctx.message.guild.fetch_member(offender_info[0][3])
            embed = discord.Embed(
                title = 'Advertencia de '+ character_name,
                colour = discord.Colour.red()
            )

            embed.add_field(name= 'Infractor: ', value=f"{ment_offender.mention}", inline=True)
            embed.add_field(name= 'razon: ', value=reason, inline=True)
            today = datetime.now() + timedelta(30)
            embed.add_field(name= 'termina el dia: ', value=str(today), inline=True)

            await ctx.send(embed= embed, delete_after=45)

            msg = await ctx.send('Para confirmar reacciona con ✅', delete_after=45)
            await msg.add_reaction('✅')

            def check(reaction, user):
                return reaction.message == msg and str(reaction.emoji) == '✅' and user == ctx.author

            await client.wait_for('reaction_add', check=check, timeout=45)

            if len(ctx.message.attachments) > 0:
                photo = ctx.message.attachments[0].url
            print(Util.add_warning(offender_info[0][0], creator_info[0][0], photo, reason))
            dm_channel = await ment_offender.create_dm()

            await dm_channel.send(embed = embed)
            await ctx.send("Advertencia agregada", delete_after=45)

            channel = client.get_channel(684133033158377499)

            embed = discord.Embed(
                title = 'Advertencia de '+ character_name,
                colour = discord.Colour.red()
            )
            embed.add_field(name= 'Infractor: ', value=f"{ment_offender.mention}", inline=True)
            embed.add_field(name= 'Razon: ', value=reason, inline=True)
            embed.add_field(name= 'Creador: ', value=f"{ctx.message.author.mention}", inline=True)
            today = datetime.now() + timedelta(30)
            embed.add_field(name= 'termina el dia: ', value=str(today), inline=False)
            if photo != "":
                embed.set_image(url=photo)
            await channel.send(embed=embed)

@client.command()
async def RegCta(ctx, arg):
    if ctx.channel.id == 830529578681368627:
        channel_main = client.get_channel(822698145662107688)
        channel_alter = client.get_channel(809151729269473331)
        list_main = channel_main.members
        list_alter = channel_alter.members
        list_total = [list_main, list_alter]
        ment = ctx.message.author.mention
        info = Util.reg_cta(list_total, arg, ctx.message.author.id)
        if len(info) != 2:
            await ctx.send(f"{ment} " + info)
        else:
            await ctx.send(f"{ment} \n "+info[0])
            if info[1] != "======Discord con problemas=======\n=====end=====":
                await ctx.send(f"{ment} \n "+info[1])
        await ctx.message.delete()

@client.event
async def on_ready():
   global first_run
   if first_run:
        VerificarMiembros.start()
        first_run = False
        print(first_run)
   print('We have logged in as {0.user}'.format(client))


@client.command()
async def hi(ctx):
    embed = discord.Embed(
        title = 'Bienvenido a :imp: I DOOM I :imp:',
        description = 'Somos un gremio que vive en la zona de martlock y estamos principalmente enfocados en el contenido competitivo y el gazor se la come.',
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url= "https://i.imgur.com/vkTuSE7.png")
    embed.add_field(name='Requisitos: ', value = '-10m de fama PVP \n -Uso de discord \n PC adecuado para ZvZ masiva', inline= True)
    embed.add_field(name='Ofrecemos: ', value = '-Hideous en Zonas T5-T8 \n -Contenido PVP \n -Contenido de cristal', inline= True)
    embed.set_image(url= "https://i.imgur.com/vkTuSE7.png")
    await ctx.send(embed= embed)


@client.command()
async def Registrar(ctx, arg):
    usuario = str(ctx.message.author.id)
    ment = ctx.message.author.mention
    Personaje = str(arg)
    Respuesta = Util.agregar_usuario(usuario, Personaje.lower())
    #await asignar_rol(ctx.message.author, Personaje.lower())
    await ctx.send(f"{ment} " + Respuesta)


@client.command()
async def RegistrarAlter(ctx, arg):
    usuario = str(ctx.message.author.id)
    Personaje = str(arg)
    ment = ctx.message.author.mention
    Respuesta = Util.agregar_alter(usuario, Personaje.lower())
    await ctx.send(f"{ment} " + Respuesta)


@client.command()
@commands.is_owner()
async def SinRegistrar(ctx):
    Lista = Util.get_personajes_sin_registrar()
    String = "====PERSONAJES SIN REGISTRAR====\n"
    for Miembro in Lista:
        String = String + Miembro + "\n"
    String = String + "Total: " + str(len(Lista)) + "\n" + "====end===="
    await ctx.send(String)


@client.command()
@commands.is_owner()
async def AvisarSinRegistrar(ctx):
    Miembros = ctx.message.guild.members
    Send = "===Discord Sin Registrar===\n"
    rol = ctx.message.guild.get_role(628015708009398308)
    count = 0
    for Miembro in Miembros:
        if rol in Miembro.roles:
            if len(Util.search_user(Miembro.id)) == 0:
                if Util.is_white_list(Miembro.id):
                    ment = Miembro.mention
                    Send = Send + f"{ment} " + "\n"
                    count = count + 1

            if count > 49:
                await ctx.send(Send)
                count = 0
                Send = ""
    Send = Send + "===end==="
    await ctx.send(Send)


@client.command()
async def hora(ctx):
    await ctx.message.delete()
    hora = datetime.utcnow()
    if hora.minute<10:
        await ctx.send("Son las "+str(hora.hour)+":0"+str(hora.minute),  delete_after=10)
    else:
        await ctx.send("Son las "+str(hora.hour)+":"+str(hora.minute),  delete_after=10)

# @client.command()
# @commands.is_owner()
# async def clean_discord(ctx):
#
#     member_list = ctx.message.guild.members
#     rol = ctx.message.guild.get_role(818633494967484416)
#     guild = client.get_guild(817934118906101851)
#     bot = 741755164867821659
#     if guild == ctx.message.guild:
#
#         for member in member_list:
#             if member.id != bot:
#                 member_info = Util.search_user(member.id)
#                 if rol not in member.roles:
#                     if len(member_info) > 0:
#                         if VerificarMiembro.search_name(member_info[0][1].lower()) == 0:
#                             await ctx.message.guild.kick(member, "no reason")
#                     else:
#                         await ctx.message.guild.kick(member, "no reason")


@client.command()
@commands.is_owner()
async def test(ctx):
    channel = client.get_channel(818175543887134740)
    messages = await channel.history(limit = 1000).flatten()
    data_load = []
    for i in messages:
        if len(i.embeds) >= 1:
            id = i.embeds[0].fields[0].value
            open_id = i.embeds[0].fields[1].value.replace("<","").replace(">","").replace("@","")
            close_id = i.embeds[0].fields[2].value.replace("<","").replace(">","").replace("@","")
            reason = i.embeds[0].fields[3].value
            open_date = str(pd.to_datetime(pd.Series(i.embeds[0].fields[5].value.replace(" (UTC)","")))[0])
            close_date = str(pd.to_datetime(pd.Series(i.embeds[0].footer.text.replace("Close Time: ", "").replace(" (UTC)", "")))[0])

            data = (id, open_id, close_id, open_date, close_date, 0, reason, 1)
            data_load.append(data)

    Util.temp_load(data_load)

@tasks.loop(seconds=1200)
async def VerificarMiembros():
    Util.update_active()
    print("Cargando Miembros")
    if await CargarMiembros.load_members():
        print("Miembros Cargados")
        guild = client.get_guild(339124223635226625)
        channel = client.get_channel(821966789037654047)
        rol = get(guild.roles, id=628015708009398308)
        Miembros = guild.members
        kick = False
        Lista_Display_Name = "===Miembros a kickear===\n"
        for Miembro in Miembros:
            id = Miembro.id
            Informacion = Util.search_user(id)
            if len(Informacion) > 0 and (rol in Miembro.roles):
                Nombre_Personaje = Informacion[0][1]
                Buscar = VerificarMiembro.search_name(Nombre_Personaje.lower())
                if Buscar is 0:
                    kick = True
                    Lista_Display_Name = Lista_Display_Name + f"{Miembro.mention} " + "\n "
                    ##await eliminar_roles(Miembro)
                    ##Util.actualizar_estado(id,0)
        if kick:
            Lista_Display_Name = Lista_Display_Name + "===end==="
            await channel.send(Lista_Display_Name)

        print("Miembros Verificados")
        #Util.load_fame_history()
        #print("Fama cargada")




@VerificarMiembros.before_loop
async def before_VerificarMiembros():
    await client.wait_until_ready()


@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Handles command errors"""
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Comando no valido")
        return





































client.run(botConfig['token'])
