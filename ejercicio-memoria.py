'''Se pide a los alumnos que elijan un lenguaje de programación de su elección.

1) El objetivo es hacer un programa que simule el funcionamiento de una memoria caché con correspondencia directa.

2) Para ello, inicialmente, el alumno creará una estructura de datos a su elección que simule la memoria caché.

3) Recordamos que la memoria está compuesta por líneas y que cada línea tiene palabras y una etiqueta(no hay que implementar
   los bits de control). A modo de recuerdo incluimos la siguiente imagen.

4) Seguidamente los alumnos inicializarán los valores de todas las palabras de todas las líneas y todas las etiquetas a un valor de su elección.

5) ¡Ojo! Cada alumno decide el tamaño de su dirección, y los bits que se emplean en la misma para cada una de sus partes.

6) El modelo debe estar acorde a estas decisiones y deben de quedar claramente reflejadas en el código.

7) El programa lee un fichero de texto, creado a la elección del alumno, que contiene mínimo 5 direcciones hexadecimales cada una en una línea.

8) Adicionalmente el alumno también crea otro fichero pero esta vez binario que simule serla RAM.

9) El programa debe simularla actuación de la caché, recibiendo una dirección hexadecimal del primer fichero de texto, verificando en la línea correspondiente
   si la etiqueta de la caché coincide con la de la memoria ( caso de hit o acierto de caché) o si no coincide.

10) Si no coincide debe ir al fichero binario, tomar los datos correctos, incluirlos en la línea de caché correspondiente y actualizar la etiqueta.

Para cada memoria el programa mostrará si ha habido acierto o fallo, teniendo que verse en la
ejecución ejemplos de ambos casos. '''

import json
import os

'''
    - Palabra (desplazamiento): 4 bits → bloques de 16 palabras.
    - Índice (línea de caché): 4 bits → 16 líneas en la caché.
    - Etiqueta: 8 bits
'''

rutaArchivo : str = os.path.join(os.getcwd(), "ficheros", "direcciones.txt")

with open("memdirections.json", "r") as file: #Leemos el json precargado y almacenamos su valor en memdirections
    memdirections : dict = json.load(file)


def checkHexDirection(hexDir:str):
    directionFound: bool = False #Flag que utilizaremos para buscar la direccion en caso de que no esté en caché
    hexDirBinary = bin(int(hexDir, 16))[2:].zfill(16) #Convertimos a hexadecimal (16 bits) y rellenamos
    etiqueta_dir = hexDirBinary[:8]  #Cogemos la etiqueta (primeros 8 bits)
    for line in memdirections:
        etiqueta_mem = line['label']  #Recorremos el json y cogemos el valor de label
        if etiqueta_mem[:8] == etiqueta_dir: #Comparamos la etiqueta de la dirección con la etiqueta a buscar
            for l in line['lines']:
                word_key = list(l.keys())[0]  # Obtener la linea ('0000','0001' etc...)
                blocks = l[word_key]  #Rescatamos los bloques y los recorremos
                for block in blocks:
                    if f"{etiqueta_mem}{word_key}{block['block']}" == hexDirBinary: #Comparamos todos los valores concatenados a la direccion en binario
                        print(f"Encontrado con éxito: {etiqueta_mem}{word_key}{block['block']}")
                        directionFound = True


    if directionFound == False: #Si no lo hemos encontrado en caché
        print("No se ha encontrado el elemento, buscándolo...")
        with open("filebin.bin", "rb") as f: #Leemos el fichero binario (al que previamente le habremos insertado la direccion a buscar)

            data = f.read(2)  #Leemos dos bytes
            numero = int.from_bytes(data, "big")  #Rescatamos el numero en cuestion

            for line in memdirections:  #Recorremos cada entrada del JSON
                if line["label"] == "00000000":  #Buscamos la entrada 00000000, (explicación)

                    newNumber = bin(numero)[2:].zfill(16)  # Convertimos a binario el numero del fichero
                    newLabel = newNumber[:8]  # primeros 8 bits (etiqueta)
                    word = newNumber[8:12]  # los 4 bits siguientes (linea)
                    block = newNumber[12:]  # los últimos 4 bits (palabra)

                    last_line = line["lines"][-1]  #Sobrescribir los bloques de la palabra correspondiente en la última posición de lines
                    line["label"] = newLabel #Le damos el valor de newLabel

                    for i, blk in enumerate(last_line["0000"]): #Recorremos la linea
                        last_value = last_line["0000"]   #Guardamos la clave antes de eliminarla para no causar errores
                        del last_line["0000"]
                        last_line[word] = last_value #Sobreescribimos con el valor de word
                        last_line[word][i]["block"] = block #Actualizamos el valor del bloque correspondiente
                        break

        with open("memdirections.json", "w") as f: #Abrimos el json para escritura y le pasamos el json modificado
            json.dump(memdirections, f, indent=4)


#Leemos el archivo de txt para encontrar la dirección que se quiere
with open(rutaArchivo, "r") as file:
    for hexDirection in file:
        checkHexDirection(hexDirection)

#Escribimos en el fichero binario para realización de pruebas de recuperación:
'''with open("filebin.bin","wb") as f:
    f.write((0x081F).to_bytes(2, "big"))'''
#f.write((0x081A).to_bytes(2, "big"))
#f.write((0x081F).to_bytes(2, "big"))