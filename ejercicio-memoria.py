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
import numpy as np
from pprint import pprint
import os



directionsBus: int = 2**8  # 256 direcciones.
num_blocks: int = 4         # Bloques de 4 palabras
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



cachedMemory: list[dict] = []
rutaArchivo : str = os.path.join(os.getcwd(), "ficheros", "direcciones.txt")
#Contadores dinamicos
lineCount : int = 0
wordCount : int = 0

for _ in range(directionsBus):
    line = {
        'label':  bin(lineCount)[2:].zfill(5),  # valor inicial para etiqueta
        'lines': [
            {f'word{wordCount}': [{'block': '0'} for _ in range(num_blocks)]}
            for wordCount in range(0,4)
        ]
    }
    cachedMemory.append(line)
    lineCount += 1

#9) El programa debe simular la actuación de la caché, recibiendo una dirección hexadecimal del primer fichero de texto, verificando en la línea correspondiente
#   si la etiqueta de la caché coincide con la de la memoria ( caso de hit o acierto de caché) o si no coincide.

def checkHexDirection(hexDir:str):
    hexDirBinary = bin(int(hexDir, 16))[2:].zfill(16) #Convertimos a hexadecimal (16 bits)
    etiqueta_dir = hexDirBinary[:5]  # Cogemos la etiqueta (primeros 5 bits)

    for line in cachedMemory:
        etiqueta_mem = line['label']  # Accedemos al diccionario
        if(etiqueta_mem == etiqueta_dir):
            print(">>> Coinciden")
        print("Datos:", {
            "EtiquetaMemoria": etiqueta_mem,
            "EtiquetaDireccion": etiqueta_dir,
            "Coincide": etiqueta_mem == etiqueta_dir
        })


#Leemos del fichero con las direcciones cargadas
with open(rutaArchivo, "r") as file:
    for hexDirection in file:
        checkHexDirection(hexDirection)

#Escribimos en el fichero binario:
with open("filebin.bin","wb") as f:
    f.write(b'\x00\x01\x02\x03\x04')  # 5 bytes: 00 01 02 03 04


# Comprobamos
pprint(cachedMemory)





'''print(f"Memoria caché: ", cachedMemory)'''
