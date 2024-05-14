import pyautogui
from PIL import Image
from win32gui import SetForegroundWindow
from time import sleep
from winapi_utils import background_screenshot, getWindowInfo
from pynput.mouse import Button, Controller


EXPERT_MAP_POS = {
  (0,0,0): "GLACIAL TRAIL",
  (0,0,1): "DARK DUNGEONS",
  (0,0,2): "SANCTUARY",
  (0,1,0): "RAVINE",
  (0,1,1): "FLOODED VALLEY",
  (0,1,2): "INFERNAL",
  (1,0,0): "BLOODY PUDDLES",
  (1,0,1): "WORKSHOP",
  (1,0,2): "QUADS",
  (1,1,0): "DARK CASTLE",
  (1,1,1): "MUDDY PUDDLES",
  (1,1,2): "OUCH"
}

hwnd, g_x,g_y,g_w,g_h = getWindowInfo('BloonsTD6')
print(f"{g_x}, {g_y}, {g_w}, {g_h},BloonsTD6")

mouse = Controller()

def click(xy):
  mouse.position = (xy[0], xy[1])
  mouse.press(Button.left)
  mouse.release(Button.left)
  sleep(.1) # let windows process the click

def focus_game():
  SetForegroundWindow(hwnd)

def resize_img(img, scale):
  return img.resize((int(img.width * scale), int(img.height * scale)))

def rel_to_abs(rel_pos) -> tuple[int, int]:
  '''
  Convert relative position to absolute position of a xy coordinate
  '''
  return (int(rel_pos[0] + g_x), int(rel_pos[1] + g_y))

r2a = rel_to_abs

def get_game_ss(retries=3) -> Image.Image:
  '''
  Get screenshot of the current game window
  '''
  for _ in range(retries):
    try:
      return background_screenshot(hwnd, g_w, g_h)
    except Exception as e:
      pass

  raise Exception("Failed to take screenshot:", e)

def find_img(img) -> tuple[int, int]:
  '''
  Find the position of the image in the game window
  '''
  if (g_x, g_y) < mouse.position < (g_x + g_w, g_y + g_h):
    # move the mouse out of the game window if it is in the game window
    mouse.position = g_x + g_w, g_y + g_h
  game_ss = get_game_ss()
  try:
    s = pyautogui.locate(img, game_ss, grayscale=True, confidence=0.82)
    return s
  except Exception as e:
    return None


def wait_til_exists(img, sleep_time=3, mode_bw=False):
  '''
  wait until the image is found in the game window
  '''
  if mode_bw:
    while not (pos:=locate_by_white(img)):
      sleep(sleep_time)
    return pos

  while not (pos:=find_img(img)):
    sleep(sleep_time)
  
  return pos

def locate_by_white(img):
  '''
  compare near white parts of a image
  '''
  game_ss = get_game_ss()
  game_ss = game_ss.convert('L').point(lambda x: 255 if x > 250 else 0)
  img = img.convert('L').point(lambda x: 255 if x > 250 else 0)
  try:
    pos = pyautogui.locate(img, game_ss, grayscale=True, confidence=0.70)
  except Exception as e:
    pos = None
  return pos
