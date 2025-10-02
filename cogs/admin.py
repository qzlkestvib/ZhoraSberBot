# админские команды
# админские команды
from discord.ext import commands
import discord

@bot.command(name="сбор_дота")
@commands.has_permissions(administrator=True)
async def general_call(ctx):
    """Пингует каждого с ролью 'явный игрок в доту'"""
    role_name = "явный игрок в доту"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"⚠️ Роль '{role_name}' не найдена!")
        return

    # Собираем список участников с этой ролью
    members = [member.mention for member in ctx.guild.members if role in member.roles]

    if not members:
        await ctx.send("❌ Никого с этой ролью нет на сервере.")
        return

    # Склеиваем упоминания в одно сообщение
    mentions = " ".join(members)

    await ctx.send(f"📢 **Общий сбор!**\n{mentions}")
