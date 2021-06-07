from DES_personalizado import DES
import sys
from random import randint

# Función que comprueba si queda una única posibilidad para la clave (False) o
# aún hay varias opciones (True)
def comprobar_posibilidades(posibilidades):
    for posibilidad in posibilidades:
        if len(posibilidad) > 1:
            return True
    return False

if len(sys.argv) < 2:
    print("El uso del programa es: python3 DES_dif_4R.py clave")
    print("La clave debe proporcionarse en formato hexadecimal")
    exit()

clave = int(sys.argv[1], 16)
# Almacenaremos los posibles valores de las claves para las S-Boxes de 2 a 8
posibilidades = [list(range(64))]*7

diferencia_entrada = 0x2000000000000000

des = DES(clave, 4)
des.comprobar_paridad()

iters = 0

while comprobar_posibilidades(posibilidades):
    iters += 1
    plano1 = randint(0, 0xffffffffffffffff)
    plano2 = plano1 ^ diferencia_entrada
    cifrado1 = des.des(plano1)
    cifrado2 = des.des(plano2)
    S_E1 = des.expandir(cifrado1 & 0xffffffff)
    S_E2 = des.expandir(cifrado2 & 0xffffffff)
    l_dif = (cifrado1^cifrado2) >> 32
    # Solo usaremos las S-Boxes de 2 a 8
    S_O_dif = des.permutar_inv(l_dif)
    for i in range(1, 8):
        nuevas_posibilidades = []
        for clave_parcial in posibilidades[i-1]:
            entrada_1 = ((S_E1 >> (48-6*(i+1))) & 0b111111) ^ clave_parcial
            fila_1 = ((entrada_1 >> 4) & 0b10) ^ (entrada_1 & 0b1)
            columna_1 = (entrada_1 >> 1) & 0b1111
            entrada_2 = ((S_E2 >> (48-6*(i+1))) & 0b111111) ^ clave_parcial
            fila_2 = ((entrada_2 >> 4) & 0b10) ^ (entrada_2 & 0b1)
            columna_2 = (entrada_2 >> 1) & 0b1111
            if des.S[i][fila_1][columna_1] ^ des.S[i][fila_2][columna_2] == ((S_O_dif >> (32-4*(i+1))) & 0b1111):
                nuevas_posibilidades.append(clave_parcial)
        posibilidades[i-1] = nuevas_posibilidades

subclave = 0
for parte in posibilidades:
    subclave = subclave << 6
    subclave = subclave | parte[0]

mascara = des.deshacer_subclave(0x3ffffffffff)
clave_deshecha = des.deshacer_subclave(subclave)

clave_obtenida = clave_deshecha
resultado = ''
placeholder = 'A'
for i in range(64):
    if mascara % 2 == 1:
        resultado += str(clave_obtenida % 2)
    else:
        if i % 8 == 0:
            resultado += '_'
        else:
            resultado += placeholder
            placeholder = chr(ord(placeholder) + 1)
    mascara = mascara >> 1
    clave_obtenida = clave_obtenida >> 1

resultado = resultado[::-1]

print('Iteraciones utilizadas: ', iters)
print('Clave obtenida: 0b'+ resultado)
print('Clave real:     '+ bin(clave))
print('Los _ son bits de paridad, las letras son 14 bits desconocidos')

print('Obteniendo los 14 bits restantes por fuerza bruta')

resultado = resultado[::-1]

for i in range(2**14):
    placeholder = 'A'
    clave_test = clave_deshecha
    for j in range(14):
        clave_test = clave_test | ((i >> j) & 1) << resultado.index(placeholder)
        placeholder = chr(ord(placeholder) + 1)
    des_test = DES(clave_test, 4)
    if des_test.des(plano1) == cifrado1:
        des_test.calcular_paridad()
        print('La clave de cifrado es', hex(des_test.clave))
        break

# TODO: Paridad