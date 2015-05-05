# Esteganografia

* Practica de seguridad
* Lenguaje de programación java

El programa cifra un mensaje seleccionado en el audio text.wav. Podría realizar esto con cualquier audio .wav.
Con una pequeña modificación se podría pedir el audio en el que se desea esconder el mensaje por teclado.

Tenemos un vector que guarda canales y los frames correspondientes a cada canal. Si se trata de un audio estereo (2 canales) 
se van alternando los canales, es decir el orden de modificación sería el siguiente:
Canal1 Frame1,Canal2 Frame1, Canal1 Frame2, Canale 2 Frame2, Canal1 Frame3 ...

Si el audio es mono (1 canal) se modificarán por orden los frames de ese canal: Canal1 Frame1, Canal1 Frame2 ....

Para ocultar el mensaje en las canciones, se procede de la siguiente manera:

1. Se obtendrá el mensaje a ocultar (un String)
2. Dicho mensaje se convertirá a binario (Siguiendo el formato ASCII para la conversión) y se coje los bits 
uno por uno (de izq a der) 
3. Se recorrerá cada frame de la canción
4. Se cambiará el último bit de cada frame por el bit correspondiente del mensaje a ocultar, hasta que el 
mensaje esté oculto. El resto de los frames de la canción se mantendrán iguales.

Para recuperar el mensaje oculto se procede de la siguiente manera:

1. Se obtendrá de cada frame de la canción el último bit
2. Se concatenarán todos estos bits obtenidos
3. Se construirá el mensaje oculto (un String en formato ASCII)


