from DES_personalizado import DES
from random import randint
import csv
import sys

ejemplos_entrenamiento = 3500000
ejemplos_prueba = 1500000

def bits_a_lista(cifrado, plano):
    lista = []
    for i in range(64):
        lista.append((cifrado >> (63 - i)) & 0x1)
    for i in range(64):
        lista.append((plano >> (63 - i)) & 0x1)
    return lista

try:
    rondas = int(sys.argv[1])
except ValueError:
    print('El número de rondas tiene que ser un entero en [1,16]')
    exit()
except IndexError:
    print('Es necesario proporcionar el número de rondas como argumento de entrada')
    exit()
if rondas < 1 or rondas > 16:
    print('El número de rondas tiene que ser un entero en [1,16]')
    exit()
rondas_str = str(sys.argv[1])
f_train = 'dataset_' + rondas_str + 'R_train.txt'
f_test = 'dataset_' + rondas_str + 'R_test.txt'

# Generamos una clave aleatoria común
clave = randint(0, 0xffffffffffffffff)
des = DES(clave, rondas)
# Arreglamos la paridad si es necesario
des.calcular_paridad()

with open(f_train, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_entrenamiento):
        plano = randint(0, 0xffffffffffffffff)

        cifrado = des.des(plano)

        writer.writerow(bits_a_lista(cifrado, plano))

with open(f_test, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_prueba):
        plano = randint(0, 0xffffffffffffffff)

        cifrado = des.des(plano)

        writer.writerow(bits_a_lista(cifrado, plano))
