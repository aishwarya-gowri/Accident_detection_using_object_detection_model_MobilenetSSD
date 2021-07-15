import socket, cv2, pickle, struct
import imutils # pip install imutils
import threading
import cv2

global frame
global packet

frame = None
packet = None


def start_video_stream():
	global frame
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '192.168.0.6'
	port = 9999

	while True:			
		try:
			client_socket.connect((host_ip,port))
			break
		except Exception as e:
			print(f"Connection not established. waiting.")
			continue

	data = b""
	payload_size = struct.calcsize("Q")
	while True:
		while len(data) < payload_size:
			packet = client_socket.recv(4*1024)
			if not packet: 
				cv2.destroyAllWindows()
				break
			data+=packet
		
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		if not packet :
			print(packet)
			break
		msg_size = struct.unpack("Q",packed_msg_size)[0]
		
		while len(data) < msg_size:
			data += client_socket.recv(4*1024)
		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)
		cv2.imshow("RECEIVING VIDEO FROM SENDER",frame)
		key = cv2.waitKey(1) & 0xFF
		if key  == ord('q'):
			break
	client_socket.close()
	


def serve_client(addr,client_socket,packet):
	global frame
	
	try:
		print(packet)
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			while True:
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
						
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		pass

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 12345

server_socket.bind((host_ip,port))
server_socket.listen()
print("Listening at",(host_ip,port))

thread = threading.Thread(target=start_video_stream, args=())
thread.start()


while True:
	client_socket,addr = server_socket.accept()
	print(addr)
	thread = threading.Thread(target=serve_client, args=(addr,client_socket,packet))
	thread.start()
	print("TOTAL CLIENTS ",threading.activeCount() - 2)
