#!/usr/bin/env python
# coding: utf-8

# In[1]:


########################here  1

import socket  
import json
import pandas as pd
ADDRESS = ('127.0.0.1', 8711)
# 如果开多个客户端，这个client_type设置不同的值，比如客户端1为linxinfa，客户端2为linxinfa2
client_type ='linxinfa'
# g_socket_server = None  # 负责监听的socket
g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
df = pd.read_excel("Email.xlsx", header = None, names = ["name","info"])
df_1 = pd.DataFrame({'Dynamic Port': [],"IP":[]})
df_1.to_excel("Dynamic Port.xlsx", index = False)


def send_data_nameserver(client):
    global client_type
    df_1 = pd.read_excel("Dynamic Port.xlsx") 
    jd = {}
    jd['Name'] = 'Email'
    jd['COMMAND'] = 'SEND_DATA'
    jd['client_type'] = client_type
    
    jsonstr = json.dumps(jd)
    print('send: ' + jsonstr)
    client.sendall(jsonstr.encode('utf8'))
    bytes = client.recv(1024)
    
    msg = bytes.decode(encoding='utf8')
    jdd = json.loads(msg)
    print("here")
    dynamic_port = jdd['Dynamic_Port']
    IP = jdd['IP']
    new_Table_information = {'Dynamic Port': dynamic_port,"IP":IP}
    df_1 = df_1.append(new_Table_information,ignore_index=True)
    df_1.to_excel("Dynamic Port.xlsx", index = False)

    
def input_client_type():
    name = "Email"
    return name
    
if '__main__' == __name__:
    client_type = input_client_type()
    client = socket.socket() 
    client.connect(ADDRESS)
    print(client.recv(1024).decode(encoding='utf8'))
    send_data_nameserver(client)
    client.close()


# In[1]:


########################here 2

import socket  
import json
import pandas as pd
from threading import Thread
import time
# 如果开多个客户端，这个client_type设置不同的值，比如客户端1为linxinfa，客户端2为linxinfa2
client_type ='linxinfa'
df = pd.read_excel("Email.xlsx", header = None, names = ["name","info"])
df_1 = pd.read_excel("Dynamic Port.xlsx") 
dynamic_port = df_1["Dynamic Port"].values.item()
IP = df_1["IP"].values.item()
print(IP)
print(dynamic_port)
ADDRESS = (IP, dynamic_port)


g_socket_server = None  # 负责监听的socket
 
g_conn_pool = {}  # 连接池

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    g_socket_server.bind(ADDRESS)
    print(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("server start，wait for client connecting...")
    
def accept_client():
    """
    接收新连接
    """
    while True:
        client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
        print("aa")
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=send_data_infoserver, args=(client))
        print("bb")
        # 设置成守护线程
        thread.setDaemon(True)
        print("cc")
        thread.start()
        print("dd")
        
        
def send_data_infoserver(client):
    print("haha")
    global client_type
 
    bytes = client.recv(1024)
    print("a")
    msg = bytes.decode(encoding='utf8')
    print("b")
    jd = json.loads(msg)
    print("c")
    name = jd['People_Name']
    print('receieved request'+'\n')
    jdd = {}
    jdd['info'] = df.loc[df["name"]== name,"info"].values.item()
    jsonstr = json.dumps(jdd)
    client.sendall(jsonstr.encode('utf8'))
    print('send: ' + jsonstr + "to the client"+'\n'+'\n')
    
def input_client_type():
    name = "Email"
    return name
    
if '__main__' == __name__:
    
    init()
    # 新开一个线程，用于接收新连接
    print("aaa")
    thread = Thread(target=accept_client)
    print("bbb")
    thread.setDaemon(True)
    print("ccc")
    thread.start()
    print("ddd")
    # 主线程逻辑
    while True:
        time.sleep(0.01)
    

