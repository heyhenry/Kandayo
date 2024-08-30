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
            'job': obj.rank, 
            'level': obj.role,
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

b1 = Bosses(True, False, True)
p1 = Player('henry', 'SSS', 'tank', b1)

players = {'henry': p1}

json_data = json.dumps(players, default=custom_serializer, indent=4)

with open(storage_filename, 'w') as outfile:
    outfile.write(json_data)






