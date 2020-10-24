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
If IsExitAFile(getfolder()+"\__服务已启动.txt") Then
runStop()
DeleteAFile(getfolder()+"\__服务已启动.txt")
Else
Msgbox "程序未运行，无需关闭~~"
End If


