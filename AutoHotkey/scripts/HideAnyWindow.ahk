#InstallKeybdHook
#Persistent
#HotkeyInterval,100
#NoEnv
SetKeyDelay, –1
SetTitleMatchMode, 2 ; Makes matching the titles easier
SendMode Input
SetWorkingDir %A_ScriptDir%
 
<^CapsLock:: ; Press left control + capslock to hide
{
WinHide, Google Chrome ; Place desired window title instead of Google Chrome
Return
}
 
<+CapsLock:: ; press left shift + capslock to reveal
{
DetectHiddenWindows, On
WinShow, Google Chrome
Return
}