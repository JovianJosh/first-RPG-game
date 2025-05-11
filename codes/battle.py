from RPGchar import *
from random import *
from team import *
from utils import *
from boss import *
from tabulate import tabulate
import keyboard
import os
from rich.console import Console


GOLD     = 2000  
MIN_COST = 100

classes = {
  1: Fighter,
  2: Mage,
  3: Berserker,
  4: ArchMage,
  5: Necromancer,
  6: Assassin,
  7: Paladin,
  8: Cleric,
  9: Archer,
  10: Minstrel,
  11: Monk,
  12: Bishop,
  13: Alchemist,
  14: Gladiator,
}

bosses = {
  1: Orpheus,
  2: Gawain,
  
}

def create_char(i):
  return classes[i]()

def create_rand_boss():
  return [bosses[randint(1,len(bosses))]()]

def create_rand_team(gold):
  team = []
  number = {}
  while gold > 0 and len(team)<5:
    char = create_char(randint(4, len(classes)))
    char.unique_name = char.newname(number)
    if gold >= char.cost:
      gold -= char.cost
      team.append(char)     
  return team

def user_choose_boss():
    while True:
        try:
            dprint("Choices:")
            for key, i in bosses.items():
                dprint(f"{key}: {i.__name__}")
            
            user_input = input(f'Input a choice from 1 to {len(bosses)}: ').strip()
            choice = int(user_input)

            if choice < 1 or choice > len(bosses):
                dprint(f"Your choice {choice} is not valid. Please choose again.")
            else:
                return [bosses[choice]()]
        except ValueError:
            dprint("Invalid input. Please enter a valid number.", style='bold red')


def user_choose_team(gold):
    team = []
    number = {}
    
    while (gold >= MIN_COST) and (gold != 0) and len(team) < 5:
        try:
            dprint("\nYour current team:")
            print_stat(team)
            dprint(f'\nYou have {gold} gold currently')
            choice = -1

            while True:
                dprint("Choices:")
                for i, cls in classes.items():
                    dprint(f"{i}: {cls.__name__} (cost: {cls().cost})")
                dprint("0: Start the game now")
                
                user_input = input(f'Input a choice from 0 to {len(classes)}: ').strip()
                choice = int(user_input)

                if choice == 0:
                    return team
                elif choice < 1 or choice > len(classes):
                    dprint(f"Your choice {choice} is not valid. Please choose again.")
                else:
                    break

            char = create_char(choice)
            char.unique_name = char.newname(number)
            char.controlled = True
            if gold >= char.cost and len(team) < 5:
                gold -= char.cost
                team.append(char)
            else:
                dprint("Not enough gold", style="bold red")
        except ValueError:
            dprint(f"Invalid input. Please enter a valid number.", style='bold red')

    return team


def user_choose_enemy_team(gold):
    team = []
    number = {}
    choice = -1
    while (gold >= MIN_COST) and (gold != 0) and len(team) < 5:
        dprint("\nYour current team:")
        print_stat(team)
        dprint(f'\nYou have {gold} gold currently')
        choice = -1
        while True:
            dprint("Choices:")
            for key, i in classes.items():
                dprint(f"{key}: {i.__name__} (cost: {i().cost})")
            dprint("0: Finish creating the team")
            user_input = input(f'Input a choice from 0 to {len(classes)}: ').strip()
            if not user_input.isdigit():
                dprint(f"Invalid input: '{user_input}'. Please enter a valid number.")
                continue
            choice = int(user_input)
            if choice == 0:
              return team
            elif choice < 1 or choice > len(classes):
                dprint(f"Your choice {choice} is not valid. Please choose again.")
            else:
                break
        char = create_char(choice)
        char.unique_name = char.newname(number)
        if gold >= char.cost and len(team) < 5:
            gold -= char.cost
            team.append(char)
        else:
            print("Not enough gold")
    return team


def run_battle(team_a, team_b, pause=True):
    rd = 0
    a_turn = True
    dprint("")
    dprint("THE BATTLE STARTS!!!!!")

    while not all_dead(team_a) and not all_dead(team_b):
        dprint('')
        if a_turn:
            attacker_team = team_a
            defender_team = team_b
            rd += 1
            dprint(f"Round {rd}")
        else:
            attacker_team = team_b
            defender_team = team_a
        if DEBUG_PRINT:
            print("Team A:")
            print_stat(team_a)
            print()
            print("Team B:")
            print_stat(team_b)
        dprint('')
        attacker = action_turn(attacker_team)
        team_s = 'Team A' if a_turn else 'Team B'
        dprint(f'{attacker_team[attacker].active_effects()}')
        dprint(team_s + f' member {attacker + 1} {attacker_team[attacker].unique_name} acts')
        attacker_team[attacker].action(attacker_team, defender_team)
        a_turn = not a_turn
        if pause:
            dprint('')
            input("Press Enter to continue....")
    if all_dead(team_b):
        return 0
    return 1

