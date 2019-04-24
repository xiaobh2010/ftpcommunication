# ftpcommunication
ftp服务器的实现步骤 
  ftp文件服务器程序 
    1.获取文件列表 
    2.下载文件 
    3.上传文件  
步骤： 
    设计（使用什么技术，实现什么功能，达到什么目的） 
    计划实施（）     
    文档确认（概要设计，详细设计，使用说明，需求分析）     
    编写（） 
测试（） 
-------------------------------------------------------------------- 
tcp连接，并发 并发---》多进程并发fork 

实现步骤： 
  1 创建网络连接  
  1+ 客户端功能架构的设计和客户端退出的处理 （客户端退出相应的子进程退出就可以了） 
  2 实现list file功能 
      @客户端请求 
      @服务器端确认请求 
      @遍历文件夹下文件，把文件名发给客户端（滤除文件夹和隐藏文件就可以了）   
  .开头的隐藏文件，过滤的时候只需要判断第一个字符是不是.就可以了 判断是否是普通文件，是普通文件返回True，不是普通文件返回False 
  补充： os.listpath(path)    #获取指定目录下所有文件的列表 os.path.isfile(filename)    #判断一个文件是否是普通文件 @客户端接收并打印  
  3 实现get file功能     
      @客户端请求     
      @服务器端确认请求     
      @服务器端以读的形式打开文件，客户端以写的形式打开文件    
      @服务器读read---send,客户端recv---write       
  4 实现put file功能     
      @客户端请求     
      @服务器端确认请求    
      @服务器端以写的形式打开文件，客户端以读的形式打开文件    
      @服务器读recv---write,客户端read---send     
