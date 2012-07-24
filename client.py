import socket

ip = raw_input("IP-Adresse: ") 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((ip, 50000))

try: 
    #while True: 
    #nachricht = raw_input("Nachricht: ") 
    nachricht = '{"plugin": "check_disc", "warning": "2", "critical": "90", "param": {"disc:" : "/dev/sda1"}}'
    s.send(nachricht) 
    antwort = s.recv(1024) 
    print "[%s] %s" % (ip,antwort) 
finally: 
    s.close()