def create_enemy_team(gold):
    dprint("How would you like to create the enemy team?", style = 'cyan')
    dprint("1: Randomly generate the team", style = 'cyan')
    dprint("2: Choose the team manually", style = 'cyan')
    while True:
      try:
        choice = int(input("Enter 1 or 2: "))
        if choice == 1:
            return create_rand_team(gold)
        elif choice == 2:
            dprint("You will now manually choose the enemy team.")
            return user_choose_enemy_team(gold)
        else:
            dprint("Invalid choice. Please enter 1 or 2.", style = 'bold red')
      except ValueError:
        dprint("Invalid choice. Please enter 1 or 2", style = 'bold red')

def create_boss_team():
    dprint("How would you like to create the boss?", style = 'cyan')
    dprint("1: Randomly generate the boss", style = 'cyan')
    dprint("2: Choose the boss manually", style = 'cyan')
    while True:
      try:
        choice = int(input("Enter 1 or 2: "))
        if choice == 1:
            return create_rand_boss()
        elif choice == 2:
            dprint("You will now manually choose the enemy team.")
            return user_choose_boss()
        else:
            dprint("Invalid choice. Please enter 1 or 2.", style = 'bold red')
      except ValueError:
        dprint("Invalid choice. Please enter 1 or 2", style = 'bold red')

def choose_fight():
    dprint("Who would you like to fight?", style = 'cyan')
    dprint("1: Normal Enemy", style = 'cyan')
    dprint("2: Boss", style = 'cyan')
    while True:
      try:
        choice = int(input("Enter 1 or 2: "))
        if choice == 1:
          return create_enemy_team(3000)
        elif choice == 2:
          return create_boss_team()
        else:
          dprint("Invalid choice. Please enter 1 or 2", style = 'bold red')
      except ValueError:
        dprint("Invalid choice. Please enter 1 or 2", style = 'bold red')

def game_start(gold,pause = True):
  enemy = choose_fight()
  dprint('')
  dprint("Your enemy will be:")
  print_stat(enemy)
  my_team = user_choose_team(gold)
  if run_battle(my_team, enemy, pause) == 0:
    dprint('')
    dprint('Team A:')
    print_stat(my_team)
    dprint('Team B:')
    print_stat(enemy)
    dprint("Congratz! You won!")
  else:
    dprint('')
    dprint('Team A:')
    print_stat(my_team)
    dprint('Team B:')
    print_stat(enemy)
    dprint("Sorry, you lose")

