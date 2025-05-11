from random import *
from tabulate import tabulate
from random import choice as random_choice
from utils import *
from rich.console import Console

console = Console()
DEBUG_PRINT = True
def dprint(text, style=None):
    if DEBUG_PRINT:
        console.print(text, style=style)


MANA_COST = 20
MANA_RECOVERY = 30
DEBUFF_RATE = 50
UNBUFF_RATE = 50

class Stats:
    def __init__(self):
        self.hp = 100
        self.maxhp = self.hp
        self.mana = 60
        self.maxmana = self.mana
        self.int = 0
        self.str = 0
        self.defense = 10
        self.cr = 20
        self.cd = 150
        self.penetration = 10
        self.accuracy = 100
        self.resistance = 25

    def acc(self):
        return randint(self.accuracy,100)

    def resist(self):
        odds = randint(0,100)
        if self.resistance >= odds:
            return True
        return False      

    def crit_rate(self):
        crit = randint(1, 100)
        if self.cr >= 100:
            return True
        return self.cr >= crit

    def crit_damage(self, raw_damage):
        if self.crit_rate():
            dprint('')
            dprint('Critical Hit!!', style = 'bold yellow')
            return int(raw_damage * (self.cd / 100))
        return raw_damage

class Character(Stats):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.alive = True
        self.cost = 0
        self.controlled = False
        self.unique_name = None
        self.ability = False
        self.combo_counter = 0
        self.cooldown = 0
        self.ignore_defense = False
        self.skill_cooldown = 1
        self.debuffs = {
            'Defense break' : False,
            'Attack down' : False,
            'Critical down' : False,
            'Blind' : False,
        }
        self.buffs = {
            'Defense up' : False,
            'Attack up' : False,
            'Crit rate up' : False,
            'Crit dmg up' : False,
            'Immunity' : False,
        }
    def char_type(char_type, team):
        return [i for i in team if i.type == char_type and i.alive]

    def active_effects(self):
        active_debuffs = [i for i, value in self.debuffs.items() if value is True]
        active_buffs = [i for i, value in self.buffs.items() if value is True]
        return {'Debuffs': active_debuffs, 'Buffs': active_buffs}

    def inactive_buffs(self):
        return [i for i, value in self.buffs.items() if value is False]

    def inactive_debuffs(self):
        return [i for i, value in self.debuffs.items() if value is False]

    def active_buffs(self):
        return [i for i, value in self.buffs.items() if value is True]

    def active_debuffs(self):
        return[i for i, value in self.buffs.items() if value is True]

    def decrement_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                dprint(f"Ability is ready!", style='bold green')

    def count_debuff(self):
        return sum(i for i in self.debuffs.values())

    def count_buff(self):
        return sum(i for i in self.buffs.values())

    def apply_debuff(self, debuff):
        if self.resist() == True:
            dprint('')
            dprint(f"{self.unique_name} resisted the debuff!!")
        else:
            debuffed = randint(0,100)
            if debuffed >= DEBUFF_RATE:              
                    if self.debuffs[debuff] == False:
                        self.debuffs[debuff] = True
                        dprint('')
                        dprint(f"{self.unique_name} is afflicted with {debuff}!", style = 'magenta')
                        if debuff == "Defense break":
                            self.defense //= 2
                            dprint('')
                            dprint(f"{self.unique_name}'s defense is halved to {self.defense}!", style = 'magenta')
                        
                        elif debuff == "Attack down":
                            if self.int >= self.str:
                                self.int //= 2
                                dprint('')
                                dprint(f"{self.unique_name}'s intelligence is halved to {self.int}!", style = 'magenta')
                            else:
                                self.str //= 2
                                dprint('')
                                dprint(f"{self.unique_name}'s strength is halved to {self.str}!", style = 'magenta')
                        
                        elif debuff == "Critical down":
                            self.cr -= 25
                            self.cd -= 25
                            dprint('')
                            dprint(f"{self.unique_name}'s critical rate decreased by 25%! Current CR: {self.cr}%", style = 'magenta')
                            dprint(f"{self.unique_name}'s critical damage decreased by 25%! Current CD: {self.cd}%", style = 'magenta')
                        
                        elif debuff == "Blind":
                            self.accuracy -= 50
                            dprint('')
                            dprint(f"{self.unique_name} is blinded! Accuracy decreased by 50%.", style = 'magenta')
            else:
                dprint('')
                dprint('Debuff is not afflicted successfully', style = 'bright_green')
                
    def clear_debuff(self, debuff):
        if debuff in self.debuffs and self.debuffs[debuff]:
                self.debuffs[debuff] = False
                dprint('')
                dprint(f"{self.unique_name}'s {debuff} debuff has been cleared!", style = 'bright_green')

                if debuff == "Defense break":
                    self.defense *= 2
                    dprint('')
                    dprint(f"{self.unique_name}'s defense is restored to {self.defense}!", style = 'bright_green')
                elif debuff == "Attack down":
                    if self.int >= self.str:
                        self.int *= 2
                        dprint('')
                        dprint(f"{self.unique_name}'s intelligence is restored to {self.int}!", style = 'bright_green')
                    else:
                        self.str *= 2
                        dprint('')
                        dprint(f"{self.unique_name}'s strength is restored to {self.str}!", style = 'bright_green')
                elif debuff == "Critical down":
                    self.cr += 25
                    dprint('')
                    dprint(f"{self.unique_name}'s critical rate is restored to {self.cr}!", style = 'bright_green')
                elif debuff == "Blind":
                    dprint('')
                    dprint(f"{self.unique_name} has recovered from blindness!", style = 'bright_green')

    def clear_all_debuffs(self):
        cleardebuff = randint(0,100)
        if cleardebuff >= DEBUFF_RATE:
            for i in self.debuffs:
                if self.debuffs[i]:
                    self.clear_debuff(i)
                    dprint('')
                    dprint(f"All debuffs have been cleared from {self.unique_name}!", style = 'bright_green')
        else:
            dprint('')
            dprint(f"Debuff not successfully removed from {self.unique_name}")
            
    def apply_buff(self, buff):
        if buff in self.buffs and not self.buffs[buff]:
            self.buffs[buff] = True
            dprint('')
            dprint(f"{self.unique_name} gains the buff: {buff}!", style = 'green')
            if buff == "Defense up":
                self.defense *= 2
                dprint('')
                dprint(f"{self.unique_name}'s defense is doubled to {self.defense}!", style = 'green')
            elif buff == "Attack up":
                if self.str >= self.int:
                    self.str = int(self.str * 1.5)
                    dprint('')
                    dprint(f"{self.unique_name}'s strength is doubled to {self.str}!", style = 'green')
                else:
                    self.int = int(self.int * 1.5)
                    dprint('')
                    dprint(f"{self.unique_name}'s intelligence is doubled to {self.int}!", style = 'green')
            elif buff == "Crit rate up":
                self.cr += 25
                dprint('')
                dprint(f"{self.unique_name}'s critical rate increased to {self.cr}%!", style = 'green')
            elif buff == "Crit dmg up":
                self.cd += 25
                dprint('')
                dprint(f"{self.unique_name}'s critical damage increased to {self.cd}%!", style = 'green')
            elif buff == "Immunity":
                self.resistance += 75
                dprint('')
                dprint(f"{self.unique_name} is now immune to debuffs", style = 'green')

    def clear_buff(self, buff):
        if buff in self.buffs and self.buffs[buff]:
                self.buffs[buff] = False
                dprint('')
                dprint(f"{self.unique_name}'s {buff} buff has been cleared!", style = 'bright_blue')
                if buff == "Defense up":
                    self.defense //= 2
                    dprint('')
                    dprint(f"{self.unique_name}'s defense is restored to {self.defense}!", style = 'bright_blue')
                elif buff == "Attack up":
                    if self.str >= self.int:
                        self.str = int(self.str/1.5)
                        dprint('')
                        dprint(f"{self.unique_name}'s strength is restored to {self.str}!", style = 'bright_blue')
                    else:
                        self.int = int(self.int/1.5)
                        dprint('')
                        dprint(f"{self.unique_name}'s intelligence is restored to {self.int}!", style = 'bright_blue')
                elif buff == "Crit rate up":
                    self.cr -= 25
                    dprint('')
                    dprint(f"{self.unique_name}'s critical rate is restored to {self.cr}!", style = 'bright_blue')
                elif buff == "Crit dmg up":
                    self.cd -= 25
                    dprint('')
                    dprint(f"{self.unique_name}'s critical damage is restored to {self.cd}!", style = 'bright_blue')
                    
    def clear_all_buffs(self):
        for i in self.buffs:
            unbuffed = randint(0,100)
            if unbuffed >= UNBUFF_RATE:
                if self.buffs[i]:
                    self.clear_buff(i)
                    dprint('')
                    dprint(f"{i} buff have been cleared from {self.unique_name}!", style = 'bright_blue')
            elif unbuffed < UNBUFF_RATE and self.buffs[i]:
                dprint('')
                dprint(f"Buffs not successfully removed from {self.unique_name}")
                
    def newname(self, number):
        class_name = self.__class__.__name__
        if class_name not in number:
            number[class_name] = 1
        else:
            number[class_name] += 1
        return f'{class_name} {number[class_name]}'

    def damage(self, target, damage):
        if self.crit_rate():
            damage = self.crit_damage(damage)
        if self.ignore_defense:
            return int(damage * (self.acc() / 100))
        else:
            new_defense = target.defense - self.penetration
            final_damage = int(damage * (self.acc() / 100) * (120 / (120 + new_defense)))
            return final_damage

    def action(self, my_team, enemy):
        if self.controlled:
            self.player_action(my_team, enemy)
        else:
            self.ai_action(my_team, enemy)


    def got_hurt(self, damage, my_team=None, enemy=None):
        if damage >= self.hp:
            self.hp = 0
            self.alive = False
            dprint('')
            dprint(f"{self.unique_name} takes {damage} damage.", style='red')
            dprint('')
            dprint(f'{self.unique_name} died!')
        else:
            self.hp -= damage
            dprint('')
            dprint(f"{self.unique_name} takes {damage} damage.", style='red')
            dprint(f"{self.unique_name} has {self.hp} HP remaining.", style='red')
        self.ignore_defense = False

    def heal(self, amount):
        self.hp += amount
        dprint('')
        dprint(f"{self.unique_name}'s HP is healed by {amount}")
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def act(self, my_team, enemy):
        self.decrement_cooldown()
        target_index = rand_alive(enemy)
        target = enemy[target_index]
        calculated_damage = self.damage(target, max(self.str, self.int))
        target.got_hurt(calculated_damage, my_team, enemy)

    def player_action(self, my_team, enemy):
        dprint(f"{self.unique_name}'s turn!")
        dprint("1. Attack")
        dprint('2. Unique Skill')
        dprint('3. Train')
        try:
            choice = int(input("Choose an action (1-3): "))
            if choice == 1:
                self.act(my_team, enemy)
            elif choice == 2:
                self.use_skill(my_team, enemy)
            elif choice == 3:
                dprint(f'{self.unique_name} uses Train!')
                dprint('1: Attack Power')
                dprint('2: Defense')
                dprint('3: Critical')
                train_choice = int(input('Choose an attribute to train (1-3): '))
                if train_choice not in [1, 2, 3]:
                    train_choice = random_choice([1, 2, 3])
                    dprint('')
                    dprint(f"Invalid choice! Randomly selecting training option {train_choice}...")
                if train_choice == 1:
                    dprint('')
                    dprint(f"{self.unique_name}'s Attack Power increased by 50!")
                    if self.str >= self.int:
                        self.str += 50
                    else:
                        self.int += 50
                elif train_choice == 2:
                    dprint('')
                    dprint(f"{self.unique_name}'s Defense increased by 10!")
                    self.defense += 10
                elif train_choice == 3:
                    dprint('')
                    dprint(f"{self.unique_name}'s Critical Rate increased by 15%!")
                    dprint(f"{self.unique_name}'s Critical Damage increased by 15%!")
                    self.cr += 15
                    self.cd += 15
            else:
                dprint('')
                dprint("Invalid input. Defaulting to attack.")
                self.act(my_team, enemy)
        except ValueError:
            dprint('')
            dprint("Invalid input. Defaulting to attack.")
            self.act(my_team, enemy)

    def ai_action(self, my_team, enemy):
        self.use_skill(my_team, enemy)

