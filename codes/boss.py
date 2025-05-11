from random import *
from tabulate import tabulate
from random import choice as random_choice
from utils import *
from rich.console import Console
from RPGchar import *

class Boss(Character):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.action_timer = self.speed
        self.first_phase = False
        self.second_phase = False
        self.mana = 1000

    def set_teams(self, my_team, enemy):
        self.my_team = my_team
        self.enemy_team = enemy

    def atk_cd_down(self):
        self.action_timer -= 1
        if self.action_timer <= 0:
            self.action_timer = 0
        
    def act(self, my_team, enemy):
        if count_alive(enemy) >= 3:
            for i in enemy:
                if i.alive:
                    dmg = self.damage(i)//3 * 2
                    i.got_hurt(dmg)
        elif count_alive(enemy) < 3:
            for i in enemy:
                if i.alive:
                    dmg = self.damage(i)
                    i.got_hurt(dmg)

    def use_skill(self, my_team, enemy):
        if count_alive(enemy) == 1:
            self.speed = 0
        else:
            self.speed = 1
        if self.action_timer == 0:
            self.action_timer = self.speed
            if self.cooldown == 0:
                self.cooldown = self.skill_cooldown
                self.skill(my_team, enemy)
            else:
                self.act(my_team, enemy)
        else:
            self.atk_cd_down()
                
    def phases(self, my_team, enemy):
        if self.hp <= int(0.7 * self.maxhp) and self.first_phase == False:
            self.first_phase = True
            return self.phase_1(my_team, enemy)
        elif self.hp <= int(0.4 * self.maxhp) and self.second_phase == False:
            self.second_phase = True
            return self.phase_2(my_team, enemy)

    def got_hurt(self, damage, my_team, enemy):
        super().got_hurt(damage)
        self.phases(my_team, enemy)
            
class Orpheus(Boss, Alchemist):
    def __init__(self):
        super().__init__()
        self.name = 'Orpheus'
        self.unique_name = self.name
        self.type = 'Boss'
        self.hp = 5000
        self.maxhp = self.hp
        self.defense = 50
        self.speed = 2
        self.action_timer = self.speed
        self.str = 300
        self.phase = 1

    def phase_1(self, my_team, enemy):
            dprint('')
            dprint('PHASE 1!!!', style = 'bold yellow')
            dprint('')
            dprint('Critical Rate are cut by 50%', style = 'magenta')
            for i in my_team:
                if i.alive:
                    dprint(f"{i.unique_name}'s Critical rate decreased by 50%")
                    i.cr -= 50
                    if i.cr < 0:
                        i.cr = 0

    def phase_2(self, my_team, enemy):
            dprint('')
            dprint('PHASE 2!!!', style = 'bold yellow')
            dprint('')
            self.clear_all_debuffs()
            for i in enemy:
                if i.alive:
                    i.clear_all_buffs()
            dprint('')
            dprint('Steals Attack power all allies')
            for i in my_team:
                if i.alive:
                    dprint(f"{i.unique_name}'s Attack power decreased by 100")
                    if i.str > i.int:
                        i.str -= 100
                    elif i.str < i.int:
                        i.int -= 100
            self.str += 200
            dprint('')
            dprint(f"{self.unique_name}'s Attack power increased by 200")

    def skill(self, my_team, enemy):
        Alchemist.skill(self, my_team, enemy)

class Gawain(Boss):
    def __init__(self):
        super().__init__()
        self.name = 'Gawain'
        self.unique_name = self.name
        self.type = 'Boss'
        self.hp = 5000
        self.maxhp = self.hp
        self.defense = 200
        self.str = 50
        self.resistance = 50

    def act(self, my_team, enemy):
            for i in enemy:
                if i.alive:
                    self.ignore_defense = True
                    dmg = self.damage(i, self.str)
                    i.got_hurt(dmg)
                    i.maxhp -= dmg

    def phase_1(self, my_team, enemy):
        dprint('')
        dprint('PHASE 1!!!', style='bold yellow')
        dprint('')
        dprint('Buff steal!!')

        enemy[0].clear_all_debuffs()
        for i in my_team:
            effects = i.active_effects()
            active_buffs = effects['Buffs']
            if active_buffs:
                for buff in active_buffs:
                    enemy[0].apply_buff(buff)
                i.clear_all_buffs()

    def phase_2(self, my_team, enemy):
        dprint('')
        dprint('PHASE 2!!!', style='bold yellow')
        dprint('')
        dprint("Defense boost!! Gawain's defense increased by 200")
        dprint("Shield Bash!!")

        enemy[0].defense += 200
        enemy[0].str += 30
        for i in my_team:
            self.ignore_defense = True
            dmg = self.damage(i, enemy[0].defense)
            i.got_hurt(dmg, my_team, enemy)
            i.maxhp -= dmg

    def skill(self, my_team, enemy):
        if self.debuffs["Defense break"]:
            self.clear_debuff("Defense break")
        self.act(my_team, enemy)
        

    


        


            
            
            

