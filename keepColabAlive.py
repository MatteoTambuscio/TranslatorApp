import time
from pynput.mouse import Controller ,Button

MouseClick = Controller()

k=0
while True:

    MouseClick.click(Button.left, 1)
    k=k+1
    print(k)
    time.sleep(20)
