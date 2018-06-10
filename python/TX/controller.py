import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys
import json
import time
from collections import namedtuple
import multiprocessing
import TX802_11
import TX802_15_4




def wifi():
      TX802_11.main()
    

def zigbee():
      TX802_15_4.main()
       

class Controller(tornado.websocket.WebSocketHandler):
    p = multiprocessing.Process(target=wifi)
    p1 = multiprocessing.Process(target=zigbee)
    ip_address1='XXX.XXX.XXX.XXX' #IP ADDRESS OF MACHINE WITH GNURADIO TX FILES
    ip_address2='XXX.XXX.XXX.XXX' #IP ADDRESS OF MACHINE WITH RX CONTROLLER
    
   
    def open(self):
        #ON WEB SOCKET OPENING
        print 'WEB SOCKET SERVER--->SOCKET ON'
    
    def activate_rx(self,value):
            print 'CONTROLLER----->TRY TO ACTIVATE RX'
            self.socket_tcp_client(value,8003,self.ip_address2)
       
    def parser_message(self,message):
    
        x = json.loads(message, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        if "wifi" in x.type:
            
            if self.p1.is_alive():
               self.p1.terminate()

	    if self.p.is_alive()==False :
               self.p = multiprocessing.Process(target=wifi)
               self.activate_rx(x.type)
               #time.sleep(4)
               self.p.start()
            time.sleep(2)
            self.socket_tcp_client(x.message,8001,self.ip_address1)
            print 'SEND MESSAGE USING IEEE 802.11(WIFI)'
            
        else:

            if self.p.is_alive():
               self.p.terminate()

	    if self.p1.is_alive()==False :
               self.p1 = multiprocessing.Process(target=zigbee)
               self.activate_rx(x.type)
               #time.sleep(4)
               self.p1.start()
            time.sleep(2)
            self.socket_tcp_client(x.message,8002,self.ip_address1)
            print 'SEND MESSAGE USING IEEE 802.15.4(ZIGBEE)'       
     




    def socket_tcp_client(self,message,port,ip_address):
        #SOCKET TCP CLIENT
        print '***************TRANSPORT LAYER*****************'
        server_address = (ip_address, port)
        try:
             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             print('SOCKET TCP CLIENT----> CONNECTION TO {} PORT {}'.format(*server_address))
             sock.connect(server_address)
             print 'SOCKET TCP ONLINE......'
             #Send data
             print('SOCKET TCP SENDING---> {!r}'.format(message))
             sock.sendall(message)

        except socket.error, msg:
             print "SOCKET TCP ERROR: COULD'NT CONNECT TO SOCKET SERVER---->ABORT"
             sock.close()
             sys.exit(1)


        
        

    def on_message(self, message):
        
        print 'WEB SOCKET SERVER--->MESSAGE FROM CLIENT: %s' % message
        #SEND MESSAGE TO TCP SOCKET
        self.write_message("WEB SOCKET SERVER ACK-->YOUR MESSAGE:"+message)
        self.parser_message(message)
    
  
    def on_close(self):
        # CLOSE WEBSOCKET
        print 'WEB SOCKET SERVER--->CONNECTION CLOSE'
  
    def check_origin(self, origin):
        return True
  
application = tornado.web.Application([
    (r'/websocketserver', Controller),
])
  


if __name__ == "__main__":
   
    try:
        #WEBSOCKET SERVER START
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8000)
        print '***************APPLICATION LAYER***************'
        print 'WEB SOCKET SERVER LISTENING ON PORT 8000'
        tornado.ioloop.IOLoop.instance().start()     
    except KeyboardInterrupt:
        print '*****Interrupted by user*****'
    finally:    
        # CLOSE WEBSOCKET ON KEYBOARD INTERRUPT
        http_server.close_all_connections
        sys.exit(1)
        
