import SocketServer
import json
import os
import ConfigParser
import time
#import socket
class ChatRequestHandler(SocketServer.BaseRequestHandler):
    def log(self, msg, ip):
	print "["+str(time.strftime("%d.%m.%Y %H:%M:%S")) +"]["+ip+"] "+str(msg)
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
        #print "[%s] Verbindung hergestellt" % addr 
	self.log("Verbindungs hergestellt", addr)
        while True:
            s = self.request.recv(1024)
	    socket = self.request
            if s: 
                #print "[%s] %s" % (addr, s) 
		self.log(s, addr)
		anfrage =  json.loads(s)
		params = "" # Parameter die per anfrage["param"] uebergeben werden
		dir = os.popen("plugins/"+anfrage["plugin"]+".plugin -w "+anfrage["warning"]+" -c "+anfrage["critical"]+" --disc /dev/sda1").readlines()
		#print str(dir)
		#self.log(dir, addr)
		ret = str(dir[0]).replace("\n", "")
		arr = json.loads(ret)
		ret = '{"plugin": "'+anfrage["plugin"]+'" , "status": "'+arr["status"]+'", "msg" : "'+arr["msg"]+'"}'
		if(addr in self.ips):
			socket.sendto(ret, self.client_address)
		else:
			socket.sendto("Wrong IP", self.client_address)
		#print ret
		self.log(ret, addr)
            else: 
                #print "[%s] Verbindung geschlossen" % addr 
		self.log("Verbindung geschlossen", addr)
                break

server = SocketServer.ThreadingTCPServer(("", 50000), ChatRequestHandler) 
#server.loadConfig()
server.serve_forever()

