#coding=gbk
#��һ��ע�Ͳ���ʡ��ָ������������֧������
#�������ļ���32λ��python 3.4.3�����ͨ��
import urllib
import time
import string
import ctypes
from ctypes import * 

dll = ctypes.windll.LoadLibrary(r'D:\PythonProject\PersonalDemo\code_identify\wanmei\WmCode.dll')
#���dll���ڵ�ǰĿ¼����ô��Ҫָ��ȫ·��


if(dll.UseUnicodeString(1,1)): #�������������DLL˵��������ı�ʹ��unicode��ʽ
        print('SetInUnicode Success:')#UseUnicodeString����һ�μ��ɣ������ظ�����
else:
        print('etInUnicode Fail!')#ע��������ʽ


if(dll.LoadWmFromFile(r'D:\PythonProject\PersonalDemo\code_identify\wanmei\������̳.dat','163')):#ʹ�þ���·��
        print('Loaddat Success:')#LoadWmFromFile����һ�μ��ɣ������ظ�����
        Str = create_string_buffer(20)#�����ı�������
        if(dll.GetImageFromFile(r'D:\PythonProject\PersonalDemo\code_identify\wanmei\captcha.JPG',Str)):#ʹ�þ���·��
                #�����֤��ͼ���ڵ�ǰĿ¼����ô��Ҫָ��ȫ·��
                print('GetVcode Success:',Str.raw.decode("gbk"))
                #���ص��ı����д���ڿڿ�����
        else:
                print('GetVcode Fail!')
                
	
else:
        print('Loaddat Fail!')#ע��������ʽ
	
	
	
	
		
		
		
	
		
