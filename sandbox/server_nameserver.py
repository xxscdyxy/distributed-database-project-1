#!/usr/bin/env python
# coding: utf-8

# In[ ]:


###demo###
import socket
s = socket.socket()
HOST = socket.gethostname() 
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(addr[1])
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(f"receieved hahaha from client: {data}")
            if not data:
                break
            conn.sendall(data)


# In[22]:


###demo###
import socket
s = socket.socket()
HOST = socket.gethostname() 
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(addr[1])
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(f"receieved hahaha from client: {data}")
            if not data:
                break
            conn.sendall(str(addr[0]).encode())
            conn.sendall(str(addr[1]).encode())


# In[1]:


###project 1###
import tabulate
import pandas as pd
import socket
s = socket.socket()
host = socket.gethostname() 
df = pd.DataFrame({'Table Name': [], 'Network Address': [], 'Port Number': []})


# In[2]:


###get data base includeing the email, ID, phone number, 
def get_information_from_servers(table_info):
    df = table_info
    port = 11111
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"Hello")
        Table_Name = s.recv(1024)
        Network_Address = s.recv(1024)
        Port_Number = s.recv(1024)
        new_Table_information = {'Table Name': Table_Name.decode(), 'Network Address': Network_Address.decode(), 'Port Number': Port_Number.decode()}
        df = df.append(new_Table_information,ignore_index=True)
        print(f"the table name is: {df}")
        df.to_excel("table_info.xlsx", index = False)  


# In[80]:


def send_IP_to_client(df):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 11111
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            port = addr[1]
            while True:
                table_name = conn.recv(1024)
                table_name = table_name.decode()
                
                Network_Address = df.loc[df["Table Name"]==table_name,"Network Address"].values.item()
                Port_Number = df.loc[df["Table Name"]==table_name,"Port Number"].values.item()
                print(f"client request the IP address of: {table_name}")
                if not table_name:
                    break
                conn.sendall(Network_Address.encode())
                conn.sendall(str(Port_Number).encode())
                print(f"the ip address is: {Network_Address}")
                print(f"the port number is: {Port_Number}")


# In[3]:


get_information_from_servers(df)
df = pd.read_excel("table_info.xlsx")


# In[65]:


get_information_from_servers(df)
df = pd.read_excel("table_info.xlsx")


# In[67]:


get_information_from_servers(df)
df = pd.read_excel("table_info.xlsx")


# In[81]:


send_IP_to_client(df)


# In[32]:


df = pd.DataFrame({'Table Name': ['Email', 'ID','Phone Number'], 
#                  'Network Address': ['192.168.50.66', '192.168.50.66', '192.168.50.66']}, 
                 'Network Address': ['192.168.50.11', '192.168.50.22', '192.168.50.33']})
table_nameserver = tabulate({'Table Name': ['Email', 'ID','Phone Number'], 
#                  'Network Address': ['192.168.50.66', '192.168.50.66', '192.168.50.66']}, 
                 'Network Address': ['192.168.50.11', '192.168.50.22', '192.168.50.33']}, 
                 headers='keys', 
                 tablefmt='fancy_grid', 
                 missingval='N/A')
print(table_nameserver)
print(df[df["Table Name"]=="Email"].values[0][1])
# print(df.loc[df["Table Name"]=="Email"]["Network Address"])
a = df.loc[df["Table Name"]=="Email","Network Address"].values.item()
print(a)


# In[ ]:





# In[3]:


import pandas as pd
df = pd.DataFrame({'Table Name': [], 'Network Address': [], 'Port Number': []})
print(df)
new_Table_information = {'Table Name': "haha", 'Network Address': "12.123.123.12", 'Port Number': 2}
df = df.append(new_Table_information,ignore_index=True)
print(df)


# In[ ]:




