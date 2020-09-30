# sudo apt install python3-espeak

from espeak import espeak
from ina219 import INA219, DeviceRangeError
from time import sleep

SHUNT_OHMS = 0.1 								# Resistencia do resistor de shunt do circuito INA219
MAX_EXPECTED_AMPS = 0.3							# Corrente máxima esperada para medição
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

espeak.set_voice("brazil")		# Configura espeak para sintetizar em pt-br

# Variaveis strings de parametros medidos pelo INA219
sTensao_int = ""
sTensao_dec = ""
sTensao_sinal = ""

sCorrente_int = ""
sCorrente_dec = ""
sCorrente_sinal = ""

# Sintetiza string "texto", adicionando uma pausa "delay_ms" no final
def falar(texto, delay_ms):
	espeak.synth(texto)
	while espeak.is_playing():
		pass
	sleep(delay_ms/1000)

# Lê parâmetros medidos pelo INA219, imprime no terminal e salva em string nas variaveis
def read_ina219():
	try:
		# Aceita as variaveis globais nessa funcao
		global sTensao_int, sTensao_dec, sTensao_sinal
		global sCorrente_int, sCorrente_dec, sCorrente_sinal
		
		# Faz leituras
		tensao = ina.voltage()
		corrente = ina.current()
	
		# Cria strings com os valores lidos pelo INA219		
		# Tensao #
		sTensao_int = abs(int(tensao))
		if tensao < 0.0:
			sTensao_sinal = "-"
		else:
			sTensao_sinal = ""
		sTensao_int = str(sTensao_int)
		
		if (abs(tensao) % 1) >= 0.1:
			sTensao_dec = str(int((abs(tensao) % 1)*100))
		else:
			sTensao_dec = "0{}".format(str(int((abs(tensao) % 1)*100)))
			
		# Corrente #
		sCorrente_int = abs(int(corrente))
		if corrente < 0.0:
			sCorrente_sinal = '-'
		else:
			sCorrente_sinal = ""
		sCorrente_int = str(sCorrente_int)
		
		if (abs(corrente) % 1) >= 0.1:
			sCorrente_dec = str(int((abs(corrente) % 1)*100))
		else:
			sCorrente_dec = "0{}".format(str(int((abs(corrente) % 1)*100)))
			
			
		#sCorrente_dec = str(int((abs(corrente) % 1)*100))
		
		# Imprime leituras no terminal
		print("Bus Voltage: {0:0.4f}V".format(tensao))
		print("Bus Current: {0:0.4f}mA".format(corrente))
		#print('Power: {0:0.2f}mW'.format(ina.power()))
		#print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
		
		print("Tensao:   {}{},{} V".format(sTensao_sinal, sTensao_int, sTensao_dec))
		print("Corrente: {}{},{} mA".format(sCorrente_sinal, sCorrente_int, sCorrente_dec))
		print("")

	except DeviceRangeError as e:
		# Current out of device range with specified shunt resister
		print("Erro, medição fora do alcance")
		falar("Erro, medição fora do alcance",300)

while 1:
	read_ina219()
	
	falar("Tensao",200)
	if sTensao_sinal == "-":
		falar("menos",50)
	falar(sTensao_int, 0)
	falar("vírgula",0)
	falar(sTensao_dec,50)
	falar("volts",300)
	
	falar("Corrente",200)
	if sCorrente_sinal == "-":
		falar("menos",50)
	falar(sCorrente_int, 0)
	falar("vírgula",0)
	falar(sCorrente_dec,50)
	falar("milli amperes",300)
	sleep(1)