from random import randint

def rand_alive(team):
  n = len(team)
  r = randint(0,n-1)
  return r if team[r].alive else rand_alive(team)

def rand_death(team):
  n = len(team)
  r = randint(0,n-1)
  return r if not team[r].alive else rand_death(team) 

def count_alive(team):
  res = 0
  for i in team:
    if i.alive:
      res += 1
  return res

def count_dead(team):
  res = 0
  for i in team:
    if not i.alive:
      res += 1
  return res

def all_dead(team):
  for i in team:
    if i.alive:
      return False
  return True

def all_alive(team):
  for i in team:
    if not i.alive:
      return False
  return True

team_index = {}
def action_turn(team):
    team_id = id(team)
    if team_id not in team_index:
        team_index[team_id] = -1
    while True:
        team_index[team_id] = (team_index[team_id] + 1) % len(team)
        if team[team_index[team_id]].alive:
            return team_index[team_id]

def char_type(itype, team):
    return [i for i in team if i.type == itype and i.alive]

  
