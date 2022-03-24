import pyautogui

pyautogui.PAUSE = 6

def main():
    ffx, ffy = pyautogui.locateCenterOnScreen('img/firefoxHomeScreen.png')
    pyautogui.moveTo(ffx, ffy, duration=4)
    pyautogui.doubleClick()

if __name__ == "__main__":
    main()