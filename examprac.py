#Libreria I2C
import smbus
import time
#Librerias OLED
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

#Configuracion OLED
oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 32 
BORDER = 5
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

#Configuracion I2C EEPROM
bus = smbus.SMBus(1)
i2c_addr = 0x50 #Direccion de la memoria 24LC256 devuelta por el comando i2cdetect -y 1

#1

primos = [1,2,4,6,10,12,16,18] #Lista de numeros primos ajustados al inicio de las localidades con un valor de 0
multiplos = [2,5,8,11,14,17] #Lista con numeros de las localidades multiples de 3 ajustadas al inicio de las mismas con un valor de 0
resultados = [20,21,22,23] #Lista con numeros de las localidades resultado de 3 ajustadas al inicio de las mismas con un valor de 0
numero_datos = 20 #Numero de datos a ser ingresados por el usuario
datos = [] #Lista en la que se guardan los datos ingresados por el usuario
nuevos = [] #Lista en la que se guardan los datos a reemplazar en las localidades de resultados
print("Escriba los " + str(numero_datos) + " datos a guardar")
for g in range (numero_datos): #Se van adicionando los datos ingresados a la lista de datos.
	entrada = int(input())
	datos.append(entrada)

#Se escriben los elementos de la lista de datos a la memoria 24LC256
data = 0
write_addr = 0x0000 #Se inicia la escritura desde la primera localidad en la memoria
for x in range (numero_datos):
	L_Bye_Data = [write_addr, datos[data]]
	bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data)
	data = data + 1 #Aumenta en uno el valor del indice que recorre la lista de datos
	write_addr += 1 #Aumenta en uno el valor del indice que recorre las localidades de memoria
	time.sleep(0.01) #Se utiliza un delay con el fin de no provocar errores al leer la memoria en las siguientes lineas de codigo.

#A
Mensaje_A = "Datos empleados en A: "
print(Mensaje_A)
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de mensaje predeterminado
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = Mensaje_A #Se asigna el mensaje predeterminado a la variable text para la impresion en la pantalla
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1) #Se utiliza un intervalo de un segundo entre las impresiones con el fin de poder leer el valor en la pantalla
index_par = 0x0001 #Esta es la localidad de memoria 2 pero por el inicio de conteo en 0 se le quita uno y termina en la posicion 1
resultado_par = 0 #Variable que guarda el resultado final de la suma de contenidos de las localidades recorridas
for o in range (10):
	bus.write_i2c_block_data(i2c_addr, 0x0000, [index_par])
	value = bus.read_byte(i2c_addr)
	print(int(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value) #Se convierte en string el valor obtenido de la localidad de la memoria para su impresion en la pantalla
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	time.sleep(1) #Se utiliza un intervalo de un segundo entre las impresiones con el fin de poder leer el valor en la pantalla
	resultado_par = resultado_par + int(value)
	index_par += 2 #Se aumenta en 2 el valor del indice que recorre las localidades de memoria dado a que solo se quieren consultar las localidades pares
datos.append(resultado_par) #Se agrega el resultado del inciso a la lista de datos con el fin de esribirlo a la memoria.
L_Bye_Data = [write_addr, datos[20]] #Esta es la posicion 21 en la lista pero la misma inicia con 0 por eso 20.
bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data) #Se escribe el resultado retomando la ultima posicion a la que apunto el indice con el cual escribimos en la memoria previamente.
write_addr += 1 #Aumenta en uno el indice que vamos utilizando para escribir en la memoria.
time.sleep(0.1) #Delay con el fin de no provocar errores al leer la memoria en las siguientes lineas de codigo.

