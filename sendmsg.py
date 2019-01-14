#!/usr/bin/env python
# @Author:ZhengZhong,Jiang
# @TIME:2018/12/4 16:34

import sys
import time
import socket



class SendMsg:
    def __init__(self, mobile, msg):
        self.mobile = mobile
        self.msg = msg

    def trans(self):
        Msgtype = '6101'
        Bank = '0305'
        Systrace = '000000'
        TransTm = time.strftime("%m%d%H%M%S", time.localtime(int(time.time())))
        Mobile = self.mobile
        BusNum ='000000'
        SourceFlag = 'ZABBIX'
        message = "%s%s%s%s%s%s%s%s" % (Msgtype,
                                       Bank,
                                       Systrace,
                                       TransTm,
                                       Mobile,
                                       BusNum,
                                       SourceFlag,
                                       self.msg,
                                       )
        
        MsgLen = len(message.encode('gb2312'))

        if len(str(MsgLen)) < 4:
            MsgLen = str(MsgLen).zfill(4)

        data = "%s%s" % (MsgLen, message)
        with open('/tmp/sendmsg.log', 'a+') as f:
            f.write(data + '\n')
        return data.encode('gb2312')

    def send(self):
        address = ('198.203.209.203', 9901)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        self.trans()
        client.send(self.trans())
        r_data = client.recv(1024)
        with open('/tmp/sendmsg.log', 'a+') as f:
            f.write(str(r_data) + '\n')
        client.close()


if __name__ == '__main__':
    mobile = sys.argv[1]
    msg = sys.argv[2]
    obj = SendMsg(mobile, msg)
    obj.send()
