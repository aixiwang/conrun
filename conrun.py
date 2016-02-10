#---------------------------------------------------------------------------------------------
# conrun v01 -- a tool to run program through Linux console serial port
# BSD license is applied to this code
# Copyright by Aixi Wang (aixi.wang@hotmail.com)
#
# How to use:
# python conrun.py serial_port_name local_src_file linux_desc_file 
# example:
#     nodeburn.py COM3 test.txt /root/a.txt
#---------------------------------------------------------------------------------------------
import serial
import sys,time

   
#----------------------
# console_cmd
#----------------------
def console_cmd(serial,cmd,tag1,tag2=''):
    try:
        cmd2 = cmd + '\r'
        serial.write(cmd2)
        
        s2 = ''
        i = 0
        while i < 1024:
            c = s.read(1)
            #print c
            s2 += c
            if s2.find(tag1) >= 0 and len(tag1) > 0:
                return 0, s2
            elif s2.find(tag2) >= 0 and len(tag2) > 0:
                return 1, s2
            else:
                continue
            time.sleep(0.1)
            i += 1
            
        return -1, s2
    except:
        
        return -2, 'console_cmd exception'

#----------------------
# console_login
#----------------------                
def console_login(serial,board_type,username=None,password=None):
    if board_type == 'galileo':
        # prepare login
        while True:
            ret, resp = console_cmd(serial,'','login:', '~#')        
            print ret, resp
            
            if ret == 0:
                break
            if ret == 1:
                print 'has entered command'
                return 0
                
            else:
                print 'prepare login again!'
                time.sleep(1)

        # login
        while True:
            ret, resp = console_cmd(serial,'root','~#')        
            print ret, resp
            
            if ret == 0:
                print 'entered command'                
                return 0
            else:
                print 'login retry again!'
                time.sleep(1)
        

    else:
        print 'unsupported board!'
        return -1

    return 0;
    
        
#-------------------------
# main
#-------------------------
if __name__ == '__main__':
    serialport_path = sys.argv[1]
    serialport_baud = 115200
    s = serial.Serial(serialport_path,serialport_baud)

    console_login(s,'galileo','root')
    
    fname = sys.argv[2]
    print 'prepare to read: ' + fname
    i = 0
    fh = open(fname)
    for line in fh.readlines(): 
    
        print line
        if i == 0:
            c = 'echo "%s" > %s' % (line.rstrip('\r\n'),sys.argv[3])
        else:
            c = 'echo "%s" >> %s' % (line.rstrip('\r\n'),sys.argv[3])
        #print 'sent cmd:',c
        ret, resp = console_cmd(s,c,'~#')
        print ret,resp
        i += 1    
 
    c = 'python %s > /tmp/r.txt' % (sys.argv[3])
    ret, resp = console_cmd(s,c,'~#')
    print ret,resp
    
    
    print '---------> dump r.txt'
    c = 'cat /tmp/r.txt'
    ret, resp = console_cmd(s,c,'~#')
    print ret,resp
    
    s.close()
