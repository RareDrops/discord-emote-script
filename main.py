from pynput import keyboard
from pynput.keyboard import Key, Controller
from os.path import exists
import win32clipboard
import os
from PIL import Image
from pystray import Icon as icon, Menu, MenuItem as item
import pystray

RECORDING = False
WORD = ""
keyboard_press = Controller()

def send_to_clipboard(filepath):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    #the two lines of code below only works for some programs, does work on disocrd though(it is to preserve transparency)
    wide_path = os.path.abspath(filepath).encode('utf-16-le') + b'\0'
    win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat('FileNameW'), wide_path)
    win32clipboard.CloseClipboard()
    #then simulates pressing ctrl+v using the keyboard module:
    keyboard_press.release(Key.shift_r)
    with keyboard_press.pressed(Key.ctrl):
        keyboard_press.press('v')
        keyboard_press.release('v')
    keyboard_press.press(Key.backspace)
    keyboard_press.release(Key.backspace)
    
def find_image(word):
    filepath = f"Emotes/{word.lower()}.png"
    file_exist = exists(filepath)
    if file_exist == False:
        return
    image = Image.open(filepath)
    if image.size != (48, 48):
        image = image.resize((48, 48))
        image.save(filepath)
    send_to_clipboard(filepath)


def on_press(key):
    global RECORDING, WORD
    try:
        if key.char == ':':
            if RECORDING == False:
                RECORDING = True
            else:
                RECORDING = False
                find_image(WORD)
                WORD = ""
        elif RECORDING == True:
                WORD += key.char
                if len(WORD) > 30:
                    RECORDING = False
                    WORD = ""
    except AttributeError:
        if RECORDING == True:
            if key == Key.backspace:
                WORD = WORD[:-1]
            elif key == Key.enter:
                RECORDING = False
                WORD = ""

# Collect events until released
listener = keyboard.Listener(on_press=on_press)
listener.start()
temp_iterable = []
image = Image.open('keyboard.ico')
icon = pystray.Icon('discord-emotes',image,'discord-emotes',temp_iterable)
menu = Menu(item('quit',lambda : icon.stop()),)
icon.menu = menu
icon.run()






