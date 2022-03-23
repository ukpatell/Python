import pyautogui as pg
import time

text = 'Hello from Pihoo and Yukta'
time.sleep(7)               # Allow python some break for the previous message to load
for i in range(5):          # Sends the message 5 times
    pg.write(text)          # Writes the message
    pg.press('enter')       # Presses the enter button to send


