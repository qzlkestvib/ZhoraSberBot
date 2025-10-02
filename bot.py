# Системный файл, отсюда запускаешь код.
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import aiohttp
import steam_register
import json
import stats_dota
from steam_id import steam_ids

STEAM_JSON = "steam_ids.json"

def load_steam_ids():
    try:
        with open(STEAM_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


load_dotenv()  # сначала загружаем .env
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

active_matches = {}

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

if TOKEN is None:
    raise ValueError("❌ Токен не найден! Проверьте .env и переменную ZHORA_TOKEN")

# Префикс для команд Жоры
bot = commands.Bot(command_prefix="жора ", intents=discord.Intents.all())
steam_register.setup(bot)

@bot.event
async def on_ready():
    """Обработчик запуска бота"""
    print(f'Бот {bot.user.name} успешно подключился к Discord!')
    await bot.change_presence(activity=discord.Game(name="очке твоей матери"))



# --- Команды (пинг, инфо, команды)
@bot.command(name="команды")
async def show_commands(ctx):
    embed = discord.Embed(
        title="📜 Доступные команды Жоры Сбербанка",
        description="Ниже представлен список команд и их краткое описание:",
        color=0x2391e0
    )

    # --- Основные команды ---
    embed.add_field(name="💡 Основные", value=(
        "`жора команды` — Показать этот список команд\n"
        "`жора пинг` — Проверить задержку бота\n"
        "`жора инфо` — Информация о боте"
    ), inline=False)

    # --- Админские команды ---
    embed.add_field(name="🛡 Админские", value=(
        "`жора сбор_дота` — Пингует всех игроков с ролью 'явный игрок в доту'\n"
        "`жора начать_матч bo1/bo3/bo5` — Начать серию матчей 5x5\n"
        "`жора состав_1 / жора состав_2` — Задать составы команд\n"
        "`жора результат team1/team2` — Отметить победившую команду\n"
        "`жора счет` — Показать текущий счет серии"
    ), inline=False)

    # --- Профили и статистика ---
    embed.add_field(name="📊 Статистика игроков", value=(
        "`жора стим (в личном сообщении с ботом)` — указать стим для работы с командами ниже.\n"
        "`жора профиль @игрок` — Показать профиль игрока с OpenDota\n"
        "`жора топ_ранг` — Топ игроков по рангу\n"
        "`жора топ_вр` — Топ игроков по винрейту\n"
        "`жора сравнить @игрок1 @игрок2` — Сравнение двух игроков"
    ), inline=False)

    embed.set_footer(text="Создан как кент к Гоше Пацану | Управление сервером и играми 5x5")

    await ctx.send(embed=embed)


@bot.command(name="пинг")
async def ping(ctx):
    await ctx.send(f"Задержка: {round(bot.latency * 1000)}ms")

@bot.command(name="инфо")
async def info(ctx):
    embed = discord.Embed(
        title="ℹ️ О Жоре",
        description="Я — Жора Сбербанк, курьер Дамира и кент Гоши Пацана. "
                    "Могу помочь с управлением сервером, проверкой статуса и другими функциями.",
        color=0x34a853
    )
    embed.set_footer(text="Создан как кент к Гоше Пацану")
    await ctx.send(embed=embed)

# --- Админская команда "сбор_дота"
@bot.command(name="сбор_дота")
@commands.has_permissions(administrator=True)
async def general_call(ctx):
    role_name = "явный игрок в доту"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"⚠️ Роль '{role_name}' не найдена!")
        return

    members = [member.mention for member in ctx.guild.members if role in member.roles]
    if not members:
        await ctx.send("❌ Никого с этой ролью нет на сервере.")
        return

    # Отправляем отдельное сообщение для каждого участника
    for mention in members:
        await ctx.send(f"📢 **Общий сбор!** {mention}")



