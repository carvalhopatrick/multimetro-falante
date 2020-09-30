# coding=utf-8

import time
try:
	import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")


def decodeDigit(a, b, e, f, g):
	if not a and b and not e and not f and not g:
		return(1)
	elif a and b and e and not f and g:
		return(2)
	elif a and b and not e and not f and g:
		return(3)
	elif not a and b and not e and f and g:
		return(4)
	elif a and not b and not e and f and g:
		return(5)
	elif a and not b and e and f and g:
		return(6)
	elif a and b and not e and not f and not g:
		return(7)
	elif a and b and e and f and g:
		return(8)
	elif a and b and not e and f and g:
		return(9)
	elif a and b and e and f and not g:
		return(0)
	elif not a and not b and not e and not f and not g:
		return(-1)
	else:
		return('x')

GPIO.setmode(GPIO.BCM)	# otherwise: (GPIO.BOARD)
GPIO.setwarnings(False)

# GPIO.setup(17, GPIO.IN)		# otherwise: (xx, GPIO.OUT), (xx, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LCD_BP = [21]
LCD_NEG = [20]
LCD_4BC = [26]
LCD_1A = [12]
LCD_1B = [6]
LCD_1E = [5]
LCD_1F = [1]
LCD_1G = [0]
LCD_2A = [23]
LCD_2B = [22]
LCD_2E = [27]
LCD_2F = [18]
LCD_2G = [17]
LCD_3A = [8]
LCD_3B = [11]
LCD_3E = [25]
LCD_3F = [9]
LCD_3G = [10]

LCD = [ LCD_NEG, LCD_4BC, \
		LCD_1A, LCD_1B, LCD_1E, LCD_1F, LCD_1G, \
		LCD_2A, LCD_2B, LCD_2E, LCD_2F, LCD_2G, \
		LCD_3A, LCD_3B, LCD_3E, LCD_3F, LCD_3G]

# Seta todos pinos do LCD como input
# Tambem cria segunda posicao para armazenar estados logicos dos segmentos
GPIO.setup(LCD_BP[0], GPIO.IN)
LCD_BP.append(False)
for i in range(len(LCD)):
	GPIO.setup(LCD[i][0], GPIO.IN)
	LCD[i].append(False)

# Lista LCD --> LCD[i][0] = pino /// LCD[i][1] = estado

# Espera por uma mudanca de polaridade em LCD_BP,
# que deve acontecer a cada 20ms (50Hz)
LCD_BP[1] = GPIO.wait_for_edge(LCD_BP[0], GPIO.BOTH, timeout=250)
if LCD_BP[1] is None:
	print("Timeout esperando por LCD_BP")
	exit("Timeout")
else:
	LCD_BP[1] = GPIO.input(LCD_BP[0])
	time.sleep(0.003)	# espera 3ms para estabilizar todos segmentos
	for i in range(len(LCD)):
		if GPIO.input(LCD[i][0]) != LCD_BP[1]:
			LCD[i][1] = True	# segmento ligado (fase diferente de LCD_BP)
		else:
			LCD[i][1] = False	# segmento desligado (mesma fase de LCD_BP)



# Decodifica números a partir dos segmentos
digito_1 = decodeDigit(LCD_1A[1], LCD_1B[1], LCD_1E[1], LCD_1F[1], LCD_1G[1])
if digito_1 == 'x':
	print("Erro digito 1 = x")
digito_2 = decodeDigit(LCD_2A[1], LCD_2B[1], LCD_2E[1], LCD_2F[1], LCD_2G[1])
if digito_2 == 'x':
	print("Erro digito 2 = x")
digito_3 = decodeDigit(LCD_3A[1], LCD_3B[1], LCD_3E[1], LCD_3F[1], LCD_3G[1])
if digito_3 == 'x':
	print("Erro digito 3 = x")

if LCD_4BC[1] == True:
	digito_4 = 1
else:
	digito_4 = -1

# Decodifica string a ser enunciada
# Caso 1: Display desligado
if digito_4 == -1 and digito_1 == -1 and digito_2 == -1 and digito_3 == -1:
	string = "Display desativado"
# Caso 2: Fora de escala / circuito aberto
elif digito_4 == 1 and digito_1 == -1 and digito_2 == -1 and digito_3 == -1:
	string = "Fora de escala"
# Caso 3: Medida usando os 4 digitos
elif digito_4 == 1 and digito_1 != -1:
	string = "{}{}{}{}".format(digito_4, digito_3, digito_2, digito_1)
# Caso 4: Medida usando apenas 3 digitos
elif digito_4 == -1 and digito_1 != -1:
	string = "{}{}{}".format(digito_3, digito_2, digito_1)
else:
	string = " Erro na decodificacao da string"

# Adiciona sinal negativo caso segmento estiver ativo
if LCD_NEG == True:
	string = "-{}".format(string)



print("LCD_BP = {}".format(LCD_BP[1]))
print("LCD_NEG = {}".format(LCD_NEG[1]))
print("LCD_4BC = {}".format(LCD_4BC[1]))
print("LCD_1A = {}".format(LCD_1A[1]))
print("LCD_1B = {}".format(LCD_1B[1]))
print("LCD_1E = {}".format(LCD_1E[1]))
print("LCD_1F = {}".format(LCD_1F[1]))
print("LCD_1G = {}".format(LCD_1G[1]))
print("LCD_2A = {}".format(LCD_2A[1]))
print("LCD_2B = {}".format(LCD_2B[1]))
print("LCD_2E = {}".format(LCD_2E[1]))
print("LCD_2F = {}".format(LCD_2F[1]))
print("LCD_2G = {}".format(LCD_2G[1]))
print("LCD_3A = {}".format(LCD_3A[1]))
print("LCD_3B = {}".format(LCD_3B[1]))
print("LCD_3E = {}".format(LCD_3E[1]))
print("LCD_3F = {}".format(LCD_3F[1]))
print("LCD_3G = {}".format(LCD_3G[1]))

print()
print("dig4: {}\ndig3: {}\ndig2: {}\ndig1: {}".format(digito_4, digito_3, digito_2, digito_1))
print()
print(string)

# volta a configuracao de GPIO original (para nao afetar o RPi fora deste programa)
GPIO.cleanup()

	
