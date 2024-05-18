import pyautogui
import pygetwindow as gw
import keyboard
import time
import threading
import winsound

toggle = True

def watch_mouse():
    global toggle
    while True:
        if toggle:
            xpos, ypos = pyautogui.position()
            screen_width, screen_height = pyautogui.size()

            in_top_center = ypos < 20 and (screen_width / 2 - 50) < xpos < (screen_width / 2 + 50)

            try:
                overlay_window = gw.getWindowsWithTitle('Sharing control bar | Microsoft Teams')[0]
                oxpos, oypos = overlay_window.left, overlay_window.top
                owidth, oheight = overlay_window.width, overlay_window.height

                overlay_under_mouse = oxpos <= xpos <= (oxpos + owidth) and oypos <= ypos <= (oypos + oheight)

                if in_top_center or overlay_under_mouse:
                    overlay_window.restore()
                else:
                    overlay_window.minimize()
            except IndexError:
                pass  # Window not found

        time.sleep(0.1)

# def show_tooltip(message):
#     pyautogui.alert(text=message, title='Notification', button='OK')

def beep_sound():
    winsound.Beep(800, 200)  # Beep at 1000 Hz for 500 ms

def notify_user(message):
    # show_tooltip(message)
    print(message)
    beep_sound()

def toggle_overlay():
    global toggle
    toggle = not toggle
    if toggle:
        notify_user("Overlay control enabled")
    else:
        notify_user("Overlay control disabled")

def main():
    threading.Thread(target=watch_mouse, daemon=True).start()
    keyboard.add_hotkey('ctrl+;', toggle_overlay)

    print("Press Ctrl + ; to toggle overlay control.")
    keyboard.wait('esc')  # Keep the script running until 'esc' is pressed

if __name__ == "__main__":
    main()
