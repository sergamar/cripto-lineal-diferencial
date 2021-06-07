from DES_personalizado import DES
from random import randint
import csv
import sys

ejemplos_entrenamiento = 750000
ejemplos_prueba = 250000
diferencial = 0x4008000004000000

def bits_a_lista(diferencial_salida, clase):
    lista = []
    for i in range(64):
        lista.append((diferencial_salida >> (63 - i)) & 0x1)
    lista.append(clase)
    lista.append(1 - clase)
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

with open(f_train, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_entrenamiento):
        clave = randint(0, 0xffffffffffffffff)
        plano_1 = randint(0, 0xffffffffffffffff)
        plano_2 = plano_1 ^ diferencial
        plano_3 = randint(0, 0xffffffffffffffff)
        while plano_1 ^ plano_3 == diferencial:
            plano_3 = randint(0, 0xffffffffffffffff)

        des = DES(clave, rondas)
        des.calcular_paridad()

        cifrado_1 = des.des(plano_1)
        cifrado_2 = des.des(plano_2)
        cifrado_3 = des.des(plano_3)

        diferencial_1 = cifrado_1 ^ cifrado_2
        diferencial_2 = cifrado_1 ^ cifrado_3

        writer.writerow(bits_a_lista(diferencial_1, 1))
        writer.writerow(bits_a_lista(diferencial_2, 0))

with open(f_test, 'w', newline='') as out:
    writer = csv.writer(out)
    for i in range(ejemplos_prueba):
        clave = randint(0, 0xffffffffffffffff)
        plano_1 = randint(0, 0xffffffffffffffff)
        plano_2 = plano_1 ^ diferencial
        plano_3 = randint(0, 0xffffffffffffffff)
        while plano_1 ^ plano_3 == diferencial:
            plano_3 = randint(0, 0xffffffffffffffff)

        des = DES(clave, rondas)
        des.calcular_paridad()

        cifrado_1 = des.des(plano_1)
        cifrado_2 = des.des(plano_2)
        cifrado_3 = des.des(plano_3)

        diferencial_1 = cifrado_1 ^ cifrado_2
        diferencial_2 = cifrado_1 ^ cifrado_3

        writer.writerow(bits_a_lista(diferencial_1, 1))
        writer.writerow(bits_a_lista(diferencial_2, 0))
