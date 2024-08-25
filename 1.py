import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer
import os

# Задайте ваш сервер и токен бота
CHANNEL_ID = 1277366025704313014
SERVER_NAME = "VainLand"  # Имя сервера, которое будет отображаться в заголовке

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

message_id = None  # Переменная для хранения ID сообщения

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен и готов к работе!')
    update_server_status.start()  # Запускаем цикл отслеживания статуса сервера

@tasks.loop(seconds=60)
async def update_server_status():
    global message_id  # Указываем, что используем глобальную переменную

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Канал с ID {CHANNEL_ID} не найден.")
        return

    try:
        server = JavaServer.lookup("188.127.241.208:25687")
        status = server.status()
        player_count = status.players.online
        max_players = status.players.max
        player_names = ", ".join([player.name for player in status.players.sample]) if status.players.sample else "Нет игроков"

        embed = discord.Embed(title=f"Состояние сервера {SERVER_NAME}", color=discord.Color.green())
        embed.add_field(name="Статус", value="Онлайн", inline=False)
        embed.add_field(name="Игроки", value=f"{player_count}/{max_players}", inline=False)
        embed.add_field(name="Список игроков", value=player_names, inline=False)
    except Exception:
        embed = discord.Embed(title=f"Состояние сервера {SERVER_NAME}", color=discord.Color.red())
        embed.add_field(name="Статус", value="Офлайн", inline=False)

    if message_id is None:  # Если сообщение еще не отправлено
        message = await channel.send(embed=embed)
        message_id = message.id  # Сохраняем ID сообщения
    else:
        try:
            message = await channel.fetch_message(message_id)  # Получаем сообщение по ID
            await message.edit(embed=embed)  # Редактируем сообщение
        except discord.NotFound:  # Если сообщение не найдено (возможно было удалено)
            message = await channel.send(embed=embed)
            message_id = message.id  # Сохраняем новый ID сообщения

bot.run("MTI3NDM5MTgwNjM3MjQ3OTA3MA.Gut_nb.ni4pajzO03nF-w4mHCRp2eiRjEmgEpewaE3GhE")
