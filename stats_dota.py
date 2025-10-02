import json
import os

STATS_FILE = "series_stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

def update_player_stats(players, is_win):
    stats = load_stats()
    for player in players:
        pid = str(player.id)
        if pid not in stats:
            stats[pid] = {"wins": 0, "losses": 0}
        if is_win:
            stats[pid]["wins"] += 1
        else:
            stats[pid]["losses"] += 1
    save_stats(stats)
