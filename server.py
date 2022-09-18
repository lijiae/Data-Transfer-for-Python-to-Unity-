# coding=utf-8
import datetime
import socket
import threading
import json
import time
import argparse
import numpy as np

'''
备注：这里主要使用json传输
格式如下：
MoveData、Person、AreaNum、Action需要与其对应
Person：船员编号
AreaNum：船员目的位置
Action：动作编号，1为站，2为坐
'''

parser = argparse.ArgumentParser(description="To Unity 3D config")
parser.add_argument('--ip', default='127.0.0.1')
parser.add_argument('--port', default=10086,type=int)
parser.add_argument('--unity_opt', default=1,type=int)

args = parser.parse_args()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class ToUnity3D(object):
    def __init__(self):
        self.transdata=[0,1]
        self.ip=args.ip
        self.init=False
        self.port=args.port
        self.opt=args.unity_opt

    def trans_json(self,transdata=[0,1]):
        """
        说明 将数据转换成json格式

        transdata = [0, 1]  测试样例

        :param transdata: 原数据
        :return: json格式数据
        """
        num=0
        translist = []
        for area in transdata:
            if area =="[" or area =="]" or area ==" " or area =="\n" or area == ",":
                continue
            single = {"shipNum":0,"AreaNum": area, "Action": 1}  # 注意这里的Action全是1
            translist.append(single)
        result = {"MoveData": translist}
        print(result)
        return result
    def update(self,loc_num=[2,0,4]):

        self.init=True
        # self.transdata=np.random.randint(low=0, high=9, size=np.random.randint(0,5)).tolist()
        self.transdata=loc_num

    def on_new_connection(self,client_executor, addr):
        file_object = open('demolist.txt', 'r')


        print('Accept new connection from %s:%s...' % addr)
        for line in file_object:
            if self.opt == -1:
                break
            if self.opt == 1:

                time.sleep(0.6)
                self.update(line)
                print(line)
                client_executor.send(
                    bytes(repr(json.dumps(self.trans_json(self.transdata))), encoding="utf-8"))
                #print(bytes(repr(json.dumps(self.trans_json(self.transdata))), encoding="utf-8"))# 发送json信息,socket只传输byte
                    # bytes(repr(json.dumps(self.trans_json(self.transdata))),cls=NpEncoder),)  # 发送json信息,socket只传输byte
                # print(self.transdata)


        client_executor.close()  # 所有信息发送完就会关闭
        file_object.close()
        print('Connection from %s:%s closed.' % addr)

    def toUnity3D_start(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((args.ip,args.port))
        listener.listen(10)  # 最大连接数
        print('Waiting for connect...')
        while True:
            client_executor, addr = listener.accept()
            t = threading.Thread(target=self.on_new_connection, args=(client_executor, addr))
            t.start()
        print('end')

if __name__ == '__main__':
    toUnity3D=ToUnity3D()
    toUnity3D.toUnity3D_start()





#
#
# # 当新的客户端连入时会掉用这个方法
# def on_new_connection(client_executor, addr):
#     print('Accept new connection from %s:%s...' % addr)
#     while True:
#         if opt == -1:
#             break
#         if opt == 1:
#             client_executor.send(
#                 bytes(repr(json.dumps(trans_json(loc_num))), encoding="utf-8"))  # 发送json信息,socket只传输byte
#             time.sleep(0.1)
#
#     client_executor.close()  # 所有信息发送完就会关闭
#     print('Connection from %s:%s closed.' % addr)
#
#
# listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listener.bind((ip, port))
# listener.listen(10)  # 最大连接数
# print('Waiting for connect...')
#
# # 每连接一个线程就会有这个
# while True:
#     client_executor, addr = listener.accept()
#     t = threading.Thread(target=on_new_connection, args=(client_executor, addr))
#     t.start()
#     print('end')
