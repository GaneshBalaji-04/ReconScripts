import socket
from time import sleep
host = input("Enter the host:")
smtp_ports = []
for port in range(1,65535):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(3)
			s.connect((host,port))
			banner = s.recv(1024).decode().strip()
			if banner.startswith('220'):
				print(f"[+] Possible SMTP port open at {port}...")
				smtp_ports.append(port)
			else:
				print(f"[+] No SMTP port open at {port}...")
				
			
	except Exception as e:
		print(f"Test failed at {port}...")
		print(f"Exception:{e}")

if len(smtp_ports)!=0:
	print("List of SMTP ports open:",smtp_ports)
else:
	print("No SMTP ports open in the target...")