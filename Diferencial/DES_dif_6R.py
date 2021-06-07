from DES_personalizado import DES
import sys
import numpy as np
from random import randint

if len(sys.argv) < 2:
    print("El uso del programa es: python3 DES_dif_6R.py clave")
    print("La clave debe proporcionarse en formato hexadecimal")
    exit()

# Conteo de las ocurrencias de cada posible subclave
def contar_subclaves_parciales_candidatas(posibilidades, contador, top, max):
    for i in posibilidades[0]:
        for j in posibilidades[1]:
            for k in posibilidades[2]:
                for l in posibilidades[3]:
                    for m in posibilidades[4]:
                        subclave_parcial = i << 24 | j << 18 | k << 12 | l << 6 | m
                        contador[subclave_parcial] += 1
                        if contador[subclave_parcial] == max:
                            top.append(subclave_parcial)
                        elif contador[subclave_parcial] >= max:
                            top = [subclave_parcial]
                            max = contador[subclave_parcial]
    return top, max

# Criptoanálisis de las 5 S-Boxes de la sexta ronda del DES
def diferencial_5SBoxes(diferencia, n_parejas, sboxes):
    contador = np.zeros(2**30)
    top = []
    max = 0

    for _ in range(n_parejas):
        plano1 = randint(0, 0xffffffffffffffff)
        plano2 = plano1 ^ diferencia
        cifrado1 = des.des(plano1)
        cifrado2 = des.des(plano2)
        S_E1 = des.expandir(cifrado1 & 0xffffffff)
        S_E2 = des.expandir(cifrado2 & 0xffffffff)
        l_dif = (cifrado1^cifrado2) >> 32
        # Solo usaremos las S-Boxes de 2 a 8
        S_O_dif = des.permutar_inv(l_dif^(diferencia & 0xffffffff))
        posibilidades = []
        for i in sboxes:
            posibilidades_SBox = []
            for clave_parcial in range(64):
                entrada_1 = ((S_E1 >> (48-6*(i))) & 0b111111) ^ clave_parcial
                fila_1 = ((entrada_1 >> 4) & 0b10) ^ (entrada_1 & 0b1)
                columna_1 = (entrada_1 >> 1) & 0b1111
                entrada_2 = ((S_E2 >> (48-6*(i))) & 0b111111) ^ clave_parcial
                fila_2 = ((entrada_2 >> 4) & 0b10) ^ (entrada_2 & 0b1)
                columna_2 = (entrada_2 >> 1) & 0b1111
                if des.S[i-1][fila_1][columna_1] ^ des.S[i-1][fila_2][columna_2] == ((S_O_dif >> (32-4*(i))) & 0b1111):
                    posibilidades_SBox.append(clave_parcial)
            posibilidades.append(posibilidades_SBox)

        top, max = contar_subclaves_parciales_candidatas(posibilidades, contador, top, max)
    return top

# Comprobación de la coherencia entre las predicciones obtenidas por cada diferencial
def comprobar_coherencia(p1, p2):
    ext_p1 = ((p1 & 0x3f000000) << 12) | (p1 & 0xffffff)
    ext_p2 = (((p2 & 0x3ffc0000) << 6) | (p2 & 0x3ffff)) << 12
    if (ext_p1 & 0x3f000fff000) == (ext_p2 & 0x3f000fff000):
        return ((ext_p1 & 0x03f000ffffff) | (ext_p2 & 0xfff03ffff000))
    else:
        return None

# Búsqueda por fuerza bruta de los bits restantes de la clave
def fuerza_bruta(union, des):
    mascara = des.deshacer_subclave(0xfff03fffffff)
    clave_deshecha = des.deshacer_subclave(union)

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

    plano1 = randint(0, 0xffffffffffffffff)
    cifrado1 = des.des(plano1)

    for i in range(2**14):
        placeholder = 'A'
        clave_test = clave_deshecha
        for j in range(14):
            clave_test = clave_test | ((i >> j) & 1) << resultado.index(placeholder)
            placeholder = chr(ord(placeholder) + 1)
        des_test = DES(clave_test, 6)
        if des_test.des(plano1) == cifrado1:
            des_test.calcular_paridad()
            return des_test.clave
    return None

clave = int(sys.argv[1], 16)

des = DES(clave, 6)
des.comprobar_paridad()

n_parejas = 120

# Primera diferencia para obtener los bits de la clave correspondientes a las S-Boxes 2, 5, 6, 7 y 8
diferencia1 = 0x4008000004000000
SBoxes1 = [2,5,6,7,8]

top1 = diferencial_5SBoxes(diferencia1, n_parejas, SBoxes1)

# top1 contiene las claves parciales más probables de las S-Boxes 2, 5, 6, 7 y 8

# Segunda diferencia para obtener los bits de la clave correspondientes a las S-Boxes 1, 2, 4, 5 y 6
diferencia2 = 0x0020000800000400
SBoxes2 = [1,2,4,5,6]

top2 = diferencial_5SBoxes(diferencia2, n_parejas, SBoxes2)

for p1 in top1:
    for p2 in top2:
        union = comprobar_coherencia(p1, p2)
        if union:
            clave = fuerza_bruta(union, des)
            if clave:
                print('La clave es:', hex(clave))
                exit(0)

# Al ser probabilístico, cabe la pequeña posibilidad de que las probabilidades
# no nos indiquen la subclave correcta con suficientes ocurrencias.
# En ese caso, solicitamos al usuario que vuelva a ejecutar el programa
print('No se ha podido obtener la clave, por favor vuelve a ejecutar el programa')