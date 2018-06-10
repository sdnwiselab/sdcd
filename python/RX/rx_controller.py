import multiprocessing 
import socket
import sys
import wifi_rx
import Zigbee_RX
from Naked.toolshed.shell import muterun_js

def wifi():
	wifi_rx.main()
        

def zigbee():
	Zigbee_RX.main()

def node_script():
       response = muterun_js('sdcd/Frontend/socket_udp.js') #PATH TO NODE JS SCRIPT 
       if response.exitcode == 0:
          print(response.stdout)
       else:
           sys.stderr.write(response.stderr)	 
 
class Rx_Controller():

   p = multiprocessing.Process(target=wifi)
   p1 = multiprocessing.Process(target=zigbee)    
   p2 = multiprocessing.Process(target=node_script)  
    
   def rx_handler(self,type_data):
          
          if self.p2.is_alive()==False :
             self.p2.start()

	  if "wifi" in type_data:
              if self.p1.is_alive():
		 self.p1.terminate()
              if self.p.is_alive()==False :
                 self.p = multiprocessing.Process(target=wifi)
		 self.p.start()   
	  else:
	      if self.p.is_alive():
		 self.p.terminate()
	      if self.p1.is_alive()==False :
                 self.p1 = multiprocessing.Process(target=zigbee) 
		 self.p1.start()
          
   

   def socket_tcp_server(self):
      try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print '*****************RX_CONTROLLER**************'
        print 'SOCKET TCP SERVER-->CREATE CONNECTION'
	client_address=('0.0.0.0',8003) 
	#Bind socket to local host and port
	try:
	    s.bind(client_address)
	except socket.error as msg:
	    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    sys.exit()
	     
	print 'SOCKET TCP SERVER-->BIND COMPLETE'
	 
	#Start listening on socket
	s.listen(10)
	print 'SOCKET TCP SERVER-->LISTENING'
	 
	#now keep talking with the client
	while 1:
	    #wait to accept a connection - blocking call
	    conn, addr = s.accept()
	    data=conn.recv(1024) 
            self.rx_handler(data)
      except KeyboardInterrupt:
        print '*****Interrupted by user*****'
        s.close()
        sys.exit(1)


if __name__ == "__main__":
     rx_controller=Rx_Controller()
     rx_controller.socket_tcp_server()    



