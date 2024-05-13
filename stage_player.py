'''
Plays, complete and exit the stage to main menu
'''

from keylog_replay import make_instruction, read_keylog, run_instruction, make_setting
from utils import locate_by_white, find_img, wait_til_exists, focus_game, sleep, r2a, g_x, g_y, g_w, g_h
from datetime import datetime
from assets import success_next_icon, success_home_icon, collect_icon, insta_icon, reward_continue_icon, back_icon, defeat_icon, level_up_icon, restart_icon, restart_btn_icon, overwrite_ok_icon, stage_loaded_check_icon
import pyautogui
from pynput.keyboard import Key, Controller

def restart_stage():
  keyboard = Controller()
  while not(pos := find_img(restart_btn_icon)):
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    sleep(1)
  
  pyautogui.click(r2a(pos))
  pyautogui.click(r2a(wait_til_exists(restart_icon)))
  wait_til_exists(stage_loaded_check_icon)

def resume_stage():
  keyboard = Controller()
  keyboard.press(Key.esc)
  keyboard.release(Key.esc)
  sleep(1)
  keyboard.press(Key.space)
  keyboard.release(Key.space)
  sleep(.5)
  keyboard.press(Key.space)
  keyboard.release(Key.space)


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
  if find_img(success_next_icon):
    print("\033[KStage completed!")
    return True
  if find_img(defeat_icon):
    raise Exception("Stage failed, restarting...")
  if find_img(level_up_icon):
    resume_stage()
  return False

def return_to_home():
  pyautogui.click(r2a(wait_til_exists(success_next_icon)))
  pyautogui.click(r2a(wait_til_exists(success_home_icon)))
  sleep(5) # leave 5 sec buffer for collection of instas to appear
  if pos := find_img(collect_icon):
    collect_instas(pos)

def collect_instas(continue_pos):
  pyautogui.click(r2a(continue_pos))
  wait_til_exists(insta_icon, mode_bw=True) # wait for insta icon to appear
  print("Collecting instas")
  while pos:=locate_by_white(insta_icon):
    pyautogui.click(r2a(pos))
    sleep(1)
    pyautogui.click(r2a(pos))
    sleep(1)
  
  pyautogui.click(r2a(wait_til_exists(reward_continue_icon)))
  pyautogui.click(r2a(wait_til_exists(back_icon)))

if __name__ == "__main__":
  run_stage("INFERNAL")

# print("checking...", find_img(success_next_icon))
