import pyautogui, sys
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'x: ' + str(x).rjust(4) + ' y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except:
    print('\n')

# for i in range(210, 1825, 161):
#     print(i)