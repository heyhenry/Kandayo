import json

class Bosses:
    def __init__(self, magnus, pinkbean, zakum):
        self.magnus = magnus
        self.pinkbean = pinkbean
        self.zakum = zakum

class Player:
    def __init__(self, name, rank, role, boss_list):
        self.name = name
        self.rank = rank
        self.role = role
        self.boss_list = boss_list

def custom_serializer(obj):
    if isinstance(obj, Player):
        return {
            'player_name': obj.name,
            'rank': obj.rank, 
            'role': obj.role,
            'boss_list': custom_serializer(obj.boss_list)
        }
    elif isinstance(obj, Bosses):
        return {
            'magnus': obj.magnus,
            'pinkbean': obj.pinkbean,
            'zakum': obj.zakum
        }
    return obj

storage_filename = 'player_save.json'

# default bosslist obj to be included in all player objs
b1 = Bosses(True, False, True)

# creation of a player obj
p1 = Player('henry', 'SSS', 'tank', b1)

# dictionary of players
players = {'henry': p1}

# update the save file with latest players data
def update_players():
    json_data = json.dumps(players, default=custom_serializer, indent=4)

    with open(storage_filename, 'w') as outfile:
        outfile.write(json_data)

# loading player data and updates the existing player dictionary
def load_players():
    with open(storage_filename, 'r') as file:
        player_data = json.load(file)

    for key, val in player_data.items():
        players[key] = Player(key, val['rank'], val['role'], val['boss_list'])

# updating a boss's status in the boss_list sub obj
p1.boss_list.magnus = False
# print(p1.boss_list.magnus)
update_players()
load_players()


# displaying the data stored in the player obj and its sub obj (bosses)
for key, val in players.items():
    # to see the values of the main obj
    print(vars(val))







