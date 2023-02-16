#!/usr/bin/env python
# coding: utf-8

# In[ ]:


########################here

import socket  # 导入 socket 模块
from threading import Thread
import time
import json
import pandas as pd

df = pd.DataFrame({'Table Name': [], 'Network Address': [], 'Port Number': []})
df.to_excel("table_info.xlsx", index = False)

ADDRESS = ('127.0.0.1', 8712)  # 绑定地址
 
g_socket_server = None  # 负责监听的socket
 
g_conn_pool = {}  # 连接池

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("server start，wait for client connecting...")

def accept_client():
    """
    接收新连接
    """
    while True:
        client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client, info))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
 
 
def message_handle(client, info):
    """
    消息处理
    """
    client.sendall("connect server successfully!".encode(encoding='utf8'))
    while True:
        try:
            bytes = client.recv(1024)
            msg = bytes.decode(encoding='utf8')
            jd = json.loads(msg)
            cmd = jd['COMMAND']
            df = pd.read_excel("table_info.xlsx") 
            if 'GET_IP' == cmd:
                table_name = jd['Table_Name']
                print("connected with client, he/she request the ip and port numbber of "+ table_name + " table"+'\n')
                print(df)
                network_address = df.loc[df["Table Name"]==table_name,"Network Address"].values.item()
                port_number = df.loc[df["Table Name"]==table_name,"Port Number"].values.item()
                print("a" )
                jdd = {}
                jdd['Network_Address'] = network_address
                print("b")
                jdd['Port_Number'] = port_number
                jsonstr = json.dumps(jdd)
                client.sendall(jsonstr.encode('utf8'))
                print('send: ' + jsonstr + " to the client" +'\n'+'\n' )
                
            elif 'SEND_DATA' == cmd:
                name = jd['Name']
                print("connected with server, it send the information of the "+ name + " table"+'\n')
                client_type = jd['client_type'] 
                g_conn_pool[client_type] = client
                print('The table  information of the servers updated'+'\n')
                jdd = {}
                jdd['Dynamic_Port'] = info[1]
                jdd['IP'] = info[0]
                print(jdd)
                jsonstr = json.dumps(jdd)
                client.sendall(jsonstr.encode('utf8'))
                
                new_Table_information = {'Table Name': name, 'Network Address': info[0], 'Port Number':info[1]}
#                 print(name)
#                 print(info[0])
#                 print(info[1])
#                 print(new_Table_information)
                dff = df.append(new_Table_information,ignore_index=True)
                dff.to_excel("table_info.xlsx", index = False) 
                print(dff)
                
                    
#         except Exception as e:
#             print("error")
# #             remove_client(client_type)
#             break

# def remove_client(client_type):
#     client = g_conn_pool[client_type]
#     if None != client:
#         client.close()
#         g_conn_pool.pop(client_type)
#         print("client offline: " + client_type)

if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        time.sleep(0.01)

