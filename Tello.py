import cv2
import threading
import time
from djitellopy import Tello
import paho.mqtt.client as mqtt
from pid import PIDController

#region: MQTT references
broker = ''
port = 1883
topic = "IDAtual"
ProximoID = 1
#endregion

def initialize():
	drone = Tello()
	drone.connect()
	drone.streamon()
	#cv2.namedWindow("Tello") # Stream window
	return drone # Initialize drone

#region: global variables
stack_angle = []

group_a = {2,3,4,5}
group_b = {6,7,8,9}
group_c = {10,11,12,13}
group_d = {14,15,16,17}
group_e = {18,19,20,21}
group_p = {22,23,24}

id_to_group = {}

for identified in group_a:
	id_to_group[identified] = 'group_a'
for identified in group_b:
	id_to_group[identified] = 'group_b'
for identified in group_c:
	id_to_group[identified] = 'group_c'
for identified in group_d:
	id_to_group[identified] = 'group_d'
for identified in group_e:
	id_to_group[identified] = 'group_e'
for identified in group_p:
	id_to_group[identified] = 'group_p'
#endregion

def get_rotation_roll_back():
	return sum(stack_angle) # Angle necessary to return to the initial direction

def rotate_right(angle):
	tello.rotate_counter_clockwise(-1*angle)
	stack_angle.append(-1*angle)
	time.sleep(2) # Rotate, save angle and wait the drone to perform

def rotate_left(angle):
	tello.rotate_counter_clockwise(angle)
	stack_angle.append(angle)
	time.sleep(1) # Rotate, save angle and wait the drone to perform

def initialize_aruco():
	arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
	arucoParams = cv2.aruco.DetectorParameters()
	return arucoDict, arucoParams # Initialize ArUco variables

def process_image(frame, arucoDict, arucoParams):

	corners, ids, _ = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	corners, ids, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams) # Detect ArUco IDs

	if ids is not None: # If identified any ID
		if corners is not None: # And identified their corners

			for (marker_corner, marker_id) in zip(corners, ids):
				corners = marker_corner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = corners

				topRight = (int(topRight[0]), int(topRight[1])) # Turn the corners into frame coordinates
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				marker_size = 10250  # Size of marker_area one meter away
				marker_area = cv2.contourArea(marker_corner) # Size of marker in the frame
				distance = (marker_size / marker_area) ** 0.5
				# Calculo da distancia baseado na area real e visivel
				# (passível de erros, portanto o drone não realiza movimentos
				# continuos em YAW para evitar perder sua noção de distância)

				height, width, _ = frame.shape
				aruco_x = int((topLeft[0] + bottomRight[0]) / 2.0) # Coordenada x do Aruco
				frame_x = width // 2 # Coordenada x do Frame

				return ids, distance, aruco_x, frame_x

def align(D, center_x, aruco_x):
	kp_d = 10
	ki_d = 0.1
	kd_d = 0.01

	kp_x = 1
	ki_x = 0.1
	kd_x = 0.01

	pid_x = PIDController(kp_x, ki_x, kd_x)
	error_x = center_x - aruco_x
	rc_x = pid_x.update(error_x)

	desired_distance = 2.0

	pid_distance = PIDController(kp_d, ki_d, kd_d)
	error_distance = desired_distance - D
	rc_distance = pid_distance.update(error_distance)

	rc_x = max(min(rc_x, 20), -20)
	rc_distance = max(min(rc_distance, 20), -20)
	rc_x = -1 * rc_x
	return rc_x, rc_distance
	# O PID itera a velocidade em y do drone até a distância entre as coordenadas x do aruco e do frame seja nula
	# E a velocidade em x até que ele esteja a 2 metros do ID

def begin(id): # Rotina de start
	tello.takeoff()
	x=0 # Coordenadas dadas no dia da prova
	y=0
	z=0
	v=60
	tello.go_xyz_speed(x,y,z,v) # Move o drone até o inicio
	time.sleep(5)
	tello.send_rc_control(0,0,0,0) #estabiliza
	tello.rotate_clockwise(90) # Vira o drone para a arena (?)
	if id == 1: # Se detectado o ID 1
		IDAtual = send(1) # Deveria enviar (sem função de envio)
		ProximoID = receive() # Recebe o próximo
	if ProximoID != 1:
		tello.move_up(150) # Move a 2.5 metros do chão
		tello.send_rc_control(0,0,0,0) #estabiliza

def go_around(tello):

	tello=Tello()
	tello.go_xyz_speed(200, 310, 0, 50) # Se move para a proximma face do totem (Assumindo 2 metros do mesmo)
	time.sleep(4) # Espera o drone executar
	rotate_left(90) # Vira para o totem
	time.sleep(4) # Espera o drone executar
	tello.send_rc_control(0,0,0,0) # Estabiliza

def send(id):

	return

def receive():

	IDAtual = 12
	ProximoID = 4

def frame_thread(): # Função de atualização global do frame
	global frame
	while True:
		try:
			frame = tello.get_frame_read().frame
		except Exception:
			print ('\nExit . . .\n')
			break

if __name__ == "__main__":

	tello = initialize() # Inicializa o drone

	frame = None
	frameThread = threading.Thread(target=frame_thread)
	frameThread.daemon = True
	frameThread.start()

	arucoDict, arucoParams = initialize_aruco() # Inicializa os parâmetros dos IDs

	time.sleep(8) # 8 sec

	#tello.takeoff()
	#tello.send_rc_control(0,0,0,0)
	print('Start:')

	while True:

		result = process_image(frame, arucoDict, arucoParams) # Recolhe as variáveis de distancia e coordenadas do ID

		if result is not None and all(item is not None for item in result):

			ID, distance, aruco_x, frame_x = result # Separa as variáveis
			identified = ID
			print(result)
			searched = 5 # Id vuscado
			searched_group = id_to_group.get(searched) # grupo buscado = grupo do id buscado

			if searched not in group_p: # Ainda não deve pousar

				if identified in id_to_group and id_to_group.get(identified) == searched_group: # Se o id identificado está no grupo buscado
					
					(rc_x, rc_d) = align(distance, frame_x, aruco_x) # Alinha com o id identificado

					if distance>2:
						#tello.send_rc_control(int(rc_x), int(rc_d), 0, 0) # Executa as velocidades iteradas até alinhar
						print(f"Distance: {distance}, RC_d: {rc_d}, RC_x: {rc_x}")

					if distance<2:
						#tello.send_rc_control(0, 0, 0, 0) # Para o drone
						while searched != identified:
							result = process_image(frame, arucoDict, arucoParams)

							if result is not None:
								identified = int(result[0]) 
								#go_around(tello) # Gira em torno do totem
								print('Around')
							else:
								#tello.send_rc_control(0,0,0,0)
								print('No markers detected.')
				else:
					while(ID not in searched_group):
						result = process_image(frame, arucoDict, arucoParams) # Volta a processar os IDs dentro do while
						ID, distance, aruco_x, frame_x = result
						tello.rotate_clockwise(1)

			else: # Se deve pousar
				if identified in group_p: # Se encontrou o ID 
					(rc_x, rc_d) = align(distance, frame_x, aruco_x) # Alinha com o ID do carrinho
					tello.land() # Falta chegar mais perto

		else:
			#tello.send_rc_control(0,0,0,0)
			print('No markers detected.')