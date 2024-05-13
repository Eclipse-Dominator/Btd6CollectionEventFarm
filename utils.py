import pyautogui
from PIL import Image
from win32gui import GetClientRect, GetWindowRect
from time import sleep

def get_window_rect(hwnd):
    client_rect = GetClientRect(hwnd)
    window_rect = GetWindowRect(hwnd)
    # Convert client area dimensions to window dimensions
    window_width = client_rect[2] - client_rect[0]
    window_height = client_rect[3] - client_rect[1]

    win_margin = ((window_rect[2] - window_rect[0]) - (client_rect[2] - client_rect[0])) // 2
    border_height = (window_rect[3] - window_rect[1]) - (client_rect[3] - client_rect[1]) - win_margin
    
    # Calculate the position of the top-left corner of the borderless window
    left = window_rect[0] + win_margin
    top = window_rect[1] + border_height

    return left, top, window_width, window_height

game_window = pyautogui.getWindowsWithTitle('BloonsTD6')
g_x,g_y,g_w,g_h = get_window_rect(game_window[0]._hWnd)
print(f"{g_x}, {g_y}, {g_w}, {g_h},BloonsTD6")

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

def resize_img(img, scale):
  return img.resize((int(img.width * scale), int(img.height * scale)))

def rel_to_abs(rel_pos) -> tuple[int, int]:
  '''
  Convert relative position to absolute position of a xy coordinate
  '''
  return (int(rel_pos[0] + g_x), int(rel_pos[1] + g_y))

r2a = rel_to_abs

def get_game_ss() -> Image.Image:
  '''
  Get screenshot of the current game window
  '''
  game_ss = pyautogui.screenshot(region=(g_x, g_y, g_w, g_h))
  
  return game_ss

def find_img(img) -> tuple[int, int]:
  '''
  Find the position of the image in the game window
  '''
  pyautogui.moveTo(g_x, g_y)
  game_ss = get_game_ss()
  try:
    return pyautogui.locate(img, game_ss, grayscale=True, confidence=0.82)
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