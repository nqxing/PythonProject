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
If IsExitAFile(getfolder()+"\__����������.txt") Then
Msgbox "�����Ѿ����У����ȹر�������~~"
Else
runBat()
Dim objFso
Set objFso = CreateObject("Scripting.FileSystemObject")
Set textFile = objFso.CreateTextFile(getfolder()+"\__����������.txt",True)
Set objFso = Nothing
End If