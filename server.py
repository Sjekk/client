import SocketServer
import json
import os
import ConfigParser
#import socket
class ChatRequestHandler(SocketServer.BaseRequestHandler):
    def loadConfig(self):
	self.config = ConfigParser.ConfigParser()
	self.config.read("config") 
	print self.config.get("Secure", "Server")
    def handle(self): 
	try:
		self.ips
	except AttributeError:
		config = ConfigParser.ConfigParser()
		config.read("config")
		contactIP = config.get("Secure", "Server")
		self.ips = contactIP.rsplit(",")
		print "JA"
        addr = self.client_address[0] 
        print "[%s] Verbindung hergestellt" % addr 
        while True:
            s = self.request.recv(1024)
	    socket = self.request
            if s: 
                print "[%s] %s" % (addr, s) 
		anfrage =  json.loads(s)
		#disc_space.py -w 80 -c 90 --disc /dev/sda1
		dir = os.popen("plugins/disc_space.plugin -w 80 -c 90 --disc /dev/sda1").readlines()
		print str(dir)
		ret = str(dir[0]).replace("\n", "")
		#print ret
		arr = json.loads(ret)
		ret = '{"plugin": "'+anfrage["plugin"]+'" , "status": "'+arr["status"]+'", "msg" : "'+arr["msg"]+'"}'
		#addr.send(ret)
		if(addr in self.ips):
			socket.sendto(ret, self.client_address)
			#socket.sendto("Wrong IP", self.client_address)
		else:
			socket.sendto("Wrong IP", self.client_address)
			#socket.sendto(ret, self.client_address)
		print ret
            else: 
                print "[%s] Verbindung geschlossen" % addr 
                break

server = SocketServer.ThreadingTCPServer(("", 50000), ChatRequestHandler) 
#server.loadConfig()
server.serve_forever()

