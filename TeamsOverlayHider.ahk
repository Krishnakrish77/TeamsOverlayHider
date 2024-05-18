#Requires AutoHotkey v2.0

Persistent
toggle := true ; Initialize the toggle flag
SetTimer(WatchMouse, 100)
return

; Ctrl + \ hotkey to toggle the functionality
^;::
{
    global toggle
    toggle := !toggle
    if toggle {
        SetTimer(WatchMouse, 100)
        Tooltip("Overlay control enabled", 5000, 0)
        SetTimer () => ToolTip(), -5000 ; Display a tooltip for 5 seconds
    } else {
        SetTimer(WatchMouse, 0)
        Tooltip("Overlay control disabled", 5000, 0)
        SetTimer () => ToolTip(), -5000 ; Display a tooltip for 5 seconds
    }
return
}

WatchMouse() {
    global toggle
    if !toggle
        return

    xpos := MouseGetPosX()
    ypos := MouseGetPosY()
    ScreenWidth := A_ScreenWidth
    ScreenHeight := A_ScreenHeight

    ; Define the area at the top center of the screen
    inTopCenter := (ypos < 20 && xpos > (ScreenWidth / 2 - 50) && xpos < (ScreenWidth / 2 + 50))
    
    ; Initialize variables for overlay window position and size
    oxpos := 0
    oypos := 0
    owidth := 0
    oheight := 0
    overlayUnderMouse := false

    ; Get overlay window position and size
    if WinExist("Sharing control bar | Microsoft Teams") {
        WinGetPos(&oxpos, &oypos, &owidth, &oheight, "Sharing control bar | Microsoft Teams")
        overlayUnderMouse := (xpos >= oxpos && xpos <= oxpos + owidth && ypos >= oypos && ypos <= oypos + oheight)
    }  

    if (inTopCenter || overlayUnderMouse) {
        ; Show the overlay
        DetectHiddenWindows true
        if WinExist("Sharing control bar | Microsoft Teams") {
            WinShow("Sharing control bar | Microsoft Teams") ; Replace with the actual window title of the overlay
        }
        DetectHiddenWindows false
    } else {
        ; Hide the overlay
        if WinExist("Sharing control bar | Microsoft Teams") {
            WinHide("Sharing control bar | Microsoft Teams") ; Replace with the actual window title of the overlay
        }
    }
}

MouseGetPosX() {
    MouseGetPos(&xpos)
    return xpos
}

MouseGetPosY() {
    MouseGetPos(, &ypos)
    return ypos
}


