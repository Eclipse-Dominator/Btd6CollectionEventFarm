'''
This is a simple keylogger that logs the mouse clicks and keyboard inputs.
The main purpose is for users to record their actions and replay them later.
The keylogger starts recording when the left alt key is pressed and stops when the esc key is pressed.

To record btd6 gameplay
1. the user can press the left alt key to start recording, then play the game.
2. After the game is finished, the user can press the esc key to stop recording.
3. The user should run ./utils to find out the window dimension and coordinate.
4. The user should then add the out put of the prev line to the top of the logged file
Note: this recorder only supports click and keyboard press.
Thus, the user should only use keyboard to place down the towers.
'''

from pynput.mouse import Listener
from pynput.keyboard import Listener as Listener2, Key
import logging

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
record = False

def on_move(x, y):
    # logging.info("Mouse moved to ({0}, {1})".format(x, y))
    pass

def on_click(x, y, button, pressed):
    if pressed and record:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    # logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    pass

def on_release(key):
    global record
    print(key)
    # start if enter is pressed
    if key == Key.alt_l:
        print("Recording...")
        logging.info('Recording started!')
        record = True
        return
    # stop if esc is pressed
    if key == Key.esc:
        print('Exiting...')
        exit(0)
    if record:
      logging.info('Key released: {0}'.format(key))

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll), Listener2(on_release=on_release) as listener:
    listener.join()