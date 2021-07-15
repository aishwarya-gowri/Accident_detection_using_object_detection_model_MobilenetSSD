import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.0.6'
port = 12345
print("Waiting for a sender in the network")
while True:
	try:
		client_socket.connect((host_ip,port)) 
		print("connected to a sender")
		break
	except Exception as e:
		print("Waiting to receive video")
		continue

data = b""
payload_size = struct.calcsize("Q")


while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
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
