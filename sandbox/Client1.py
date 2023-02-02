#!/usr/bin/env python
# coding: utf-8

# In[8]:


### project 1 ###
import socket

s = socket.socket()
HOST = socket.gethostname()


# def get_table_name(table_name):
#     print(table_name)    

def get_ip_port(table_name):
    PORT = 8080 # The port used by the server (arbitrarily defining this)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(table_name.encode())
        Network_Address = s.recv(1024)
        Port_Number = s.recv(1024)
        print(f"the IP address is: {Network_Address.decode()}")
        print(f"the Port Number is: {Port_Number.decode()}")
        
        
table_name = "Email"
get_ip_port(table_name)


# In[ ]:




