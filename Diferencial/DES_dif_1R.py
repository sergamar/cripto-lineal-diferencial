from DES_personalizado import DES
from random import randint
import sys

# Función que comprueba si queda una única opción para la clave (False) o no (True)
def comprobar_posibilidades(conjuntos):
    if len(conjuntos) == 0:
        return True
    clave_encontrada = False
    for conjunto in conjuntos:
        if len(conjunto) > 1:
            clave_encontrada = True
            break
    return clave_encontrada

if len(sys.argv) is not 2:
    print("El uso del programa es: python3 DES_dif_1R.py clave")
    print("La clave debe proporcionarse en formato hexadecimal")
    exit()

clave = int(sys.argv[1], 16)

des = DES(clave, 1)

posibles_claves = []
primera = True

while comprobar_posibilidades(posibles_claves):
    plano = randint(0, 0xffffffffffffffff)
    cifrado = des.des(plano)
    l_p = plano >> 32
    r_c = cifrado & 0xffffffff
    l_c = cifrado >> 32
    # Bits de entrada de las S-Boxes antes de calcular el XOR con la clave
    entrada_S = des.expandir(r_c)
    # Bits de la salida de las S-Boxes antes de calcular la permutación P
    salida_S = des.permutar_inv(l_p ^ l_c)
    for i in range(8):
        salida_Si = (salida_S >> (4*(7-i))) & 0b1111
        entrada_Si = (entrada_S >> (6*(7-i))) & 0b111111
        posibles_claves_parciales = set([])
        for j,fila in enumerate(des.S[i]):
            posibles_claves_parciales.add(des.entrada_fc(j, fila.index(salida_Si)) ^ entrada_Si)
        if primera:
            posibles_claves.append(posibles_claves_parciales)
        else:
            posibles_claves[i] = posibles_claves_parciales.intersection(posibles_claves[i])
    primera = False

subclave = 0
for sub in posibles_claves:
    subclave = subclave << 6
    subclave = subclave | sub.pop()
clave_deshecha = des.deshacer_subclave(subclave)
mascara = des.deshacer_subclave(0xffffffffffff)
resultado = ''
for i in range(64):
    if mascara % 2 == 1:
        resultado += str(clave_deshecha % 2)
    else:
        if i % 8 == 0:
            resultado += 'P'
        else:
            resultado += '_'
    mascara = mascara >> 1
    clave_deshecha = clave_deshecha >> 1
print('Clave obtenida: 0b'+ resultado[::-1])
print('Clave real:     '+ bin(clave))