# telnet program example
import socket, select, string, sys

#main function
if __name__ == "__main__":
	
    if(len(sys.argv) < 3) :
        print('Usage : python telnet.py hostname port')
        sys.exit()
	
    host = sys.argv[1]
    port = int(sys.argv[2])
	
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
	
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
	
    print('Connected to remote host. Start sending messages')
    print(f'<You> ')

    while True:
        msg = input('Ваше сообщение: ')
        if msg == 'exit':
            break
        s.send(msg.encode('utf-8')) 	# Отправить!
        data = s.recv(1024).decode('utf-8')
        print('Ответ:', data)

    # while 1:
    #     msg = input('Ваше сообщение: ')
    #     socket_list = [msg, s]
		
    #     # Get the list sockets which are readable
    #     read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		
    #     for sock in read_sockets:
    #         #incoming message from remote server
    #         if sock == s:
    #             data = sock.recv(4096)
    #             if not data :
    #                 print ('\nDisconnected from chat server')
    #                 sys.exit()
    #             else :
    #                 #print data
    #                 print(f'<You> {data}')
			
    #         #user entered a message
    #         else :
    #             # msg = sys.stdin.readline()
    #             s.send(msg)
    #             print(f'<You> ')