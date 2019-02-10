;[Acc functions]
;Acc library (MSAA) and AccViewer download links - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?f=6&t=26201
;tested on Windows 7
q:: ;Explorer window/Desktop - get name of file under cursor
oAcc := Acc_ObjectFromPoint(vChildID)
MouseGetPos,,, hWnd, vCtlClassNN
WinGetClass, vWinClass, % "ahk_id " hWnd
vText := ""
if (vWinClass = "CabinetWClass") || (vWinClass = "ExploreWClass")
try vText := oAcc.accValue(vChildID)
else if (vWinClass = "Progman") || (vWinClass = "WorkerW")
try vText := oAcc.accName(vChildID)
MsgBox, % vText
oAcc := ""
return