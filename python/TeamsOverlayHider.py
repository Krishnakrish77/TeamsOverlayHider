from pyautogui import size, position
import pygetwindow as gw
import keyboard 
import time
import threading
from winsound import Beep
import pystray
from PIL import Image, ImageDraw
from os import _exit

toggle = True
running = True

def create_image():
    width = 64
    height = 64
    color1 = "white"
    color2 = "red"

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [(width // 2, 0), (width, height // 2)],
        fill=color2
    )
    dc.rectangle(
        [(0, height // 2), (width // 2, height)],
        fill=color2
    )
    return image

def watch_mouse():
    global toggle, running
    while running:
        if toggle:
            xpos, ypos = position()
            screen_width, screen_height = size()

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
                pass

        time.sleep(0.1)

# def show_tooltip(message):
#     pyautogui.alert(text=message, title='Notification', button='OK')

def beep_sound():
    Beep(800, 200)

def notify_user(message):
    # show_tooltip(message)
    beep_sound()

def toggle_overlay(icon, item):
    global toggle
    toggle = not toggle
    icon.update_menu()
    if toggle:
        notify_user("Overlay control enabled")
    else:
        notify_user("Overlay control disabled")

def on_quit(icon, item):
    global running
    running = False
    icon.stop()
    # Properly terminate the program
    _exit(0)

def setup(icon):
    icon.visible = True
    threading.Thread(target=watch_mouse, daemon=True).start()
    keyboard.add_hotkey('ctrl+;', lambda: toggle_overlay(icon, None))

def main():
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem(lambda item: "Enabled" if toggle else "Disabled", lambda icon, item: toggle_overlay(icon, item)),
        pystray.MenuItem('Exit', on_quit)
    )
    icon = pystray.Icon("Teams Overlay Control", image, "Overlay Control", menu)
    icon.run(setup)

if __name__ == "__main__":
    main()
