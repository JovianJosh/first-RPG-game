from utils import rand_alive, rand_death, count_alive, count_dead, all_alive, all_dead
from RPGchar import *
from boss import *
from tabulate import tabulate

def print_stat(team):
    if not team:
        print("(Currently no member in the team now)")
        return
    
    table = []
    for i in team:
        table.append([
            i.unique_name,
            i.hp,
            max(i.str, i.int) if i.str or i.int else "0",
            i.defense if i.defense else "0",
            i.mana if i.mana else "0",
            i.cr if i.cr else "0",
            i.cd if i.cd else "0",
        ])
    
    headers = ["Name", "HP", "Attack", "Defense", "Mana", "Crit rate", "Crit dmg"]
    print(tabulate(table, headers=headers, tablefmt="double_grid"))

def char_stat(team):
    table = []
    for key, char in team.items():
        i = char()
        table.append([
            i.name,
            i.type if i.type else "N/A",
            i.hp,
            max(i.str, i.int) if i.str or i.int else "0",
            i.defense if i.defense else "0",
            i.mana if i.mana else "0",
            i.cr if i.cr else "0",
        ])
    
    headers = ["Name", "Type", "HP", "Atk", "Def", "MP", "Crit rate"]
    print(tabulate(table, headers=headers, tablefmt="double_grid"))