heroes = {
    1: "Anti-Mage",
    2: "Axe",
    3: "Bane",
    4: "Bloodseeker",
    5: "Crystal Maiden",
    6: "Drow Ranger",
    7: "Earthshaker",
    8: "Juggernaut",
    9: "Mirana",
    10: "Morphling",
    11: "Shadow Fiend",
    12: "Phantom Lancer",
    13: "Puck",
    14: "Pudge",
    15: "Razor",
    16: "Sand King",
    17: "Storm Spirit",
    18: "Sven",
    19: "Tiny",
    20: "Vengeful Spirit",
    21: "Windranger",
    22: "Zeus",
    23: "Kunkka",
    25: "Lina",
    26: "Lion",
    27: "Shadow Shaman",
    28: "Slardar",
    29: "Tidehunter",
    30: "Witch Doctor",
    31: "Lich",
    32: "Riki",
    33: "Enigma",
    34: "Tinker",
    35: "Sniper",
    36: "Necrophos",
    37: "Warlock",
    38: "Beastmaster",
    39: "Queen of Pain",
    40: "Venomancer",
    41: "Faceless Void",
    42: "Wraith King",
    43: "Death Prophet",
    44: "Phantom Assassin",
    45: "Pugna",
    46: "Templar Assassin",
    47: "Viper",
    48: "Luna",
    49: "Dragon Knight",
    50: "Dazzle",
    51: "Clockwerk",
    52: "Leshrac",
    53: "Nature's Prophet",
    54: "Lifestealer",
    55: "Dark Seer",
    56: "Clinkz",
    57: "Omniknight",
    58: "Enchantress",
    59: "Huskar",
    60: "Night Stalker",
    61: "Broodmother",
    62: "Bounty Hunter",
    63: "Weaver",
    64: "Jakiro",
    65: "Batrider",
    66: "Chen",
    67: "Spectre",
    68: "Ancient Apparition",
    69: "Doom",
    70: "Ursa",
    71: "Spirit Breaker",
    72: "Gyrocopter",
    73: "Alchemist",
    74: "Invoker",
    75: "Silencer",
    76: "Outworld Devourer",
    77: "Lycan",
    78: "Brewmaster",
    79: "Shadow Demon",
    80: "Lone Druid",
    81: "Chaos Knight",
    82: "Meepo",
    83: "Treant Protector",
    84: "Ogre Magi",
    85: "Undying",
    86: "Rubick",
    87: "Disruptor",
    88: "Nyx Assassin",
    89: "Naga Siren",
    90: "Keeper of the Light",
    91: "Io",
    92: "Visage",
    93: "Slark",
    94: "Medusa",
    95: "Troll Warlord",
    96: "Centaur Warrunner",
    97: "Magnus",
    98: "Timbersaw",
    99: "Bristleback",
    100: "Tusk",
    101: "Skywrath Mage",
    102: "Abaddon",
    103: "Elder Titan",
    104: "Legion Commander",
    105: "Techies",
    106: "Ember Spirit",
    107: "Earth Spirit",
    108: "Underlord",
    109: "Terrorblade",
    110: "Phoenix",
    111: "Oracle",
    112: "Winter Wyvern",
    113: "Arc Warden",
    114: "Monkey King",
    119: "Dark Willow",
    120: "Pangolier",
    121: "Grimstroke",
    123: "Mars",
    126: "Void Spirit",
    128: "Snapfire",
    129: "Hoodwink",
    135: "Dawnbreaker",
    136: "Marci",
    137: "Primal Beast",
    138: "Muerta",
    131: "Ringmaster",
    140: "Kez"
}

