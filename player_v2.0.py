import json

class Player:
    def __init__(self, name, rank, role):
        self.name = name
        self.rank = rank
        self.role = role

class Bosses:
    def __init__(self):
        self.bosses = []

    def add_boss(self, boss):
        self.bosses.append(boss)

    def get_boss(self, index):
        return self.bosses[index]

def custom_serializer(obj):
    if isinstance(obj, Player):
        return {
            'name': obj.name,
            'rank': obj.rank,
            'role': obj.role
        }
    elif isinstance(obj, list):
        return [custom_serializer(item) for item in obj]
    return obj

# bosses = Bosses()

boss_list = ['Zakum', 'Pinkbean', 'Horntail']

# for i in boss_list:
#     bosses.add_boss(i)

filename = 'player_2save.json'

p1 = Player('henry', 'SSS', 'tank')

players = {'henry': [p1, boss_list]}

json_data = json.dumps(players, default=custom_serializer, indent=4)

with open(filename, 'w') as outfile:
    outfile.write(json_data)