def press_to_start():
    dprint("Welcome to Jovian Josh's first RPG Game!", style = "bold cyan")
    dprint("Select the options below if you want to know more about the game:", style = "bold yellow")
    dprint("1. Buffs", style = "green")
    dprint("2. Debuffs", style = "magenta")
    dprint("3. Character Attributes", style = "blue")
    dprint("4. Boss Attributes", style = "bright_red")
    dprint("5. I understand it now", style = "bold yellow")

    while True:
      try:
            choice = int(input("Choose an option (1-5): "))
            dprint('')

            if choice == 1:
                dprint("Buffs:", style = "bold green")
                dprint("- Defense Up: Increases defense by 2x.", style = "green")
                dprint("- Attack Up: Increases attack power by 1.5x.", style = "green")
                dprint("- Crit Rate Up: Increases critical rate by 25%.", style = "green")
                dprint("- Crit Damage Up: Increases critical damage by 25%.", style = "green")
                dprint("- Immunity: Grants immunity towards debuffs.", style = "green")
                dprint("\nPress any key to return to the menu...", style = "bright_white")
                keyboard.read_key()

            elif choice == 2:
                dprint("Debuffs:", style = "bold magenta")
                dprint("- Defense Break: Reduces defense by half.", style = "magenta")
                dprint("- Attack Down: Reduces attack power by half.", style = "magenta")
                dprint("- Critical Down: Reduces crit rate and crit damage by 25%.", style = "magenta")
                dprint("- Blind: Reduces Accuracy by 50%", style = 'magenta')
                dprint("\nPress any key to return to the menu...", style = "bright_white")
                keyboard.read_key()

            elif choice == 3:
                dprint("Character Attributes:\n", style = "bold blue")
                dprint("Note: every character's normal attack is equal to its Attack Power\n", style = "cyan")

                dprint("Fighter:", style = "bold yellow")
                dprint("Skill: Attack all enemies with AOE damage by 100.", style = "white")
                dprint('')
                
                dprint("Mage:", style = "bold yellow")
                dprint("Skill: Attack a random enemy with intelligence if MP is sufficient.", style = "white")
                dprint("If MP is not sufficient, Mage will heal MP by 30.", style = "white")
                dprint('')
                
                dprint("Berserker:", style = "bold yellow")
                dprint("Skill: Attack all enemies with AOE damage.", style = "white")
                dprint("Passive: Damage doubles when HP falls below 50%.", style = "green")
                dprint('')
                
                dprint("ArchMage:", style = "bold yellow")
                dprint("Skill: Attack all enemies with AOE damage (1200/total alive enemies), ignores 50 defense if the target if boss", style = "white")
                dprint("If MP is not sufficient, heals MP by 30.", style = "white")
                dprint('')
                
                dprint("Necromancer:", style = "bold yellow")
                dprint("Skill: Revive a teammate with half of their max HP.", style = "white")
                dprint("If MP is not sufficient, heals MP by 30.", style = "white")
                dprint('')
                
                dprint("Assassin:", style = "bold yellow")
                dprint("Skill: Increases Crit Rate (+30%) and Crit Damage (+50%).", style = "white")
                dprint("Passive: Prioritizes glasscannon units, deals double damage to bosses and glasscannon units.", style = "green")
                dprint('')
                
                dprint("Paladin:", style = "bold yellow")
                dprint("Skill: AOE damage (5x Defense + 100).", style = "white")
                dprint("Passive: Increases defense by 5 every attack.", style = "green")
                dprint('')
                
                dprint("Cleric:", style = "bold yellow")
                dprint("Skill: Heal all allies by 200 if MP is sufficient.", style = "white")
                dprint("Passive: Drain HP when Cleric is the last unit alive.", style = "green")
                dprint('')
                
                dprint("Archer:", style = "bold yellow")
                dprint("Skill: Attack all enemies with AOE damage (random arrows: 1 or 2).", style = "white")
                dprint("If the target is boss, deal damage equivalent to 20% of its maxhp", style = 'green')
                dprint('')
                
                dprint("Minstrel:", style = "bold yellow")
                dprint("Skill: Apply random buffs to all allies.", style = "white")
                dprint("Passive: Casts a powerful magic dealing 3x INT if alone.", style = "green")
                dprint('')
                
                dprint("Monk:", style = "bold yellow")
                dprint("Skill: Sacrifices 400 HP to apply lifesteal buff.", style = "white")
                dprint("Passive: Every 3 attacks, reduces enemy's defense.", style = "green")
                dprint('')
                
                dprint("Bishop:", style = "bold yellow")
                dprint("Skill: AOE attack with a chance to apply Blind debuff (once per game).", style = "white")
                dprint("After using, acts as a Cleric, but heal can cleanse debuff", style = "green")
                dprint('')

                dprint("Alchemist:", style = "bold yellow")
                dprint("Skill: AOE attack that applies random kind of debuff to all enemy.", style = "white")
                dprint("Damage increase based on enemy's debuff count.", style = "green")
                dprint('')

                dprint("Gladiator:", style = "bold yellow")
                dprint("Skill: AOE attack that removes the enemy's buff.", style = "white")
                dprint("Passive: Berserk (same as berserker.", style = "green")
                dprint('')

                char_stat(classes)
                dprint('')    
                dprint("\nPress any key to return to the menu...", style = "bright_white")
                keyboard.read_key()

            elif choice == 4:
              dprint("Boss Attributes: ", style = "bold blue")
              dprint('')
              char_stat(bosses)
              dprint('')
              dprint("Boss's phase detail wont be shown") 
              dprint('')
              
              dprint("Orpheus: ", style = 'bold yellow')
              dprint("Skill: same as Alchemist", style = 'white')
              dprint("Passive: Normal attack hits every ally, damage scales according to number of allies alive", style = 'green')
              dprint('')

              dprint("Gawain: ", style = 'bold yellow')
              dprint("Skill: cleanse defense break, then attacks normally", style = 'white')
              dprint("Passive: Ignore defense", style = 'green')

            elif choice == 5:
                dprint("Press ENTER to START...", style = "bold cyan")
                keyboard.read_key()
                game_start(GOLD, True)
                break

            else:
                dprint("Invalid option. Please choose a number between 1 and 4.", style = "bold red")
      except ValueError:
        dprint("Invalid option. Please choose a number between 1 and 4.", style = "bold red")


while True:
    press_to_start()
    dprint('Play again?')
    dprint('1. Yes')
    dprint('2. No')
    
    try:
        choice = int(input("Choose an option (1 or 2): "))
        dprint('')
        if choice == 1:
            continue
        elif choice == 2:
            dprint("Thanks for playing!")
            dprint('Press ENTER to EXIT')
            input()
            break
        else:
            dprint('Invalid input. Please choose 1 or 2.')
    except ValueError:
        dprint('Invalid input. Please enter a number.')
