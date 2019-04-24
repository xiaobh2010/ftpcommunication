from socket import *
import os
import sys
from signal import *
import time

FILE_PATH='/home/tarena/'

#子进程已经把sockfd给关闭了
class FtpServer(object):
    def __init__(self,c):
        self.c=c
    def do_list(self):
        filelist=os.listdir(FILE_PATH)
        #服务器端确认请求是否可以执行
        if not filelist or filelist==None:
            self.c.send('FALL'.encode())
        self.c.send('OK'.encode())#避免粘包问题
        time.sleep(0.1)
        for filename in filelist: #由于file是关键字所以打印不出结果
            #判断文件类型文件应该和路径联系在一起,起初只给了文件名称，程序执行的时候一直没有进入条件语句语句中去执行
            if filename[0]!='.' and os.path.isfile(FILE_PATH+filename): 
                self.c.send(filename.encode())
                time.sleep(0.1)
        self.c.send('##'.encode())
        print('文件列表发送完毕')
        return 

    def do_get(self,filename):
        try:
            fd=open(FILE_PATH+filename,'r')
        except:
            self.c.send('FALL'.encode())
        self.c.send('OK'.encode())
        time.sleep(0.1)
        #要是前面open的时候直接以二进制读取，发送的时候字符串就不需要转换成字节形式了
        # for line in fd:  #通过迭代器访问
        #   self.c.send(line.encode())
        #下面这个也可以读取，不知道为啥第一次运行程序的时候为啥木有用
        while True:
            s=fd.readline()
            if s=='':
                break
            self.c.send(s.encode())
        fd.close()
        time.sleep(0.1)
        self.c.send('##'.encode())
        print('文件发送完毕')
        return 

    def do_put(self,filename):
        try:
            fd=open(FILE_PATH+filename,'w')
        except:
            self.c.send('FAIL'.encode())
        self.c.send('OK'.encode())
        time.sleep(0.1)
        #文件传输就算粘包也没有关系，这是可靠的传输
        while True:
            data=self.c.recv(1024).decode()
            if data=='##':
                break
            elif data=='&&':
                fd.close()
                print('上传文件不存在')
                return
            fd.write(data)
        fd.close()
        print('文件接收完毕')
        return

    def do_quit(self):
        self.c.send('OK'.encode())

def main():
    if len(sys.argv)<3:
        print('argv is error')
        sys.exit(1)
        #这第二个参数好像是正常退出是０，其他数字表示异常退出
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    BUFFERSIZE=1024

    sockfd=socket(AF_INET,SOCK_STREAM)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    signal(SIGCHLD,SIG_IGN)

    while True:
        try:
            c,addr=sockfd.accept()
        except KeyboardInterrupt:
            print('异常退出')
            sockfd.close()
            sys.exit(0)  
        except Exception:
            continue
        print('connect from ',addr)  
        pid=os.fork()
        if pid<0:
            print('fork failed')
            continue
        elif pid==0:
            sockfd.close()
            while True:
                #接收客户端请求
                ftp=FtpServer(c)
                data=c.recv(BUFFERSIZE).decode()
                if not data:
                    break
                elif data[:4]=='list':
                    print('recv list')
                    ftp.do_list()
                    print(233333)
                elif data[:3]=='get':
                    print('recv get')
                    filename=data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[:3]=='put':
                    print('recv put')
                    filename=data.split(' ')[-1]
                    ftp.do_put(filename)
                elif data[:4]=='quit':
                    print('recv quit')
                    print('客户端退出')
                    ftp.do_quit()
                c.send(''.encode())
            c.close()
        elif pid>0:
            c.close()
            continue    #不写continue父进程就退出了
        #父进程回去处理下一个连接请求


if __name__=="__main__":
    main()
