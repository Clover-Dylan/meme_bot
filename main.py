import discord
from discord.ext import commands
import random
import asyncio
import json
import os
import threading
from datetime import datetime
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

memes = [
    'images/mem1.jpg','images/mem2.jpg','images/mem3.jpg','images/mem4.png',
    'images/mem5.png','images/mem6.jpg','images/mem7.mp4','images/mem8.jpg',
    'images/mem9.png','images/mem10.png','images/mem11.png','images/mem12.jpg',
    'images/mem13.jpg','images/mem14.jpg','images/mem15.jpg','images/mem16.jpg',
    'images/mem17.mp4'
]

# 🎯 CONFIG
USUARIO_OBJETIVO = 753318525145317457

CANALES_PERMITIDOS = [
    1371672165161635943,
    1202068322339000402,
    1476747432288190526
]

ROLES_AUTORIZADOS = [
    "Admin",
    "Staff",
    "Moderador",
    "Master chief",
    "【👨‍💻​】Admin【💎​】",
    "Bot creator"
]

bot_activo = True
modo = "chill"
CANAL_CONSOLA = CANALES_PERMITIDOS[0]

# 🎂 JSON SEGURO
if os.path.exists("cumples.json"):
    try:
        with open("cumples.json", "r") as f:
            contenido = f.read().strip()
            cumpleanos = json.loads(contenido) if contenido else {}
    except:
        print("⚠️ JSON corrupto, reiniciando")
        cumpleanos = {}
else:
    cumpleanos = {}

def guardar_cumples():
    with open("cumples.json", "w") as f:
        json.dump(cumpleanos, f, indent=4)

#  PERSONALIDAD
personalidades = {
    "yandere": ["solo tú puedes hablar conmigo... "],
    "toxico": ["bro... eso fue lo más tonto que leí hoy "],
    "chill": ["todo chill "],
    "troll": ["??? bro qué "],
    "serio": ["Entiendo."]
}

def generar_respuesta():
    return random.choice(personalidades[modo])

def es_admin(member):
    return any(role.name in ROLES_AUTORIZADOS for role in member.roles)

# 📁 MEMES TEXTO
memes_texto = {
    "laburo": "images/laburo.webp",
    "mahito": "images/mahito.mp4",
    "manco": "images/manco.mp4",
    "daniel": "images/daniel.mp4",
    "control": "images/makima.jpg",
    "laburo": "images/laburo.webp",
    "trabajo": "images/laburo.webp",
    "celos": "images/celos.mp4",
    "caine": "images/caine.mp4",
    "buena música": "images/buena_musica.mp4",
    "secuestro": "images/Danganronpa-jpg",
    "futuro": "images/futuro.jpg",
    "hitler": "images/hitler.mp4",
    "de hecho": "images/dehecho.jpg",
    "pene": "images/losuponia.webp",
}

# 🎉 CUMPLEAÑOS
async def revisar_cumpleanos():
    await bot.wait_until_ready()

    while not bot.is_closed():
        hoy = datetime.now().strftime("%m-%d")

        if hoy in cumpleanos:
            menciones = " ".join([f"<@{uid}>" for uid in cumpleanos[hoy]])

            for canal_id in CANALES_PERMITIDOS:
                canal = bot.get_channel(canal_id)
                if canal:
                    await canal.send(f"🎉 Feliz cumpleaños {menciones} 🎂")

            await asyncio.sleep(86400)
        else:
            await asyncio.sleep(60)

# 🤖 READY
@bot.event
async def on_ready():
    print(f'Bot listo como {bot.user}')
    bot.loop.create_task(revisar_cumpleanos())

# 🎂 COMANDOS

@bot.command()
async def meme(ctx, numero: int = None):
    # 🔒 solo canales permitidos
    if ctx.channel.id not in CANALES_PERMITIDOS:
        return
    try:
        # 🎯 meme específico
        if numero is not None:
            if numero < 1 or numero > len(memes):
                await ctx.send(f"❌ Usa un número del 1 al {len(memes)}")
                return

            ruta = memes[numero - 1]

        # 🎲 meme random
        else:
            ruta = random.choice(memes)

        with open(ruta, "rb") as f:
            await ctx.send(file=discord.File(f))

    except FileNotFoundError:
        await ctx.send("❌ Archivo no encontrado")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def info(ctx):
    mensaje = """
📜 **COMANDOS DEL BOT**

🧠 $meme
→ Envía un meme random

🧠 $meme 1-17
→ Envía un meme del 1 al 17

🧠 $modo [modo]
→ Cambia la personalidad
(yandere, chill, toxico, troll, serio) [solo admins]

🎂 $cumple @user MM-DD
→ Guarda cumpleaños

❌ $cumple_eliminar @user
→ Elimina cumpleaños

🔴 para
→ Apaga el bot (solo admins)

🟢 prende
→ Prende el bot (solo admins)

📜 $info
→ Muestra este mensaje
"""

    await ctx.send(mensaje)

