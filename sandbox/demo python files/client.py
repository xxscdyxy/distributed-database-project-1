#!/usr/bin/env python
# coding: utf-8

# In[1]:



########################here  1
import socket  
import json
import pandas as pd
from threading import Thread
import time

ADDRESS = ('127.0.0.1', 8712)
g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

# 如果开多个客户端，这个client_type设置不同的值，比如客户端1为linxinfa，客户端2为linxinfa2

client_type ='linxinfa'

df = pd.DataFrame({'Table Name': [], 'Network Address': [], 'Port Number': []})
df.to_excel("table_ip.xlsx", index = False)


def get_ip(client,table_name):
    global client_type
    bytes1 = client.recv(1024)
    msg1 = bytes1.decode(encoding='utf8')
    print(msg1)
    
    jd = {}
    jd['Table_Name'] = table_name
    jd['COMMAND'] = 'GET_IP'
    jd['client_type'] = client_type
    
    jsonstr = json.dumps(jd)
    print('send: ' + jsonstr + " to the nameserver"+'\n') 
    client.sendall(jsonstr.encode('utf8'))
    
    bytes2 = client.recv(1024)
    msg2 = bytes2.decode(encoding='utf8')
    jdd = json.loads(msg2)
    network_address = jdd['Network_Address']
    port_number = jdd['Port_Number']
    df = pd.read_excel("table_ip.xlsx") 
    new_Table_information = {'Table Name': table_name, 'Network Address': network_address, 'Port Number':port_number}
    df = df.append(new_Table_information,ignore_index=True)
    df.to_excel("table_ip.xlsx", index = False)
    print('receieved the ip ( ' + network_address+ ' ) and port number ( ' + str(port_number) +' ) from nameserver')
    
    
def input_table_name():
    return input("please input the name of the table you are looking for : ")

if '__main__' == __name__:
    table_name = input_table_name()
    client = socket.socket() 
    client.connect(ADDRESS)
    get_ip(client,table_name)
    client.close()


# In[ ]:


########################here 2
import socket  
import json
import pandas as pd
from threading import Thread
import time

# 如果开多个客户端，这个client_type设置不同的值，比如客户端1为linxinfa，客户端2为linxinfa2

client_type ='linxinfa'

df = pd.read_excel("table_ip.xlsx")

network_address = df["Network Address"].values.item()
print("aa")
port_number = df["Port Number"].values.item()
print("bb")
ADDRESS_infoserver = (network_address, port_number)
print("cc")
print(ADDRESS_infoserver)


########################################################
g_socket_server = None  # 负责监听的socket
 
g_conn_pool = {}  # 连接池

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    g_socket_server.connect(ADDRESS_infoserver)
    print("ff")

def accept_client():
    """
    接收新连接
    """
    while True:
        people_name = input_people_name()
        print("aa")
        thread = Thread(target=get_info, args=(g_socket_server, people_name))
        print("bb")
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
#########################################################

    
def get_info(client,people_name):
    global client_type
    
    jd = {}
    jd['People_Name'] = people_name
#     jd['COMMAND'] = 'GET_IP'
    jd['client_type'] = client_type
    jsonstr = json.dumps(jd)
    print('send: ' + jsonstr + "to the infoserver"+'\n')
    
    
    client.sendall(jsonstr.encode('utf8'))
    print("aaa")
    bytes = client.recv(1024)
    print("bbb")
    msg = bytes.decode(encoding='utf8')
    print("ccc")
    jdd = json.loads(msg)
    print("ddd")
    info = jdd['Info']
    print('receieved the information from infoserver: '+'\n')
    return info

def input_people_name():
    return input("please input the name of the people you are looking for : ")

if '__main__' == __name__:
    init()
    
    thread = Thread(target=accept_client)
    print("e")
    thread.setDaemon(True)
    print("f")
    thread.start()
    # 主线程逻辑
    while True:
        time.sleep(0.1)


# In[ ]:




