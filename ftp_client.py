#coding:utf8
from socket import *
import sys
import os
import time

class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd=sockfd
    def do_list(self):
        #发送请求类型
        self.sockfd.send('list'.encode())
        #接受服务器确认
        data=self.sockfd.recv(1024).decode()
        if data=='OK':
            while True:
                data=self.sockfd.recv(1024).decode()
                if data=='##':
                    break
                print(data) 
            print('文件列表打印完毕')
            return 
        else:
            print('文件列表请求失败')
            return
         
    def do_get(self,filename):
        self.sockfd.send(('get '+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=='OK':
            fd=open(filename,'w')
            while True:
                data=self.sockfd.recv(1024).decode()
                if data=='##':
                    break
                fd.write(data)
            fd.close()
            print('文件%s下载成功'%filename)
            return
        else:
            print('下载文件失败')
            return

    def do_put(self,filename):
        self.sockfd.send(('put '+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=='OK':
            try:
                fd=open(filename,'rb')
                #fd=open(filename,'r')
            except:
                print('上传文件不存在')
                self.sockfd.send('&&'.encode())
                return
            for line in fd:
                self.sockfd.send(line)
                #self.sockfd.send(line.encode())
            fd.close()
            time.sleep(0.1)
            self.sockfd.send('##'.encode())
            print('文件%s上传成功'%filename)
            return
        else:
            print('文件上传失败')
            return

    def do_quit(self):
        self.sockfd.send('quit'.encode())
        data=self.sockfd.recv(1024).decode()
        if data=='OK':
            print('客户端断开连接')

def main():
    if len(sys.argv)<3:
        print('argv is error')
        sys.exit(1)
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    BUFFERSIZE=1024

    sockfd=socket(AF_INET,SOCK_STREAM)
    sockfd.connect(ADDR)
    ftp=FtpClient(sockfd)   #生产事件对象
    while True:
        print('**********命令选项**********')
        print('**********list*************')
        print('**********get file*************')
        print('**********put file*************')
        print('**********quit*************')
        data=input('输入命令：')
        if data[:4]=='list':
            ftp.do_list()

        elif data[:3]=='get':
            filename=data.split(' ')[-1]
            ftp.do_get(filename)
            
        elif data[:3]=='put':
            filename=data.split(' ')[-1]
            ftp.do_put(filename)
            
        elif data[:4]=='quit':
            ftp.do_quit()
            sockfd.close()
            sys.exit(0)
        else:
            print('请输入正确命令')
            # continue

if __name__=='__main__':
    main()
