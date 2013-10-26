#!/usr/bin/env python
import socket

host = '192.168.1.1'
port = 23

tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_connection.connect((host, port))
tcp_connection.sendall("Hello World")
tcp_connection.close()

