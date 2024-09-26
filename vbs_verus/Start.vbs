Set shell = CreateObject("WScript.Shell")
d=Day(Date)

s=InputBox("Password:")
if s <> "virus" Then
X=MsgBox("WRONG",0,"")
X=MsgBox("",0,"")
X=MsgBox("",2,"")
WScript.Sleep 2000
X=MsgBox("",2,"")
X=MsgBox("",2,"")

WScript.Sleep 1000
shell.run "mspaint"
WScript.Sleep 1000
shell.run "explorer"
WScript.Sleep 1000
shell.run "calc"
WScript.Sleep 1000
shell.run "write"
WScript.Sleep 1000
shell.run "notepad"
WScript.Sleep 4000

X=MsgBox("Malware has been detected. Windows Defender will attempt to deactivate it.",48+0,"Windows Defender")

WScript.Sleep 3000
X=MsgBox("The virus could not be deactivated.",16+0,"Windows Defender")
X=MsgBox("Starting Virus Removal Tool.",64+0,"Windows Defender")
Wscript.Sleep 2000
shell.Run "verus.bat"
End If
if s = "virus" Then
X=MsgBox("YOU WIN!!! :)",64+0,"BRAVO")
End If