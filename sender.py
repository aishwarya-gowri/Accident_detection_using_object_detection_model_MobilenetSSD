import socket, cv2, pickle, struct
import imutils
import cv2
import time


def start_video_stream():
	client_socket,addr = server_socket.accept()
	
	camera = False
	if camera == True:
		vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	else:
		vid = cv2.VideoCapture('images_video.mp4')
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			start = time.time()
			while(vid.isOpened()):
				img,frame = vid.read()  
				frame  = imutils.resize(frame,width=320)
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				end = time.time()
				if int(end-start) >= 30:
					client_socket.close()
					vid.release()
					cv2.destroyAllWindows()
					break
				key = cv2.waitKey(1) & 0xFF
				if key ==ord('q'):
					client_socket.close()
					vid.release()
					cv2.destroyAllWindows()
					break

	except Exception as e:
		print(f"CACHE SERVER {addr} DISCONNECTED")

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = '192.168.0.6' 
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

while True:
	start_video_stream()