@bot.command(name="сравнить")
async def compare_players(ctx, member1: discord.Member, member2: discord.Member):
    try:
        with open("steam_ids.json", "r") as f:
            steam_ids = json.load(f)
    except FileNotFoundError:
        steam_ids = {}

    steam1 = steam_ids.get(str(member1.id))
    steam2 = steam_ids.get(str(member2.id))

    if not steam1 or not steam2:
        await ctx.send("❌ Один из игроков не зарегистрирован в Steam ID.")
        return

    try:
        # Данные профилей
        def get_profile(steam_id):
            data = requests.get(f"https://api.opendota.com/api/players/{steam_id}").json()
            profile = data.get("profile", {})
            nickname = profile.get("personaname", "Неизвестно")
            rank_tier = data.get("rank_tier")
            rank_text = rank_tier_to_text(rank_tier) if rank_tier else "Нет ранга"
            return {"nickname": nickname, "rank": rank_text}

        prof1 = get_profile(steam1)
        prof2 = get_profile(steam2)

        # Винрейт
        wl1 = requests.get(f"https://api.opendota.com/api/players/{steam1}/wl").json()
        wl2 = requests.get(f"https://api.opendota.com/api/players/{steam2}/wl").json()

        winrate1 = round(wl1.get("win", 0) / max(wl1.get("win",0) + wl1.get("lose",0), 1) * 100, 1)
        winrate2 = round(wl2.get("win", 0) / max(wl2.get("win",0) + wl2.get("lose",0), 1) * 100, 1)
        winrate_diff = round(abs(winrate1 - winrate2), 1)

        # Получаем все последние 500 матчей каждого игрока (можно увеличить, но медленнее)
        matches1 = requests.get(f"https://api.opendota.com/api/players/{steam1}/matches?limit=500").json()
        matches2 = requests.get(f"https://api.opendota.com/api/players/{steam2}/matches?limit=500").json()

        # Считаем только матчи, где они были в одной партии (same party)
        matches2_dict = {m["match_id"]: m for m in matches2}
        shared_games = 0
        for m1 in matches1:
            m2 = matches2_dict.get(m1["match_id"])
            if m2 and m1.get("party_size") and m2.get("party_size") and m1["party_size"] == m2["party_size"]:
                shared_games += 1

        # Embed
        embed = discord.Embed(
            title=f"⚔ Сравнение {member1.display_name} и {member2.display_name}",
            color=0x00ffcc
        )

        embed.add_field(name=f"{member1.display_name}", value=f"⭐ Ранг: {prof1['rank']}\n📊 Винрейт: {winrate1}%", inline=True)
        embed.add_field(name=f"{member2.display_name}", value=f"⭐ Ранг: {prof2['rank']}\n📊 Винрейт: {winrate2}%", inline=True)
        embed.add_field(name="Разница в винрейте", value=f"{winrate_diff}%", inline=False)
        embed.add_field(name="Совместные игры", value=str(shared_games), inline=False)

        if winrate1 > winrate2:
            embed.set_footer(text=f"Больше винрейт: {member1.display_name} ✅")
        elif winrate2 > winrate1:
            embed.set_footer(text=f"Больше винрейт: {member2.display_name} ✅")
        else:
            embed.set_footer(text="Винрейт одинаковый ⚖️")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Ошибка при сравнении: {e}")


rank_to_mmr = {
    "Рекрут": [0, 154, 308, 462, 616],
    "Страж": [770, 924, 1078, 1232, 1386],
    "Рыцарь": [1540, 1694, 1848, 2002, 2156],
    "Герой": [2310, 2464, 2618, 2772, 2926],
    "Легенда": [3080, 3234, 3388, 3542, 3696],
    "Властелин": [3850, 4004, 4158, 4312, 4466],
    "Бомжество": [4620, 4820, 5020, 5220, 5420],
    "Титан": ["5620+"]  # Immortal
}

def rank_tier_to_text(rank_tier):
    ranks = {
        1: "Рекрут", 2: "Страж", 3: "Рыцарь",
        4: "Герой", 5: "Легенда", 6: "Властелин", 7: "Бомжество", 8: "Титан"
    }
    if not rank_tier:
        return "Нет ранга", "Неизвестно"

    tier = rank_tier // 10
    stars = rank_tier % 10
    if tier == 8:  # Immortal
        return "Титан", "5620+"

    roman_stars = ["", "I", "II", "III", "IV", "V"]
    rank_name = ranks.get(tier, "Неизвестно")
    mmr_estimate = rank_to_mmr.get(rank_name, ["Неизвестно"])[stars-1] if stars > 0 else "Неизвестно"
    return f"{rank_name} {roman_stars[stars]}", f"~{mmr_estimate}"

