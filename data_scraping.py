import soccerdata as sd

world_cup_stats = sd.FBref(leagues='INT-World Cup', seasons=2026, headless=False)

schedule = world_cup_stats.read_schedule()

all_match_stats = []

for id in schedule['game_id']:

    player_match_stats = world_cup_stats.read_player_match_stats(stat_type='summary', match_id=id)

    all_match_stats.append(player_match_stats)

print(len(all_match_stats))