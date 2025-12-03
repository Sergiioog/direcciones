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
from pprint import pprint
#--------------------------
'''
Bus de direcciones:
Vamos a usar 8 bits → 28=2562^8 = 25628=256 direcciones.
Esto es muy pequeño, pero suficiente para practicar.
Bloques por línea (tamaño del bloque):
Usamos 4 palabras por bloque → desplazamiento = log₂(4) = 2 bits.
Número de líneas en la caché:
Usamos 16 líneas → índice = log₂(16) = 4 bits.

Bits dirección = 8 bits (porque el bus es de 256 direcciones).
Bits desplazamiento = 2 bits (por 4 palabras por bloque).
Bits índice = 4 bits (por 16 líneas en la caché).
Bits etiqueta =
8−(4+2)=2 bits8 - (4 + 2) = 2 \text{ bits}8−(4+2)=2 bits
'''



rutaArchivo : str = os.path.join(os.getcwd(), "ficheros", "direcciones.txt")

with open("memdirections.json", "r") as file:
    memdirections : dict = json.load(file)


def checkHexDirection(hexDir:str):
    directionFound: bool = False
    directionWritten : bool = False
    hexDirBinary = bin(int(hexDir, 16))[2:].zfill(16) #Convertimos a hexadecimal (16 bits)
    etiqueta_dir = hexDirBinary[:5]  # Cogemos la etiqueta (primeros 5 bits)

    for line in memdirections:
        etiqueta_mem = line['label']  # Accedemos al diccionario
        if etiqueta_mem[:5] == etiqueta_dir:
            #Revisar por que:
            for l in line['lines']:
                word_key = list(l.keys())[0]  # obtener la clave de la palabra, ej. '1111'
                blocks = l[word_key]  # lista de bloques
                for block in blocks:
                    if f"{etiqueta_mem}{word_key}{block['block']}" == hexDirBinary:
                        print(f"Encontrado con éxito: {etiqueta_mem}{word_key}{block['block']}")
                        directionFound = True


    if directionFound == False:
        print("No se ha encontrado el elemento, buscándolo...")
        with open("filebin.bin", "rb") as f:

            data = f.read(2)  # lee 2 bytes
            numero = int.from_bytes(data, "big")  # o "little"

            for line in memdirections:  # Recorremos cada entrada del JSON
                if line["label"] == "00000000":  # 1) buscar el label

                    newNumber = bin(numero)[2:].zfill(16)  # '1010101111001101' ejemplo
                    newLabel = newNumber[:8]  # primeros 8 bits
                    word = newNumber[8:12]  # los 4 bits siguientes
                    block = newNumber[12:]  # los últimos 4 bits

                    print(">>>", line["label"], line["lines"][-1], line["lines"][-1]["0000"][0]["block"])
                    print(">>>", newNumber, newLabel, word, block)


                    # sobrescribir los bloques de la palabra correspondiente en la última posición de lines
                    last_line_dict = line["lines"][-1]
                    line["label"] = newLabel

                    # sobrescribir todos los bloques REALIZAR PEQUEÑOS AJUSTES
                    for i, blk in enumerate(last_line_dict["0000"]):
                        last_line_dict["0000"][i]["block"] = block
                        break

        with open("memdirections.json", "w") as f:
            json.dump(memdirections, f, indent=4)


with open(rutaArchivo, "r") as file:
    for hexDirection in file:
        checkHexDirection(hexDirection)

#Escribimos en el fichero binario:
'''with open("filebin.bin","wb") as f:
    f.write((0x081F).to_bytes(2, "big"))'''


#f.write((0x081A).to_bytes(2, "big"))
#f.write((0x081F).to_bytes(2, "big"))