'''
Handles converting game recordings to chainable instructions to replay the recording
'''

#recording is done in 1280x720
from datetime import datetime, timedelta
from time import sleep
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller
from re import match
keyboard = Controller()
mouse = MouseController()

key_map = {
  "Key.enter": Key.enter,
  "Key.esc": Key.esc,
  "Key.space": Key.space,
  "Key.shift": Key.shift,
  "Key.ctrl": Key.ctrl,
  "Key.backspace": Key.backspace,
  "Key.tab": Key.tab
}

def read_keylog(file):
  with open(file, 'r') as f:
    lines = f.read().strip().split('\n')

  # setting = start_time: xxx, win_x: xxx, win_y: xxx, wh: xxx
  setting, map_name = lines[0].split(",")
  setting = [int(x) for x in setting.split(" ")]
  data = [line.split(": ") for line in lines[1:]]
  return setting, map_name, data


def wait_until(time):
  def tmp(i,setting, verbosity):
    target_time = setting["start_time"] + timedelta(seconds = time)
    wait_time = (target_time - datetime.now()).total_seconds()
    left = wait_time
    while left > 0:
        if left > 2:
            print(f"\033[Kins {i}: next ins in {int(left)}s", end='\r')
            sleep(1)
        left = (target_time - datetime.now()).total_seconds()
    if verbosity > 0:
      print(f"\033[Kins {i}: Waited for {wait_time} to run ", end='')
  return tmp

def click(pos_x,pos_y, r_wh):
  r_w,r_h = r_wh
  def tmp(i,setting,verbosity):
    w,h = setting["wh"]
    x = pos_x / r_w * w
    y = pos_y / r_h * h
    if verbosity > 0:
      print(f"click ({x}, {y})", end='\n' if verbosity > 1 else '\r')
    loc_x = int(x + setting["win_pos"][0])
    loc_y = int(y + setting["win_pos"][1])
    mouse.position = (loc_x,loc_y)
    mouse.click(Button.left)
  return tmp

def keypress(key):
  btn = key_map.get(key, key[1])
  def tmp(i,setting,verbosity):
    if verbosity > 0:
      print(f"press '{btn}'", end='\n' if verbosity > 1 else '\r')
    keyboard.press(btn)
    keyboard.release(btn)
  return tmp

def make_instruction(data, setting):
  g_x,g_y,g_w,g_h = setting
  translate = lambda x,y: (x - g_x, y - g_y)
  to_time = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S,%f')

  instructions = []

  recording_start_time = to_time(data[0][0])

  for line in data[1:]:
    t = (to_time(line[0]) - recording_start_time).total_seconds()
    instructions.append(wait_until(t))
    if len(line) == 3:
      # keypress
      instructions.append(keypress(line[2]))
    else:
      # find (x, y) in line with regex
      m = match(r".*\((\d+), (\d+)\).*", line[1])
      x,y = int(m.group(1)), int(m.group(2))
      x,y = translate(x,y)
      instructions.append(click(x,y, (g_w, g_h)))

  return instructions

def make_setting(s_time, win_pos, wh):
  return {
    "start_time": s_time,
    "win_pos": win_pos,
    "wh": wh
  }

def run_instruction(ins, setting, verbosity=1):
  for i, fn in enumerate(ins):
    fn(1 + (i//2), setting, verbosity) # timer is part of the instruction
  print(f"\033[K{len(ins)//2} instructions complete!")

if __name__ == "__main__":
  log_location = "keylog.txt"
  setting, map_name, data = read_keylog(log_location)
  ins = make_instruction(data, setting)
  run_instruction(ins, make_setting(*setting), verbosity=1)
  print(f"Instructions for {map_name} complete!")