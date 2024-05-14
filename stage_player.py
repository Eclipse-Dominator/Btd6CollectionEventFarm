'''
Plays, complete and exit the stage to main menu
'''

from keylog_replay import make_instruction, read_keylog, run_instruction, make_setting
from utils import locate_by_white, find_img, wait_til_exists, focus_game, sleep, r2a, g_x, g_y, g_w, g_h
from os_utils import click, press_key
from pynput.keyboard import Key
from datetime import datetime
import assets as img

def restart_stage():
  focus_game()
  while not(pos := find_img(img.restart_btn_icon)):
    press_key(Key.esc)
    sleep(.6)
  
  click(r2a(pos))
  click(r2a(wait_til_exists(img.restart_icon)))
  wait_til_exists(img.stage_loaded_check_icon)

def resume_stage():
  focus_game()
  press_key(Key.esc)
  sleep(1)
  press_key(Key.esc)
  sleep(.5)
  press_key(Key.esc)

def run_stage(record_path, verbosity=1, post_ins_sleep=120):
  window_setting = make_setting(datetime.now(), (g_x, g_y), (g_w, g_h))
  setting, map_name, data = read_keylog(f"lvl_recordings/{record_path}")
  instructions = make_instruction(data, setting)
  # ensure window is focused
  focus_game()
  run_instruction(instructions, window_setting, verbosity)
  if verbosity:
    print("\033[Kwaiting for completion", end="\r" if verbosity == 1 else "\n")
  sleep(post_ins_sleep)

def check_completion():
  if find_img(img.success_next_icon):
    print("\033[KStage completed!")
    return True
  if find_img(img.defeat_icon):
    raise Exception("Stage failed, restarting...")
  if find_img(img.level_up_icon):
    resume_stage()
  return False

def return_to_home():
  focus_game()
  for _ in range(3):
    try:
      click(r2a(wait_til_exists(img.success_next_icon)))
      click(r2a(wait_til_exists(img.success_home_icon)))
      break
    except Exception as e:
      print(e)

  sleep(4) # leave 5 sec buffer for collection of instas to appear
  
  if pos := find_img(img.collect_icon):
    collect_instas(pos)

def collect_instas(continue_pos):
  click(r2a(continue_pos))
  wait_til_exists(img.insta_icon, mode_bw=True) # wait for insta icon to appear
  print("Collecting instas")
  while pos:=locate_by_white(img.insta_icon):
    click(r2a(pos))
    sleep(1)
    click(r2a(pos))
    sleep(1)
  
  click(r2a(wait_til_exists(img.reward_continue_icon)))
  click(r2a(wait_til_exists(img.back_icon)))

if __name__ == "__main__":
  return_to_home()
  # run_stage("INFERNAL")

# print("checking...", find_img(success_next_icon))
