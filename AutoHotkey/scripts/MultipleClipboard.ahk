; Hotkeys
<#c::Copy(1) ; Place your desired key before the colons
<#v::Paste(1)
 
<!c::Copy(2)
<!v::Paste(2)
 
>!c::Copy(3)
>!v::Paste(3) ; You can have as many of these as you want
 
 
Copy(clipboardID)
{
    global ; All variables are global by default
    local oldClipboard := ClipboardAll ; Save the (real) clipboard
   
    Clipboard = ; Erase the clipboard first, or else ClipWait does nothing
    Send ^c
    ClipWait, 2, 1 ; Wait 1s until the clipboard contains any kind of data
    if ErrorLevel
    {
        Clipboard := oldClipboard ; Restore old (real) clipboard
        return
    }
   
    ClipboardData%clipboardID% := ClipboardAll
   
    Clipboard := oldClipboard ; Restore old (real) clipboard
}
 
Cut(clipboardID)
{
    global ; All variables are global by default
    local oldClipboard := ClipboardAll ; Save the (real) clipboard
   
    Clipboard = ; Erase the clipboard first, or else ClipWait does nothing
    Send ^x
    ClipWait, 2, 1 ; Wait 1s until the clipboard contains any kind of data
    if ErrorLevel
    {
        Clipboard := oldClipboard ; Restore old (real) clipboard
        return
    }
    ClipboardData%clipboardID% := ClipboardAll
   
    Clipboard := oldClipboard ; Restore old (real) clipboard
}
 
Paste(clipboardID)
{
    global
    local oldClipboard := ClipboardAll ; Save the (real) clipboard
 
    Clipboard := ClipboardData%clipboardID%
    Send ^v
 
    Clipboard := oldClipboard ; Restore old (real) clipboard
    oldClipboard =
}
 
; Works with text and files, sometimes but not always with images