#B
Mensaje_B = "Datos empleados en B: "
print(Mensaje_B)
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de mensaje predeterminado
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = Mensaje_B #Se asigna el mensaje predeterminado a la variable text para la impresion en la pantalla
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1) #Se utiliza un intervalo de un segundo entre las impresiones con el fin de poder leer el valor en la pantalla
bandera_complemento_b = 0 #La bandera se enciende en caso de que el resultado final resulte ser negativo
index_non = 0x0000 #Variable con la que se recorren las localidades nones del arreglo de datos guardados
bus.write_i2c_block_data(0x50, 0x0000, [index_non])
resultado_non = bus.read_byte(i2c_addr) #Variable que guarda el resultado final de la resta del contenido de las localidades recorridas
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(resultado_non) #Se convierte en string el primer valor obtenido de la localidad de la memoria para su impresion en la pantalla
print(str(resultado_non)) #Se imprime el valor en terminal con el find de una doble comprobacion
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1) #Se utiliza un intervalo de un segundo entre las impresiones con el fin de poder leer el valor en la pantalla
index_non += 2 #Se suma 2 al valor del indice con el fin de saltarnos la localidad par que no queremos restar.
for u in range (9):
	bus.write_i2c_block_data(i2c_addr, 0x0000, [index_non])
	value = bus.read_byte(i2c_addr)
	print(int(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value) #Se convierte en string el primer valor obtenido de la localidad de la memoria para su impresion en la pantalla
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	time.sleep(1) #Se utiliza un intervalo de un segundo entre las impresiones con el fin de poder leer el valor en la pantalla
	resultado_non = resultado_non - int(value)
	index_non += 2
if (resultado_non < 0):
	bandera_complemento_b = 1 #En el caso de que el resultado de la resta sea negativo se enciende la bandera
datos.append(resultado_non) #Se agrega el resultado del inciso a la lista de datos con el fin de esribirlo a la memoria.
L_Bye_Data = [write_addr, datos[21]] #Esta es la posicion 22 en la lista pero la misma inicia con 0 por eso 21.
bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data)
write_addr += 1 #Aumenta en uno el indice que vamos utilizando para escribir en la memoria.
time.sleep(0.1) #Delay con el fin de no provocar errores al leer la memoria en las siguientes lineas de codigo.

