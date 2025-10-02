import discord
from discord.ext import commands
import json
import re
import requests

STEAM_JSON = "steam_ids.json"

def load_steam_ids():
    try:
        with open(STEAM_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_steam_id(discord_id, opendota_id):
    data = load_steam_ids()
    data[str(discord_id)] = opendota_id
    with open(STEAM_JSON, "w") as f:
        json.dump(data, f, indent=4)

# Преобразование vanity URL или прямой ссылки в SteamID64
def get_steam_id64(url):
    match = re.search(r"(https?://)?steamcommunity\.com/(id|profiles)/([\w\d]+)", url)
    if not match:
        return None
    kind, identifier = match.group(2), match.group(3)
    if kind == "profiles":
        return identifier  # 64-bit
    else:
        api_key = "A163E5FFDF2172D65008D8AAED2F8261"
        r = requests.get(
            "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/",
            params={"key": api_key, "vanityurl": identifier}
        ).json()
        if r.get("response", {}).get("success") == 1:
            return r["response"]["steamid"]
        return None

# Конвертируем SteamID64 в OpenDota account_id
def steam64_to_opendota_id(steam64):
    return int(steam64) - 76561197960265728

def setup(bot):
    @bot.command(name="стим")
    async def register_steam(ctx):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("❌ Отправьте команду мне в личные сообщения.")
            return

        steam_ids = load_steam_ids()
        if str(ctx.author.id) in steam_ids:
            await ctx.send(f"⚠ Вы уже зарегистрировали Steam ID")
            return

        await ctx.send(f"Привет, {ctx.author.display_name}! Отправь ссылку на свой Steam-профиль.")

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        try:
            msg = await bot.wait_for("message", check=check, timeout=300)
            steam64 = get_steam_id64(msg.content.strip())
            if not steam64:
                await ctx.send("❌ Не удалось распознать ссылку на Steam. Попробуйте ещё раз.")
                return

            opendota_id = steam64_to_opendota_id(steam64)
            save_steam_id(ctx.author.id, opendota_id)

            await ctx.send(f"✅ Steam ID успешно сохранён для OpenDota")

        except Exception as e:
            await ctx.send(f"❌ Произошла ошибка: {e}")
