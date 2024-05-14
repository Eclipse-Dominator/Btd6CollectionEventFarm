from time import sleep
import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image

from pynput import mouse, keyboard

h_mouse = mouse.Controller()
h_keyboard = keyboard.Controller()

PYNPUT_MOUSE_DELAY = .1
PYNPUT_KEYBOARD_DELAY = .05

def click(xy: tuple[int, int], left_click=True):
  h_mouse.position = xy
  h_mouse.click(mouse.Button.left if left_click else mouse.Button.right)
  sleep(PYNPUT_MOUSE_DELAY)

def press_key(key):
  h_keyboard.tap(key)
  sleep(PYNPUT_KEYBOARD_DELAY)

def get_window_rect(hwnd):
    client_rect = win32gui.GetClientRect(hwnd)
    window_rect = win32gui.GetWindowRect(hwnd)
    # Convert client area dimensions to window dimensions
    window_width = client_rect[2] - client_rect[0]
    window_height = client_rect[3] - client_rect[1]

    win_margin = ((window_rect[2] - window_rect[0]) - (client_rect[2] - client_rect[0])) // 2
    border_height = (window_rect[3] - window_rect[1]) - (client_rect[3] - client_rect[1]) - win_margin
    
    # Calculate the position of the top-left corner of the borderless window
    left = window_rect[0] + win_margin
    top = window_rect[1] + border_height

    return left, top, window_width, window_height

def background_screenshot(hwnd, w, h) -> Image.Image:
  hwndDC = win32gui.GetWindowDC(hwnd)
  mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
  saveDC = mfcDC.CreateCompatibleDC()

  saveBitMap = win32ui.CreateBitmap()
  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
  saveDC.SelectObject(saveBitMap)

  result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

  bmpinfo = saveBitMap.GetInfo()
  bmpstr = saveBitMap.GetBitmapBits(True)

  im = Image.frombuffer(
      'RGB',
      (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
      bmpstr, 'raw', 'BGRX', 0, 1)

  win32gui.DeleteObject(saveBitMap.GetHandle())
  saveDC.DeleteDC()
  mfcDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, hwndDC)

  if result == 0:
    raise Exception("Failed to take screenshot")
  return im

def getWindowInfo(title):
  hwnd = win32gui.FindWindow(None, title)
  setWindowToForeground(hwnd)
  return hwnd, *get_window_rect(hwnd)

def setWindowToForeground(hwnd):
  try:
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
  except Exception as e:
    print("Failed to restore window:", e)
    print("Ignoring...")
  win32gui.SetForegroundWindow(hwnd)