#C
Mensaje_C = "Datos empleados en C: "
print(Mensaje_C)
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de mensaje predeterminado
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = Mensaje_C
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1)
bandera_complemento_c = 0
index_primo = 0x0000 #Variable con la que se recorren las localidades primas del arreglo de datos guardados con apoyo en la lista de numeros primos.
bus.write_i2c_block_data(0x50, 0x0000, [primos[index_primo]])
resultado_primo = bus.read_byte(i2c_addr) #Variable que guarda el resultado final de la multiplicacion del contenidos de las localidades recorridas
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(resultado_primo)
print(str(resultado_primo))
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1)
index_primo += 1
for u in range (7):
	bus.write_i2c_block_data(i2c_addr, 0x0000, [primos[index_primo]])
	value = bus.read_byte(i2c_addr)
	print(int(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	time.sleep(1)
	resultado_primo = resultado_primo * int(value)
	index_primo += 1
if (resultado_primo < 0):
	bandera_complemento_c = 1 #Si la multiplicacion diera un resultado negativo se enciende la bandera
datos.append(resultado_primo) #Se agrega el resultado del inciso a la lista de datos con el fin de esribirlo a la memoria.
L_Bye_Data = [write_addr, datos[22]] #Esta es la posicion 23 en la lista pero la misma inicia con 0 por eso 22
bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data)
write_addr += 1
time.sleep(0.1)

#D
Mensaje_D = "Datos empleados en D: "
print(Mensaje_D)
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de mensaje predeterminado
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = Mensaje_D
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1)
index_cuad = 0x0000 #Variable con la que se recorren las localidades primas del arreglo de datos guardados con apoyo en la lista de numeros primos.
bus.write_i2c_block_data(0x50, 0x0000, [multiplos[index_cuad]])
value = bus.read_byte(i2c_addr) #Variable que guarda el resultado final de la suma del contenidos de las localidades recorridas
resultado_cuad = (int(value) * int(value))
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(value)
print(str(value))
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
time.sleep(1)
index_cuad += 1
for u in range (5):
	bus.write_i2c_block_data(i2c_addr, 0x0000, [multiplos[index_cuad]])
	value = bus.read_byte(i2c_addr)
	print(int(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	time.sleep(1)
	prerescuad = (int(value) * int(value))
	resultado_cuad = resultado_cuad + prerescuad
	index_cuad += 1
datos.append(resultado_cuad) #Se agrega el resultado del inciso a la lista de datos con el fin de esribirlo a la memoria.
L_Bye_Data = [write_addr, datos[23]] #Esta es la posicion 24 en la lista pero la misma inicia con 0 por eso 23.
bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data)
write_addr += 1
time.sleep(0.1)

#2. Mostrar los datos usados y resultados en la pantalla OLED.

index_resul = 0x0000 #Indice con el cual se recorre la lista con los numeros de localidades conteniendo resultados
#Resultado de A en OLED
bus.write_i2c_block_data(i2c_addr, 0x0000, [resultados[index_resul]]) #Pasa la localidad 21 como parametro de la lectura con el fin de obtener el valor alojado en esta localidad
value = bus.read_byte(i2c_addr)
resul_final = value #Preparamos el resultado final al guardar el resultado del inciso A en una variable a sumar en el futuro con los nuevos datos ingresados por el usuario
print("Resultado de la suma en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(value)
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
index_resul += 1
time.sleep(1)
#Resultado de B en OLED
if (bandera_complemento_b == 1):
	bus.write_i2c_block_data(0x50, 0x0000, [resultados[index_resul]])
	valornon = bus.read_byte(i2c_addr)
	value = valornon - 256
	print("Resultado de la resta en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	index_resul += 1
	time.sleep(1)
else:
	bus.write_i2c_block_data(0x50, 0x0000, [resultados[index_resul]])
	value = bus.read_byte(i2c_addr)
	print("Resultado de la resta en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	index_resul += 1
	time.sleep(1)
#Resultado de C en OLED
if (bandera_complemento_c == 1):
	bus.write_i2c_block_data(0x50, 0x0000, [resultados[index_resul]])
	valorcuad = bus.read_byte(i2c_addr)
	value = valorcuad + 256
	print("Resultado de los primos en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
	#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	index_resul += 1
	time.sleep(1)
else:
	bus.write_i2c_block_data(0x50, 0x0000, [resultados[index_resul]])
	value = bus.read_byte(i2c_addr)
	print("Resultado de los primos en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
	#Limpieza de pantalla y construccion de cuadros en el marco de la misma
	oled.fill(0)
	oled.show()
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	draw.rectangle(
	(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
	outline=0,
	fill=0,
	)
	font = ImageFont.load_default()
	text = str(value)
	(font_width, font_height) = font.getsize(text)
	draw.text(
	(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
	text,
	font=font,
	fill=255,
	)
	oled.image(image)
	oled.show()
	index_resul += 1
	time.sleep(1)
#Resultado de D en OLED
bus.write_i2c_block_data(i2c_addr, 0x0000, [resultados[index_resul]])
value = bus.read_byte(i2c_addr)
print("Resultado del cuadrado en localidad " + str((int(index_resul)+21)) + " con valor: " + str(value))
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valores en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(value)
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
index_resul += 1
time.sleep(0.1)

#3
print("Escriba los nuevos valores de las localidades 21 a 24")
for g in range (4):
	entrada = int(input())
	nuevos.append(entrada)
	
#Escribir los nuevos datos en el 24LC256
data = 0
write_addr = 0x0000
for v in range (20):
	write_addr += 1
for z in range (4):
	L_Bye_Data = [write_addr, nuevos[data]]
	bus.write_i2c_block_data(i2c_addr, 0x0000, L_Bye_Data)
	print("Escrito en localidad: " + str((int(write_addr)+21)) + " con valor: " + str(nuevos[data]))
	datos[int(write_addr)] = int(nuevos[data])
	data = data + 1
	write_addr += 1
	time.sleep(0.01)

time.sleep(0.1)

#Suma final de la suma de las localidades pares junto con los valores nuevos

fin_addr = 0x0000
for j in range (20): #Aumentamos el valor del indice hasta llevarlo a las localidades en las que se encuentran los nuevos datos
	fin_addr += 1
for l in range(4): #Leemos las localidades en las que se encuentran los nuevos datos y los sumamos al resultado de la suma del inciso a
	bus.write_i2c_block_data(0x50, 0x0000, [fin_addr])
	resul_final = resul_final + bus.read_byte(i2c_addr)
	fin_addr += 1
	time.sleep(0.5)
print("Resultado final de la suma de localidades pares previa y los nuevos valores ingresados: " + str(resul_final))
#Limpieza de pantalla, construccion de cuadros en el marco de la misma e impresion de valor final en la misma
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
outline=0,
fill=0,
)
font = ImageFont.load_default()
text = str(resul_final)
(font_width, font_height) = font.getsize(text)
draw.text(
(oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
text,
font=font,
fill=255,
)
oled.image(image)
oled.show()
index_resul += 1
time.sleep(1)
