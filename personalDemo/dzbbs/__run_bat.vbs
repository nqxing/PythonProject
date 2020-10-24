function getfolder() 
getfolder=left(wscript.scriptfullname,instrrev(wscript.scriptfullname,"\")-1) 
end function
function runBat()
set ws=WScript.CreateObject("WScript.Shell")
ws.Run getfolder()+"\__run_server.bat",0
end function
Function IsExitAFile(filespec)
        Dim fso
        Set fso=CreateObject("Scripting.FileSystemObject")        
        If fso.fileExists(filespec) Then         
        IsExitAFile=True        
        Else IsExitAFile=False        
        End If
End Function
If IsExitAFile(getfolder()+"\__服务已启动.txt") Then
Msgbox "程序已经运行，请先关闭再启动~~"
Else
runBat()
Dim objFso
Set objFso = CreateObject("Scripting.FileSystemObject")
Set textFile = objFso.CreateTextFile(getfolder()+"\__服务已启动.txt",True)
Set objFso = Nothing
End If