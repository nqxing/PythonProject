import pyautogui as pg
import time
# pg.hotkey('winleft', 'd')
# time.sleep(0.5)
# pg.doubleClick(114, 863)
# # pg.moveTo(114, 863)
# # pg.click()
# time.sleep(3)
# pg.hotkey('ctrl', 't')
# pg.write("https://h5.ele.me/login/#redirect=https%3A%2F%2Fh5.ele.me%2Fprofile%2F")
# pg.press('enter')
# pg.press('enter')

# pg.click(708, 1059)
# pg.moveTo(713,597,2)
# for i in range(713, 851):
#     pg.dragTo(i, 597, button='left')
pg.click(647, 1060)
time.sleep(1)
pg.moveTo(210,558, 2)
pg.mouseDown()
for i in range(210, 1825, 161):
    pg.moveTo(i, 558, duration=1)
    # pg.dragTo(i, 558, button='left')
pg.mouseUp()

# time.sleep(1)
# pg.dragTo(210, 1825, button='left')
# pg.moveTo(210,1825,2)