from pynput import keyboard
from time import sleep

global keyCapture
keyCapture = -1

def on_press(key):
    global keyCapture
    try:
        keyCapture = 'alphanumeric key {0} pressed'.format(key.char)
        print(keyCapture)
    except AttributeError:
        keyCapture = 'special key {0}'.format(key)
        print(keyCapture)

def on_release(key):
    global keyCapture 
    keyCapture = '{0} released'.format(key)
    print(keyCapture)

# Collect events until released
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()
#     print("Doing the thing", keyCapture)
#     sleep(0.25)
logger = keyboard.Listener(on_press=on_press, on_release=on_release)
logger.start()
i=0
while i<50:
    sleep(0.1)
    print(keyCapture)
    i+=1

print("Stopping Keylogger")
logger.stop()
#exit()
