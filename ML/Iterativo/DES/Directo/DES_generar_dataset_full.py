from DES_personalizado import DES
from random import randint
import csv
import sys

ejemplos_entrenamiento = 700000
ejemplos_prueba = 300000

def bits_a_lista(pasos):
    lista = []
    for paso in pasos:
        for i in range(64):
            lista.append((paso >> (63 - i)) & 0x1)
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
f_train = 'dataset_' + rondas_str + 'R_iter_train.txt'
f_test = 'dataset_' + rondas_str + 'R_iter_test.txt'

# Generamos una clave aleatoria común
clave = randint(0, 0xffffffffffffffff)

des = []

for i in range(rondas):
    nuevo_des = DES(clave, i+1)
    # Arreglamos la paridad si es necesario
    nuevo_des.calcular_paridad()
    des.append(nuevo_des)

with open(f_train, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_entrenamiento):
        cifrados = []
        
        plano = randint(0, 0xffffffffffffffff)

        cifrados.append(plano)

        for instancia in des:
            cifrados.append(instancia.des(plano))

        writer.writerow(bits_a_lista(cifrados))

with open(f_test, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_prueba):
        cifrados = []
        
        plano = randint(0, 0xffffffffffffffff)

        cifrados.append(plano)

        for instancia in des:
            cifrados.append(instancia.des(plano))

        writer.writerow(bits_a_lista(cifrados))