@bot.command()
async def cumple(ctx, usuario: discord.Member = None, fecha: str = None):

    # 🔒 solo canales permitidos
    if ctx.channel.id not in CANALES_PERMITIDOS:
        return

    # 📜 VER LISTA
    if usuario is None and fecha is None:

        if not cumpleanos:
            await ctx.send("📭 No hay cumpleaños guardados")
            return

        mensaje = "🎂 **Lista de cumpleaños:**\n"

        for fecha_cumple, usuarios in cumpleanos.items():
            menciones = " ".join([f"<@{uid}>" for uid in usuarios])
            mensaje += f"\n📅 {fecha_cumple} → {menciones}"

        await ctx.send(mensaje)
        return

    # ⚠️ VALIDACIÓN
    if usuario is None or fecha is None:
        await ctx.send("Uso: $cumple @user MM-DD")
        return

    # 📅 VALIDAR FECHA
    try:
        datetime.strptime(fecha, "%m-%d")
    except:
        await ctx.send("Formato MM-DD")
        return

    # 💾 GUARDAR
    if fecha not in cumpleanos:
        cumpleanos[fecha] = []

    if usuario.id in cumpleanos[fecha]:
        await ctx.send("Ya existe 😅")
        return

    cumpleanos[fecha].append(usuario.id)
    guardar_cumples()

    await ctx.send(f"🎂 Guardado {usuario.mention}")

@bot.command()
async def cumple_eliminar(ctx, usuario: discord.Member):
    eliminado = False

    for fecha in list(cumpleanos.keys()):
        if usuario.id in cumpleanos[fecha] and es_admin(ctx.author):
            cumpleanos[fecha].remove(usuario.id)
            if not cumpleanos[fecha]:
                del cumpleanos[fecha]
            eliminado = True

    guardar_cumples()
    await ctx.send("❌ Eliminado" if eliminado else "No estaba")

@bot.command()
async def modo(ctx, nuevo_modo: str):
    global modo

    if not es_admin(ctx.author):
        await ctx.send("🚫 No permiso")
        return

    if nuevo_modo not in personalidades:
        await ctx.send("Modos: " + ", ".join(personalidades.keys()))
        return

    modo = nuevo_modo
    await ctx.send(f"🧠 modo {modo}")

# 💬 MENSAJES
@bot.event
async def on_message(message):
    global bot_activo

    if message.author.bot:
        return

    if message.channel.id not in CANALES_PERMITIDOS:
        return

    contenido = message.content.lower().strip()

    # 🔒 prender/apagar
    if contenido == "para":
        if not es_admin(message.author):
            await message.channel.send("🚫 No permiso")
            return
        bot_activo = False
        await message.channel.send("💀 apagado")
        return

    if contenido == "prende":
        if not es_admin(message.author):
            await message.channel.send("🚫 No permiso")
            return
        bot_activo = True
        await message.channel.send("🔥 prendido")
        return

    if not bot_activo:
        return

    # 🎯 mención específica
    if any(user.id == USUARIO_OBJETIVO for user in message.mentions):
        with open("images/video.mp4", "rb") as f:
            await message.channel.send(file=discord.File(f))
        return

    await bot.process_commands(message)

    # 📁 memes
    for palabra, ruta in memes_texto.items():
        if palabra in contenido:
            with open(ruta, "rb") as f:
                await message.channel.send(file=discord.File(f))
            return

    # 🧠 IA (solo si lo mencionan)
    if bot.user in message.mentions:
        await message.channel.send(generar_respuesta())

# 💻 CONSOLA
def consola():
    while True:
        msg = input(">>> ")
        asyncio.run_coroutine_threadsafe(enviar(msg), bot.loop)

async def enviar(msg):
    canal = bot.get_channel(CANAL_CONSOLA)
    if canal:
        await canal.send(msg)

threading.Thread(target=consola, daemon=True).start()


# ✅ MAIN LIMPIO

TOKEN = os.getenv("TOKEN")

async def main():
    async with bot:
        threading.Thread(target=consola, daemon=True).start()
        await bot.start(TOKEN)


asyncio.run(main())