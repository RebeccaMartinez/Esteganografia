#encoding=utf8
import wave, struct, binascii

def canales(audio):
	num_channels = audio.getnchannels()#devuelve el numero de canarles: 1 para mono, 2 para estereo
	sample_rate = audio.getframerate()#devuelve la frecuencia de muestreo
	sample_width = audio.getsampwidth()#devuelve la anchura de la muestra en bytes
	num_frames = audio.getnframes()#devuelve el numero de frames
	raw_data = audio.readframes( num_frames ) # lee y devuelve n marcos de audio, como cadena de bytes
	audio.close()

	total_samples = num_frames * num_channels #muestras totales
	if sample_width == 1:
		fmt = "%iB" % total_samples # read unsigned chars
	elif sample_width == 2:
		fmt = "%ih" % total_samples # read signed 2 byte shorts
	else:
		raise ValueError("Only supports 8 and 16 bit audio formats.")

	integer_data = struct.unpack(fmt, raw_data)
	del raw_data # Keep memory tidy (who knows how big it might be)
	channels = [ [] for time in range(num_channels) ]

	for index, value in enumerate(integer_data):
		bucket = index % num_channels
		channels[bucket].append(value)
	# “Channels” tiene los canales y sus frames
	return channels

def crearAudio(audio, canales):
	audio.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
	# Numero de canales de la canción de entrada
	nchannels = len(canales)
	# Numero de frames de un canal de la cancion de entrada
	tfchannel = len(canales[0])
	for i in range (0, tfchannel):
		for j in range (0, nchannels):
			data = struct.pack('<h', canales[j][i]) #la '<h' indica que se enpaquetan los datos como short integer 
			audio.writeframes(data)
	audio.close()

#pasa cadena de texto a binario devuelve 0b o 1b al  principio dependiendo si es positivo negativo
def aBinario(char):
	return bin(reduce(lambda x, y: 256* x + y, (ord(c) for c in texto), 0))

#pasa una cadena en binario a cadena de texto
def aLetras(char):
	return  ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(cadena)] * 8))


texto = raw_input("introduzca el mensaje a cifrar: ")
texto = aBinario(texto)
texto = texto.replace("b", "") #eliminamos la b
print (texto)
tam = len(texto) #guardamos el numero de frames modificados

stream = wave.open('test.wav',"rb")
channels = canales(stream)

i = 0
j = 0
if len(channels) == 2:
#de esta forma es más eficiente que usando dos bucles for para recorrer ambos canales, como en los otros casos
	for s in range(0, tam - 1):
		if s % 2 == 0: #si es par, entonces insertamos en el frame correspondiente del canal 0
			aux = bin(channels[0][i]) #pasamos a binario el frame
			aux = aux.replace("b", "") #eliminamos la b
			aux = aux[:-1] #eliminamos el ultimo bit ([:-1] = nos quedamos con todo menos el último elemento)
			aux = aux + texto[s] #añadimos el bit de la posición s del mensaje al final
			channels[0][i] = int(aux,2) #pasamos el numero a decimal
			i = i + 1
		else: #si es impar se modifica el frame correspondiente del canal 2
			aux = bin(channels[1][j])
			aux = aux.replace("b", "")
			aux = aux[:-1]
			aux = aux + texto[s]
			channels[1][j] = int(aux,2)
			j = j + 1
else:
	for s in range(0, tam - 1):
		aux = bin(channels[0][s])
		aux = aux.replace("b", "")
		aux = aux[:-1]
		aux = aux + texto[s]
		channels[0][s] = int(aux,2)

output_file = wave.open('output.wav', 'w')
crearAudio(output_file, channels)

stream = wave.open('output.wav',"rb")
channels = canales(stream)
cadena = ""
for i in range (0, tam / 2):
	for j in range (0, len(channels)):
		frame = channels[j][i] #cogemos los frames correspondientes
		frame = bin(frame)
		frame = frame.replace("b", "")
		bit = frame[-1:] #cojo el ultimo caracter equivale al último bit
		cadena = cadena + bit

cadena = aLetras(cadena)
print cadena