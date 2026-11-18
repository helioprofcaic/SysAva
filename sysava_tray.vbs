' Abre a bandeja do SysAva sem janela de console.
' Usado pelo atalho criado por: sysava_tray.ps1 -Instalar
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
base = fso.GetParentFolderName(WScript.ScriptFullName)
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & base & "\sysava_tray.ps1"""
sh.Run cmd, 0, False
