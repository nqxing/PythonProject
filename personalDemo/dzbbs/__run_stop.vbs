function getfolder() 
getfolder=left(wscript.scriptfullname,instrrev(wscript.scriptfullname,"\")-1) 
end function
function runStop()
Set oShell = WScript.CreateObject ("WSCript.shell")
oShell.run "python "+getfolder()+"\__stop.py"
Set oShell = Nothing
end function
Function IsExitAFile(filespec)
        Dim fso
        Set fso=CreateObject("Scripting.FileSystemObject")        
        If fso.fileExists(filespec) Then         
        IsExitAFile=True        
        Else IsExitAFile=False        
        End If
End Function
Sub DeleteAFile(filespec)
        Dim fso
        Set fso= CreateObject("Scripting.FileSystemObject")
        fso.DeleteFile(filespec)
End Sub
If IsExitAFile(getfolder()+"\__����������.txt") Then
runStop()
DeleteAFile(getfolder()+"\__����������.txt")
Else
Msgbox "����δ���У�����ر�~~"
End If