class Fighter(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Fighter'
        self.type = 'Fighter'
        self.hp = 1200
        self.maxhp = self.hp
        self.str = 100
        self.cost = 100
        self.mana = 40
        self.maxmana = self.mana

    def skill(self, my_team, enemy):
            dprint('')
            dprint('Whirlwind Slash!!', style = 'bold cyan')
            for i in enemy:
                if i.alive:
                    damage = self.damage(i, self.str)
                    i.got_hurt(damage, my_team, enemy)

    def use_skill(self, my_team, enemy):
        if self.cooldown == 0:
            self.cooldown = self.skill_cooldown
            self.skill(my_team, enemy)
        else:
            self.act(my_team, enemy)       
        
class Mage(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Mage'
        self.hp = 800
        self.maxhp = self.hp
        self.mana = 60
        self.maxmana = self.mana
        self.cost = 200
        self.int = 400
        self.type = 'Glasscannon'

    def skill(self, my_team, enemy):
            target_index = rand_alive(enemy)
            target = enemy[target_index]
            calculated_damage = self.damage(target, self.int)
            dprint('')
            dprint(f'{self.unique_name} casts Mana Wave',style = 'bold cyan')
            target.got_hurt(calculated_damage, my_team, enemy)

    def use_skill(self, my_team, enemy):
        if self.mana >= MANA_COST and self.cooldown == 0:
            self.mana -= MANA_COST
            self.cooldown = self.skill_cooldown
            self.skill(my_team, enemy)
        elif self.mana >= MANA_COST:
            self.act(my_team, enemy)
        else:
            self.manaregen()
            
    def manaregen(self):
        mana_before = self.mana
        self.mana += MANA_RECOVERY
        self.decrement_cooldown()
        if self.mana > self.maxmana:
            self.mana = self.maxmana
        dprint('')
        dprint('Mana not enough!! Mana Recovery!', style = 'bold cyan')
        dprint(f'Recover Mana from {mana_before} to {self.mana}.', style = 'green')

class Berserker(Fighter):
    def __init__(self):
        super().__init__()
        self.cost = 300
        self.str = 200
        self.name = 'Berserker'
        self.type = 'Fighter'

    def berserk(self):
        if self.hp <= self.maxhp // 2:
            dprint('')
            dprint('Berserk mode! Double Attack!', style = 'yellow')
            if self.ability == False:
                self.str *= 2
                self.ability = True
        elif self.hp > self.maxhp // 2:
            if self.ability:
                self.str //= 2
                self.ability = False

    def act(self, my_team, enemy):
        self.berserk()
        super().act(my_team, enemy)

    def skill(self, my_team, enemy):
        self.berserk()
        super().skill(my_team, enemy)

class ArchMage(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'ArchMage'
        self.cost = 500
        self.type = 'Glasscannon'
        self.int = 400
        self.maxpen = self.penetration

    def skill(self, my_team, enemy):
            dprint('')
            dprint('Meteor Shower!', style = 'bold cyan')
            for i in enemy:
                if i.alive:
                    if i.type == 'Boss':
                        self.penetration = 50
                    damage = self.damage(i, self.int)
                    totaldmg = damage*3 // max(1,count_alive(enemy))
                    i.got_hurt(totaldmg, my_team, enemy)
                    self.penetration = self.maxpen

class Necromancer(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'Necromancer'
        self.cost = 400
        self.type = 'Support'
        self.mana = 40
        self.maxmana = self.mana
        self.int = 200

    def skill(self, my_team, enemy):
        if count_dead(my_team) >= 1 and self.maxhp > 0:
            index = rand_death(my_team)
            target = my_team[index]
            self.mana -= MANA_COST
            self.cooldown = 2
            revivedhp = target.maxhp // 2
            target.hp = revivedhp
            target.alive = True
            dprint('')
            dprint('A R I S E ! ! !', style = 'bold green')
            dprint(f'Reviving member {target.unique_name} with {revivedhp} hp', style = 'green')
        else:
            super().skill(my_team, enemy)

class Assassin(Fighter):
    def __init__(self):
        super().__init__()
        self.name = 'Assassin'
        self.cost = 500
        self.str = 300
        self.hp = 800
        self.maxhp = self.hp
        self.penetration = 10
        self.type = 'Glasscannon'

    def act(self, my_team, enemy):
        if char_type('Glasscannon', enemy):
            self.decrement_cooldown()
            targeted = choice(char_type('Glasscannon', enemy))
            dprint('')
            dprint('Sicarius!! Double Damage!!', style = 'yellow')
            dmg = self.damage(targeted, self.str*2)
            targeted.got_hurt(dmg, my_team, enemy)
        elif enemy[0].type == 'Boss':
            dprint('')
            dprint('Sicarius!! Double Damage!!', style = 'yellow')
            normal = self.penetration
            self.penetration += enemy[0].defense//2
            dmg = self.damage(enemy[0], self.str*2)
            enemy[0].got_hurt(dmg, my_team, enemy)
            self.penetration = normal
        else:
            super().act(my_team, enemy)
            
    def skill(self, my_team, enemy):
        if self.ability == False:
            self.decrement_cooldown()
            self.ability=True
            self.cr += 30
            self.cd += 50
            dprint('')
            dprint("Shadow Walk!!", style = 'bold cyan')
            dprint(f"{self.unique_name}'s Crit rate increased by 30%", style = 'green')
            dprint(f"{self.unique_name}'s Crit damage increased by 50%", style = 'green')
        elif self.ability:
            dprint('')
            dprint('Hidden Art!!!', style = 'bold yellow')
            dprint('')
            dprint('Back Stab!! Double Damage !!', style = 'bold cyan')
            unbuffed = self.str
            self.str *= 2
            self.act(my_team, enemy)
            self.str = unbuffed

class Paladin(Fighter):
    def __init__(self):
        super().__init__()
        self.name = 'Paladin'
        self.type = 'Tank'
        self.hp = 2000
        self.maxhp = 2000
        self.cost = 500
        self.defense = 30
        self.maxdef = self.defense

    def act(self, my_team, enemy):
        self.decrement_cooldown()
        target_index = rand_alive(enemy)
        target = enemy[target_index]
        dmg = self.damage(target, max(0, self.defense)*2 + 100)
        target.got_hurt(dmg, my_team, enemy)
        self.defense += 5
        dprint(f"Defense UP!! {self.unique_name}'s defense increased by 5.", style = 'green')

    def skill(self, my_team, enemy):
            dprint('')
            dprint('Guardian Strike!!')
            dprint('')
            self.heal(200)
            for i in enemy:
                if i.alive:
                    totaldmg = self.damage(i, max(0, self.defense)*5 + 100)
                    i.got_hurt(totaldmg, my_team, enemy)
            dprint(f"Defense UP!! {self.unique_name}'s defense increased by 5.", style = 'green')

class Cleric(Mage):
    def __init__(self):
        super().__init__()
        self.name='Cleric'
        self.type='Support'
        self.hp = 1200
        self.maxhp = self.hp
        self.cost = 500
        self.int = 200

    def skill(self, my_team, enemy):
            if count_alive(my_team) > 1:
                dprint('')
                dprint(f'Healing for everyone!! heal by {self.int}', style = 'bold green')
                for i in my_team:
                    if i.alive:
                        i.heal(self.int)
            elif count_alive(my_team) == 1 and self.alive:
                self.mana -= MANA_COST
                dprint('')
                dprint('Drain!!', style = 'bold cyan')
                super().act(my_team, enemy)
                self.heal(self.int)

class Archer(Fighter):
    def __init__(self):
        super().__init__()
        self.name = 'Archer'
        self.type = 'Glasscannon'
        self.hp = 800
        self.maxhp = self.hp
        self.cr = 50
        self.str = 200
        self.cost = 500

    def skill(self, my_team, enemy):
        if enemy[0].type != 'Boss':
            dprint('')
            dprint('Arrow rain!!', style = 'bold cyan')
            for i in enemy:
                if i.alive:
                    dmg = self.damage(i, self.str)
                    random_arrow = random_choice([1,2])
                    totaldmg=dmg * random_arrow
                    dprint('')
                    dprint(f"{i.unique_name} got hit by {random_arrow} arrow", style = 'yellow')
                    i.got_hurt(totaldmg, my_team, enemy)
        elif enemy[0].type == 'Boss':
            dprint('')
            dprint('Cross Fire!!', style = 'bold cyan')
            dmg = self.damage(enemy[0], enemy[0].maxhp//5)
            enemy[0].got_hurt(dmg, my_team, enemy)

class Minstrel(Cleric):
    def __init__(self):
        super().__init__()
        self.name = 'Minstrel'

    def skill(self, my_team, enemy):
        if count_alive(my_team) > 1:
            dprint('')
            dprint('Secret Melody!!', style = 'bold cyan')
            for i in my_team:
                if i.alive:
                    if i.inactive_buffs():
                        random_buff = random_choice(i.inactive_buffs())
                        i.apply_buff(random_buff)                
        elif count_alive(my_team) == 1 and self.alive:
            dprint('')
            dprint('Battle Melody!!', style = 'bold cyan')
            unbuffed = self.int
            self.int *= 3
            super().act(my_team, enemy)
            self.int = unbuffed

class Monk(Fighter):
    def __init__(self):
        super().__init__()
        self.str = 250
        self.cost = 400
        self.mana = 20
        self.hp = 1200
        self.maxhp = self.hp
        self.revived = False

    def act(self, my_team, enemy):
        target_index = rand_alive(enemy)
        target = enemy[target_index]
        self.decrement_cooldown()
        if self.combo_counter % 2 == 0:
            dprint('')
            dprint('Shell Break!!', style='bold cyan')
            target.apply_debuff('Defense break')
            dmg = self.damage(target, self.str)
            target.got_hurt(dmg, my_team, enemy)
        else:
            super().act(my_team, enemy)

        if self.ability:
                dmg = self.damage(target, self.str)
                dprint('')
                dprint(f"Lifesteal by {dmg}")
                self.heal(dmg)

        self.combo_counter += 1

    def skill(self, my_team, enemy):
        if self.hp > 400 and self.ability == False:
            self.ability = True
            dprint('')
            dprint("Asura Aura!!", style='bold cyan')
            sacr = 400
            self.got_hurt(sacr)
            dprint('')
            dprint(f'Sacrifices {sacr} hp for boosted power')
        elif self.hp <= 400 and self.revived == False:
            self.revived = True
            dprint('')
            dprint("Forbidden Technique: Rebirth!!")
            self.hp = self.maxhp
        else:
            super().act(my_team, enemy)

class Bishop(Cleric):
    def __init__(self):
        super().__init__()
        self.name = 'Bishop'
        self.cost = 700
        self.int = 300
        self.nemesis_count = 0

    def skill(self, my_team, enemy):
        if self.nemesis_count == 0:
            self.nemesis_count += 1
            dprint('')
            dprint('Nemesis!!', style = 'bold cyan')
            for i in enemy:
                if i.alive:
                    dmg = self.damage(i, self.int)
                    i.got_hurt(dmg, my_team, enemy)
                    i.apply_debuff('Blind')
        elif count_alive(my_team) > 1:
                dprint('')
                dprint('Divine Bless!!')
                dprint('')
                dprint(f'Healing for everyone!! heal by {self.int}', style = 'bold green')
                for i in my_team:
                    if i.alive:
                        i.heal(self.int)
                        i.clear_all_debuffs()
        elif count_alive(my_team) == 1 and self.alive:
                dprint('')
                dprint('Drain!!', style = 'bold cyan')
                super().act(my_team, enemy)
                self.cooldown = self.skill_cooldown
                self.heal(self.int)
                    
class Alchemist(Mage):
    def __init__(self):
        super().__init__()
        self.cost = 600
        self.int = 300
        self.name = 'Alchemist'
        self.type = 'Support'
        self.mana = 40
        self.maxmana = self.mana

    def skill(self, my_team, enemy):
            dprint('')
            dprint('Curse Bomb!!')
            for i in enemy:
                if i.alive:
                    dmg = self.damage(i, self.int)
                    totaldmg = dmg + (100 * i.count_debuff())
                    i.got_hurt(totaldmg, my_team, enemy)
                    if i.inactive_debuffs():
                        random_debuff = random_choice(i.inactive_debuffs())
                        i.apply_debuff(random_debuff)
                        dprint(f"{i.unique_name} has {i.count_debuff()} debuff")

class Gladiator(Berserker):
    def __init__(self):
        super().__init__()
        self.name = 'Striker'
        self.type = 'Fighter'
        self.cost = 500
        self.str = 200
        self.cr = 50

    def skill(self, my_team, enemy):
            self.berserk()
            dprint('')
            dprint('Pillar blade!!', style = 'bold cyan')
            self.mana -= MANA_COST
            for i in enemy:
                if i.alive:
                    i.clear_all_buffs()
                    damage = self.damage(i, self.str)
                    i.got_hurt(damage, my_team, enemy)
        
    

    
            
            
        
            

            




    

    


        
