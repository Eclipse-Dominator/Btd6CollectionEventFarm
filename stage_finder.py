'''
Handles process of finding and entering expert map with collection bonus
'''

from time import sleep
from utils import *
from assets import reward_icon, toggle_map_icon, map_box, enter_level_select_icon, expert_page_1_icon, easy_icon, start_stage_icon, stage_loaded_check_icon, overwrite_ok_icon

def check_page() -> int:
  '''
  Check if the game is in expert page 1 or page 2
  return: 0 if in page 1, 1 if in page 2
  '''
  return 0 if find_img(expert_page_1_icon) else 1

def pos_to_map(pos) -> str:
  '''
  Convert position of the map with reward icon to the map name
  '''
  row = [g_h/4, g_h/2]
  col = [g_w/2 - map_box.width/2, g_w/2 + map_box.width/2, g_w/2 + map_box.width*3/2]
  
  # find closest (x,y) to pos
  dist_row = list(map(lambda y: abs(y - pos[1]), row))
  dist_col = list(map(lambda x: abs(x - pos[0]), col))

  index = check_page(), min(range(len(dist_row)), key=dist_row.__getitem__), min(range(len(dist_col)), key=dist_col.__getitem__)
  return EXPERT_MAP_POS[index]

def enter_expert_lvl_select() -> bool:
  '''
  Enter expert level select from main menu if not already in it
  return: True if game enters expert_lvl select successfully False otherwise
  '''
  try:
    pos = find_img(enter_level_select_icon)
    click(r2a(pos))
  except Exception as e:
    print(e)
    pass

  try:
    sleep(1)
    pos = find_img(toggle_map_icon)
    click(r2a(pos))
  except Exception as e:
    return False
  return True


def get_reward_stage(retries = 3) -> tuple[str, tuple[int, int]]:
  '''
  Get the stage from the expert map that have collection bonus
  return: (map_name, (x, y))
  '''
  for _ in range(retries):
    sleep(.5)
    if pos := find_img(reward_icon):
      return pos_to_map(pos), pos
    else:
      toggle_map_pos = wait_til_exists(toggle_map_icon)
      click(r2a(toggle_map_pos))
  else:
    raise Exception("Failed to find reward stage")
    
def find_reward_stage_from_start(retries = 5) -> tuple[str, tuple[int, int]]:
  '''
  Find the reward stage from the start of the game
  '''
  for _ in range(retries):
    if enter_expert_lvl_select():
      break
    sleep(0.5)
  else:
    raise Exception("Failed to enter expert level select")

  return get_reward_stage(retries)

def play_stage(pos):
  '''
  Play the stage with the given map name and relative position
  '''
  click(r2a(pos))
  sleep(0.5)
  click(r2a(find_img(easy_icon)))
  sleep(0.5)
  
  click(r2a(find_img(start_stage_icon)))
  sleep(0.5)

  while not find_img(stage_loaded_check_icon):
    if pos := find_img(overwrite_ok_icon):
      click(r2a(pos)) # handles overwrite save scenario
    print("\033[Kwaiting for stage to load...",end='\r')
    sleep(1)
  print("\033[K",end='') # clear line