@bot.command(name="профиль")
async def dota_profile(ctx, member: discord.Member):
    steam_ids = load_steam_ids()  # читаем актуальные данные прямо из файла
    steam_id = steam_ids.get(str(member.id))
    if not steam_id:
        await ctx.send(f"❌ {member.display_name} не зарегистрировал свой Steam ID, для этого, напишите в лс боту `жора стим`")
        return

    try:
        # --- Основная информация ---
        url_player = f"https://api.opendota.com/api/players/{steam_id}"
        data = requests.get(url_player).json()

        profile = data.get("profile", {})
        nickname = profile.get("personaname", "Неизвестно")
        avatar = profile.get("avatarfull")
        mmr = data.get("mmr_estimate", {}).get("estimate")
        rank_tier = data.get("rank_tier")
        rank_text = rank_tier_to_text(rank_tier)

        # --- Вин/лоз ---
        url_wl = f"https://api.opendota.com/api/players/{steam_id}/wl"
        wl_data = requests.get(url_wl).json()
        wins = wl_data.get("win", 0)
        losses = wl_data.get("lose", 0)
        total_games = wins + losses
        winrate = round((wins / total_games) * 100, 1) if total_games else 0

        # --- Любимые герои ---
        url_heroes = f"https://api.opendota.com/api/players/{steam_id}/heroes"
        heroes_data = requests.get(url_heroes).json()
        top_heroes = sorted(heroes_data, key=lambda x: x['games'], reverse=True)[:5]
        top_heroes_text = ""
        for h in top_heroes:
            hero_name = heroes.get(h['hero_id'], f"ID {h['hero_id']}")
            hero_winrate = round(h['win'] / h['games'] * 100, 1) if h['games'] > 0 else 0
            top_heroes_text += f"{hero_name} ({h['games']} игр, {hero_winrate}% вин)\n"

        # --- Последние 5 игр ---
        url_recent = f"https://api.opendota.com/api/players/{steam_id}/recentMatches"
        recent_games = requests.get(url_recent).json()[:5]
        recent_text = ""
        for game in recent_games:
            hero_name = heroes.get(game['hero_id'], f"ID {game['hero_id']}")
            player_radiant = game.get("player_slot") < 128  # 0-127 Radiant, 128-255 Dire
            radiant_win = game.get("radiant_win")
            result = "✅ Победа" if (player_radiant and radiant_win) or (not player_radiant and not radiant_win) else "❌ Поражение"
            kills = game.get("kills", 0)
            deaths = game.get("deaths", 0)
            assists = game.get("assists", 0)
            duration = game.get("duration", 0)
            minutes = duration // 60
            seconds = duration % 60
            recent_text += f"{hero_name} | {result} | KDA: {kills}/{deaths}/{assists} | Длительность: {minutes}м {seconds}с\n"

        # --- Embed ---
        embed = discord.Embed(title=f"🎮 Профиль {member.display_name}", color=0x00ff00)
        if avatar:
            embed.set_thumbnail(url=avatar)
        embed.add_field(name="Steam", value=nickname, inline=True)
        rank_text, mmr_text = rank_tier_to_text(rank_tier)

        embed.add_field(name="⭐ Ранг", value=rank_text, inline=True)
        embed.add_field(name="💎 Примерный MMR", value=mmr_text, inline=True)  # <-- вот сюда Z

        embed.add_field(name="📊 Винрейт", value=f"{winrate}% ({wins}W / {losses}L)", inline=False)
        embed.add_field(name="🔥 Любимые герои", value=top_heroes_text or "Нет данных", inline=False)
        embed.add_field(name="🕹 Последние 5 игр", value=recent_text or "Нет данных", inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Ошибка при получении данных: {e}")

@bot.command(name="топ_ранг")
async def top_rank(ctx):
    try:
        with open("steam_ids.json", "r") as f:
            steam_ids = json.load(f)
    except FileNotFoundError:
        steam_ids = {}

    players = []
    for discord_id, steam_id in steam_ids.items():
        member = ctx.guild.get_member(int(discord_id))
        if not member:
            continue  # если игрока нет на сервере, пропускаем

        try:
            url = f"https://api.opendota.com/api/players/{steam_id}"
            data = requests.get(url).json()
            rank_tier = data.get("rank_tier")
            players.append((rank_tier or 0, member.display_name))
        except:
            continue

    # Сортируем от высшего ранга к низшему
    players_sorted = sorted(players, key=lambda x: x[0], reverse=True)

    embed = discord.Embed(
        title="🏆 Топ игроков по рангу",
        color=0xFFD700
    )

    for i, (rank_tier, nickname) in enumerate(players_sorted[:10], start=1):
        rank_text = rank_tier_to_text(rank_tier) if rank_tier else "Нет ранга"
        embed.add_field(name=f"{i}. {nickname}", value=f"Ранг: {rank_text}", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="топ_вр")
async def top_wr(ctx):
    try:
        with open("steam_ids.json", "r") as f:
            steam_ids = json.load(f)
    except FileNotFoundError:
        steam_ids = {}

    results = []

    for user_id, steam_id in steam_ids.items():
        wl_response = requests.get(f"https://api.opendota.com/api/players/{steam_id}/wl")
        if wl_response.status_code == 200:
            wl_data = wl_response.json()
            wins = wl_data.get("win", 0)
            losses = wl_data.get("lose", 0)
            total = wins + losses
            winrate = round((wins / total) * 100, 1) if total > 0 else 0
            results.append((ctx.guild.get_member(int(user_id)), winrate, wins, losses))

    results.sort(key=lambda x: x[1], reverse=True)

    desc = "\n".join([f"**{i+1}. {r[0].display_name}** — {r[1]}% (W:{r[2]} / L:{r[3]})" for i, r in enumerate(results[:10])])
    embed = discord.Embed(title="📊 ТОП по винрейту", description=desc, color=0x00ffcc)
    await ctx.send(embed=embed)

# Получение MMR игрока
def get_player_mmr_or_estimate(mention):
    try:
        with open("steam_ids.json", "r") as f:
            steam_ids = json.load(f)
    except FileNotFoundError:
        steam_ids = {}

    discord_id = mention.strip("<@!>")
    steam_id = steam_ids.get(str(discord_id))
    if not steam_id:
        return 0  # если нет Steam ID, считаем MMR = 0

    try:
        data = requests.get(f"https://api.opendota.com/api/players/{steam_id}").json()
        mmr = data.get("mmr_estimate", {}).get("estimate")
        if mmr is None:
            rank_tier = data.get("rank_tier", 0)
            mmr = rank_tier * 500
        return mmr
    except:
        return 0

async def calculate_win_chances_from_team(team1, team2, steam_ids):
    """
    Асинхронно рассчитывает шансы на победу команд на основе среднего винрейта игроков.
    Возвращает проценты для team1 и team2.
    """

    async def avg_wr(team):
        total_wr = 0
        count = 0
        async with aiohttp.ClientSession() as session:
            for member in team:
                steam_id = steam_ids.get(str(member.id if hasattr(member, 'id') else member))
                if not steam_id:
                    continue
                try:
                    async with session.get(f"https://api.opendota.com/api/players/{steam_id}/wl", timeout=5) as resp:
                        if resp.status != 200:
                            continue
                        wl_data = await resp.json()
                        wins = wl_data.get("win", 0)
                        losses = wl_data.get("lose", 0)
                        total_games = wins + losses
                        if total_games > 0:
                            total_wr += wins / total_games
                            count += 1
                except:
                    continue
        return (total_wr / count) if count > 0 else None  # None если нет данных

    wr1 = await avg_wr(team1)
    wr2 = await avg_wr(team2)

    # Если нет данных ни по одной команде, возвращаем 50/50
    if wr1 is None and wr2 is None:
        return 50, 50
    # Если данных только по одной команде, считаем её сильнее среднего
    if wr1 is None:
        wr1 = wr2
    if wr2 is None:
        wr2 = wr1

    chance1 = round(wr1 / (wr1 + wr2) * 100)
    chance2 = 100 - chance1

    return chance1, chance2

# --- Начало матча с учётом MMR и автором ---
@bot.command(name="начать_матч")
@commands.has_permissions(administrator=True)
async def start_match(ctx, bo_type: str):
    bo_type = bo_type.lower()
    if bo_type not in ["bo1", "bo3", "bo5"]:
        await ctx.send("❌ Неверный тип серии! Допустимо: bo1, bo3, bo5")
        return

    channel_id = ctx.channel.id
    active_matches[channel_id] = {
        "bo_type": bo_type,
        "team1": [],
        "team2": [],
        "score": [0, 0],
        "author_id": ctx.author.id  # сохраняем автора
    }

    await ctx.send(
        f"Введите состав **Первой команды** строго по шаблону:\n"
        f"1 - @игрок\n2 - @игрок\n3 - @игрок\n4 - @игрок\n5 - @игрок\n\n"
        f"❗ Используйте только реальные упоминания через @, без текста после имени."
    )

    def check(m):
        return m.channel.id == ctx.channel.id and (
                m.author.id == ctx.author.id or m.author.guild_permissions.administrator
        )

    try:
        # --- Первая команда ---
        # Первая команда
        msg1 = await bot.wait_for("message", check=check, timeout=300)

        if len(msg1.mentions) != 5:
            await ctx.send("❌ Состав должен содержать ровно 5 упомянутых игроков. Серия отменена.")
            del active_matches[channel_id]
            return

        # Проверка, что каждая строка содержит ровно одно упоминание
        lines1 = msg1.content.split("\n")
        if len(lines1) != 5:
            await ctx.send("❌ Должно быть ровно 5 строк с упоминаниями.")
            del active_matches[channel_id]
            return

        mentions1 = []
        for line in lines1:
            # Проверяем, что в строке есть ровно одно упоминание
            found = [m for m in msg1.mentions if f"<@{m.id}>" in line]
            if len(found) != 1:
                await ctx.send("❌ Каждая строка должна содержать ровно одно упоминание через @.")
                del active_matches[channel_id]
                return
            mentions1.append(found[0])

        active_matches[channel_id]["team1"] = mentions1
        await ctx.send("✅ Состав Первой команды сохранён. Теперь введите состав Второй команды:")

        # Вторая команда
        msg2 = await bot.wait_for("message", check=check, timeout=300)

        if len(msg2.mentions) != 5:
            await ctx.send("❌ Состав должен содержать ровно 5 упомянутых игроков. Серия отменена.")
            del active_matches[channel_id]
            return

        lines2 = msg2.content.split("\n")
        if len(lines2) != 5:
            await ctx.send("❌ Должно быть ровно 5 строк с упоминаниями.")
            del active_matches[channel_id]
            return

        mentions2 = []
        for line in lines2:
            found = [m for m in msg2.mentions if f"<@{m.id}>" in line]
            if len(found) != 1:
                await ctx.send("❌ Каждая строка должна содержать ровно одно упоминание через @.")
                del active_matches[channel_id]
                return
            mentions2.append(found[0])

        active_matches[channel_id]["team2"] = mentions2
        await ctx.send("✅ Состав Второй команды сохранён.")

        # Рассчитываем шансы
        chance1, chance2 = await calculate_win_chances_from_team(
            active_matches[channel_id]["team1"],
            active_matches[channel_id]["team2"],
            steam_ids
        )

        embed = discord.Embed(title="Составы команд и шансы на победу", color=0x00ff00)
        embed.add_field(name="Команда 1", value="\n".join(m.mention for m in active_matches[channel_id]["team1"]), inline=True)
        embed.add_field(name="Команда 2", value="\n".join(m.mention for m in active_matches[channel_id]["team2"]), inline=True)
        embed.add_field(name="Счет", value="0 / 0", inline=False)
        embed.add_field(name="Шансы на победу", value=f"Команда 1: {chance1}%\nКоманда 2: {chance2}%", inline=False)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Ошибка: {e}")
        if channel_id in active_matches:
            del active_matches[channel_id]

@bot.command(name="результат")
@commands.has_permissions(administrator=True)
async def match_result(ctx, winner: str):
    channel_id = ctx.channel.id
    if channel_id not in active_matches:
        await ctx.send("❌ В этом канале нет активной серии матчей.")
        return

    match = active_matches[channel_id]

    winner = winner.lower()
    if winner not in ["team1", "team2"]:
        await ctx.send("❌ Укажите 'team1' или 'team2'.")
        return

    # Обновляем счёт
    if winner == "team1":
        match["score"][0] += 1
    else:
        match["score"][1] += 1

    # Текст для матча (одиночный матч)
    match_text = (
        f"Матч завершён:\n"
        f"Команда 1 ({', '.join(m.mention for m in match['team1'])}) — {match['score'][0]}\n"
        f"Команда 2 ({', '.join(m.mention for m in match['team2'])}) — {match['score'][1]}"
    )
    await ctx.send(match_text)

    # Проверяем, завершилась ли серия
    bo_type = match["bo_type"]
    needed_wins = {"bo1": 1, "bo3": 2, "bo5": 3}[bo_type]

    # Если кто-то выиграл серию
    if match["score"][0] >= needed_wins or match["score"][1] >= needed_wins:
        winner_key = "team1" if match["score"][0] >= needed_wins else "team2"
        loser_key = "team2" if winner_key == "team1" else "team1"

        winner_text = "Команда 1" if winner_key == "team1" else "Команда 2"
        loser_text = "Команда 2" if loser_key == "team2" else "Команда 1"

        final_text = (
            f"{winner_text} в составе:\n{', '.join(m.mention for m in match[winner_key])} "
            f"\nобыграла \n{loser_text} в составе:\n{', '.join(m.mention for m in match[loser_key])}\n"
            f"\nСерия: {bo_type.upper()}, финальный счёт: {match['score'][0]} / {match['score'][1]}"
        )

        # Канал для публикации результатов серии
        results_channel = discord.utils.get(ctx.guild.text_channels, name="5x5-результаты")
        if results_channel:
            await results_channel.send(final_text)
        # Обновляем статистику игроков
        stats_dota.update_player_stats(match[winner_key], is_win=True)
        stats_dota.update_player_stats(match[loser_key], is_win=False)

        # Удаляем активную серию
        del active_matches[channel_id]

@bot.command(name="счет")
async def show_score(ctx):
    channel_id = ctx.channel.id
    if channel_id not in active_matches:
        await ctx.send("❌ В этом канале нет активной серии матчей.")
        return

    match = active_matches[channel_id]

    # Проверка прав: автор или админ
    if ctx.author.id != match.get("author_id") and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Только автор серии или админ могут посмотреть счёт.")
        return

    team1 = match["team1"]
    team2 = match["team2"]
    score1, score2 = match["score"]

    embed = discord.Embed(title="📊 Текущий счёт серии", color=0x00ffcc)
    embed.add_field(name="Команда 1", value="\n".join(m.mention for m in team1), inline=True)
    embed.add_field(name="Команда 2", value="\n".join(m.mention for m in team2), inline=True)
    embed.add_field(name="Счёт", value=f"{score1} / {score2}", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="стата_дота")
async def show_stats(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    stats = stats_dota.load_stats()
    pid = str(member.id)
    if pid not in stats:
        await ctx.send(f"📊 У {member.mention} пока нет сыгранных серий.")
        return

    wins = stats[pid]["wins"]
    losses = stats[pid]["losses"]
    total = wins + losses
    wr = round((wins / total) * 100, 1) if total > 0 else 0

    await ctx.send(
        f"📊 Статистика {member.mention}:\n"
        f"🏆 Побед: {wins}\n"
        f"❌ Поражений: {losses}\n"
        f"📈 Winrate: {wr}%"
    )


# --- Запуск бота
if __name__ == "__main__":
    bot.run(TOKEN)

