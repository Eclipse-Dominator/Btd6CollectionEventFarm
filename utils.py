import pyautogui
from PIL import Image
from time import sleep, time
from os_utils import background_screenshot, getWindowInfo, setWindowToForeground, h_mouse

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

def focus_game():
  setWindowToForeground(hwnd)

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
  if (g_x, g_y) < h_mouse.position < (g_x + g_w, g_y + g_h):
    # move the mouse out of the game window if it is in the game window
    h_mouse.position = g_x + g_w, g_y + g_h
  game_ss = get_game_ss()
  try:
    s = pyautogui.locate(img, game_ss, grayscale=True, confidence=0.80)
    return s
  except Exception as e:
    return None


def wait_til_exists(img, sleep_time=3, timeout=10, mode_bw=False):
  '''
  wait until the image is found in the game window
  '''
  start = time()
  while not (pos:=locate_by_white(img) if mode_bw == 'bw' else find_img(img)):
    sleep(sleep_time)
    if time() - start > timeout:
      raise Exception("Time out while trying to find image")
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
