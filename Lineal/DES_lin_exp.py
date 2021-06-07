from DES_personalizado import DES
import numpy as np
from random import randint
import time
import sys
import matplotlib.pyplot as plt

sesgos = [1.56*(2**(-3)), -1.95*(2**(-5)), 1.22*(2**(-6)), -1.95*(2**(-9)),
          1.95*(2**(-10)), -1.22*(2**(-11)), -1.91*(2**(-14)), -1.53*(2**(-15)),
          1.91*(2**(-16)), -1.19*(2**(-17)), 1.49*(2**(-19)), -1.19*(2**(-21)),
          1.19*(2**(-22)), -1.49*(2**(-24))]

expresiones = [
    #3R
    [
        # PL
        [3, 8, 14, 25],
        # PR
        [17],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #4R
    [
        # PL
        [3, 8, 14, 25],
        # PR
        [17],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #5R
    [
        # PL
        [17],
        # PR
        [3, 8, 14, 25, 1, 2, 4, 5],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #6R
    [
        # PL
        [],
        # PR
        [8, 14, 25],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #7R
    [
        # PL
        [8, 14, 25],
        # PR
        [16, 20],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #8R
    [
        # PL
        [8, 14, 25],
        # PR
        [16, 20],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #9R
    [
        # PL
        [17],
        # PR
        [1, 2, 4, 5, 8, 14, 25],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #10R
    [
        # PL
        [],
        # PR
        [3, 8, 14, 25],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #11R
    [
        # PL
        [3, 8, 14, 25],
        # PR
        [17],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #12R
    [
        # PL
        [3, 8, 14, 25],
        # PR
        [17],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #13R
    [
        # PL
        [17],
        # PR
        [3, 8, 14, 25, 1, 2, 4, 5],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
    #14R
    [
        # PL
        [],
        # PR
        [8, 14, 25],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #15R
    [
        # PL
        [8, 14, 25],
        # PR
        [16, 20],
        # CL
        [3, 8, 14, 25],
        # CR
        [17],
    ],
    #16R
    [
        # PL
        [8, 14, 25],
        # PR
        [16, 20],
        # CL
        [17],
        # CR
        [3, 8, 14, 25, 1, 2, 4, 5],
    ],
]

claves = [
    #3R
    [
        [1, 22],
        [3, 22],
    ],
    #4R
    [
        [1, 22],
        [3, 22],
        [4, 42, 43, 45, 46],
    ],
    #5R
    [
        [1, 42, 43, 45, 46],
        [2, 22],
        [4, 22],
        [5, 42, 43, 45, 46],
    ],
    #6R
    [
        [2, 22],
        [3, 44],
        [4, 22],
        [6, 22],
    ],
    #7R
    [
        [1, 19, 23],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
    ],
    #8R
    [
        [1, 19, 23],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
        [8, 42, 43, 45, 46],
    ],
    #9R
    [
        [1, 42, 43, 45, 46],
        [2, 22],
        [4, 22],
        [5, 44],
        [6, 22],
        [8, 22],
        [9, 42, 43, 45, 46]
    ],
    #10R
    [
        [2, 22],
        [3, 44],
        [4, 22],
        [6, 22],
        [7, 44],
        [8, 22],
        [10, 22],
    ],
    #11R
    [
        [1, 22],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
        [8, 44],
        [9, 22],
        [11, 22]
    ],
    #12R
    [
        [1, 22],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
        [8, 44],
        [9, 22],
        [11, 22],
        [12, 42, 43, 45, 46],
    ],
    #13R
    [
        [1, 42, 43, 45, 46],
        [2, 22],
        [4, 22],
        [5, 44],
        [6, 22],
        [8, 22],
        [9, 44],
        [10, 22],
        [12, 22],
        [13, 42, 43, 45, 46],
    ],
    #14R
    [
        [2, 22],
        [3, 44],
        [4, 22],
        [6, 22],
        [7, 44],
        [8, 22],
        [10, 22],
        [11, 44],
        [12, 22],
        [14, 22],
    ],
    #15R
    [
        [1, 19, 23],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
        [8, 44],
        [9, 22],
        [11, 22],
        [12, 44],
        [13, 22],
        [15, 22],
    ],
    #16R
    [
        [1, 19, 23],
        [3, 22],
        [4, 44],
        [5, 22],
        [7, 22],
        [8, 44],
        [9, 22],
        [11, 22],
        [12, 44],
        [13, 22],
        [15, 22],
        [16, 42, 43, 45, 46]
    ],
]


# Devuelve el bit en la posición índice de bits [1...32]
def obtener_bit(indice, bits):
    return ((bits >> (32 - indice)) & 0x1)

# Dado un índice de la salida [1...32] de la función F, devuelve el índice de la SBox del que proviene
def detectar_SBox(indice):
    salida = (0x1 << (32 - indice))
    salida_SBoxes = DES.permutar_inv(DES, salida)
    bit_activo = 32
    while salida_SBoxes % 2 == 0:
        salida_SBoxes = salida_SBoxes >> 1
        bit_activo -= 1
    return ((bit_activo - 1) // 4) + 1

# Dado el valor de dos xors de elementos marcados por cada máscara, devuelve True si la
# clave proporcionada cumple ambas condiciones, False en caso contrario.
def comprobar_xors(clave_test, mascara_xor_r1, xor_clave_r1, mascara_xor_rn, xor_clave_rn):
    if bin(mascara_xor_r1 & clave_test).count('1') % 2 != xor_clave_r1:
        return False
    if bin(mascara_xor_rn & clave_test).count('1') % 2 != xor_clave_rn:
        return False
    return True

# Función que implementa la obtención de bits de la clave mediante criptoanálisis lineal,
# cuyo funcionamiento está descrito en la memoria del trabajo.
def ataque(N, n_rondas, planos, cifrados):
    contador_n = 0
    contador_1 = 0
    SBoxes_objetivo_n = set()
    SBoxes_objetivo_1 = set()

    for bit in expresiones[n_rondas-4][3]:
        SBoxes_objetivo_n.add(detectar_SBox(bit))
    SBoxes_objetivo_n = list(SBoxes_objetivo_n)
    SBoxes_n = len(SBoxes_objetivo_n)
    contadores_n = np.zeros(64**SBoxes_n)

    for bit in expresiones[n_rondas-4][1]:
        SBoxes_objetivo_1.add(detectar_SBox(bit))
    SBoxes_objetivo_1 = list(SBoxes_objetivo_1)
    SBoxes_1 = len(SBoxes_objetivo_1)
    contadores_1 = np.zeros(64**SBoxes_1)

    for i in range(N):
        plano = planos[i]
        cifrado = cifrados[i]
        plano_l = plano >> 32
        plano_r = plano & 0xffffffff
        cifrado_l = cifrado >> 32
        cifrado_r = cifrado & 0xffffffff
        # Primero descifrando la última ronda
        expresion_parcial_n = 0
        for bit in expresiones[n_rondas-4][0]:
            expresion_parcial_n = expresion_parcial_n ^ obtener_bit(bit, plano_l)
        for bit in expresiones[n_rondas-4][1]:
            expresion_parcial_n = expresion_parcial_n ^ obtener_bit(bit, plano_r)
        for bit in expresiones[n_rondas-4][2]:
            expresion_parcial_n = expresion_parcial_n ^ obtener_bit(bit, cifrado_r)
        for bit in expresiones[n_rondas-4][3]:
            expresion_parcial_n = expresion_parcial_n ^ obtener_bit(bit, cifrado_l)
        for parte_subclave in range(64**SBoxes_n):
            subclave = 0
            for (i,SBox) in enumerate(SBoxes_objetivo_n):
                subclave = subclave | (((parte_subclave >> (6*i)) & 0b111111) << ((8 - SBox) * 6))
            F = des.feistel(cifrado_r, subclave)
            F_exp = 0
            for bit in expresiones[n_rondas-4][3]:
                F_exp = F_exp ^ obtener_bit(bit, F)
            if expresion_parcial_n ^ F_exp == 0:
                contadores_n[parte_subclave] += 1
                contador_n += 1

        # Después descifrando la primera
        expresion_parcial_1 = 0
        for bit in expresiones[n_rondas-4][0]:
            expresion_parcial_1 = expresion_parcial_1 ^ obtener_bit(bit, plano_r)
        for bit in expresiones[n_rondas-4][1]:
            expresion_parcial_1 = expresion_parcial_1 ^ obtener_bit(bit, plano_l)
        for bit in expresiones[n_rondas-4][2]:
            expresion_parcial_1 = expresion_parcial_1 ^ obtener_bit(bit, cifrado_l)
        for bit in expresiones[n_rondas-4][3]:
            expresion_parcial_1 = expresion_parcial_1 ^ obtener_bit(bit, cifrado_r)
        for parte_subclave in range(64**SBoxes_1):
            subclave = 0
            for (i,SBox) in enumerate(SBoxes_objetivo_1):
                subclave = subclave | (((parte_subclave >> (6*i)) & 0b111111) << ((8 - SBox) * 6))
            F = des.feistel(plano_r, subclave)
            F_exp = 0
            for bit in expresiones[n_rondas-4][1]:
                F_exp = F_exp ^ obtener_bit(bit, F)
            if expresion_parcial_1 ^ F_exp == 0:
                contadores_1[parte_subclave] += 1
                contador_1 += 1

    # Aplicamos el algoritmo 2 de Matsui para hacer las estimaciones
    max = np.max(contadores_1)
    min = np.min(contadores_1)
    if contador_1 > N/2:
        if prob > 0.5:
            xor_clave_r1 = 0
        else:
            xor_clave_r1 = 1
    else:
        if prob > 0.5:
            xor_clave_r1 = 1
        else:
            xor_clave_r1 = 0

    if np.abs(max-N/2) > np.abs(min-N/2):
        parte_subclave_1 = np.argmax(contadores_1)
    else:
        parte_subclave_1 = np.argmin(contadores_1)

    max = np.max(contadores_n)
    min = np.min(contadores_n)

    if contador_n > N/2:
        if prob > 0.5:
            xor_clave_rn = 0
        else:
            xor_clave_rn = 1
    else:
        if prob > 0.5:
            xor_clave_rn = 1
        else:
            xor_clave_rn = 0

    if np.abs(max-N/2) > np.abs(min-N/2):
        parte_subclave_n = np.argmax(contadores_n)
    else:
        parte_subclave_n = np.argmin(contadores_n)

    subclave_n = 0
    mascara_n = 0
    for (i,SBox) in enumerate(SBoxes_objetivo_n):
        subclave_n = subclave_n | (((parte_subclave_n >> (6*i)) & 0b111111) << ((8 - SBox) * 6))
        mascara_n = mascara_n | (0b111111 << ((8 - SBox) * 6))

    subclave_1 = 0
    mascara_1 = 0
    for (i,SBox) in enumerate(SBoxes_objetivo_1):
        subclave_1 = subclave_1 | (((parte_subclave_1 >> (6*i)) & 0b111111) << ((8 - SBox) * 6))
        mascara_1 = mascara_1 | (0b111111 << ((8 - SBox) * 6))

    return mascara_1, mascara_n, subclave_1, subclave_n, xor_clave_r1, xor_clave_rn



def fuerza_bruta(n_rondas, mascara, clave, des, mascara_xor_r1, xor_clave_r1, mascara_xor_rn, xor_clave_rn):
    cadena = ''
    placeholder = 'A'
    mascara_parcial = mascara
    clave_parcial = clave
    for i in range(64):
        if mascara_parcial % 2 == 1:
            cadena += str(clave_parcial % 2)
        else:
            if i % 8 == 0:
                cadena += '_'
            else:
                cadena += placeholder
                placeholder = chr(ord(placeholder) + 1)
                if placeholder == '_':
                    placeholder = chr(ord(placeholder) + 1)
        clave_parcial = clave_parcial >> 1
        mascara_parcial = mascara_parcial >> 1
    cadena = cadena[::-1]

    print(cadena)

    plano = randint(0, 0xffffffffffffffff)
    cifrado = des.des(plano)

    bits_a_descubrir = 56 - bin(mascara).count('1')

    for i in range(2**bits_a_descubrir):
        placeholder = 'A'
        clave_test = clave.item()
        for j in range(bits_a_descubrir):
            nuevo_bit = ((i >> j) & 1) << (63 - cadena.index(placeholder))
            clave_test = clave_test | nuevo_bit
            placeholder = chr(ord(placeholder) + 1)
            if placeholder == '_':
                placeholder = chr(ord(placeholder) + 1)
        if not comprobar_xors(clave_test, mascara_xor_r1, xor_clave_r1, mascara_xor_rn, xor_clave_rn):
            continue
        des_test = DES(clave_test, n_rondas)
        if des_test.des(plano) == cifrado:
            des_test.calcular_paridad()
            return des_test.clave

n_rondas = 4
clave = randint(0, 0xffffffffffffffff)

prob = 0.5 + sesgos[n_rondas-4]

des = DES(clave, n_rondas)

muestras = 3000

N = np.ceil(8*np.abs(prob - 0.5) ** -2).astype('int')

tomas = 10

intervalos = [round(N/tomas * i) for i in range(1, tomas + 1)]

probs_exito = []

# Por cada valor de N que queremos estudiar
for N in intervalos:
    prob_exito = 0
    # Tomamos un número de muestras para cada ejemplo
    for _ in range(muestras):
        planos = []
        cifrados = []
        contador_1 = 0
        contador_n = 0
        for i in range(N):
            contadores_1 = np.zeros(64)
            contadores_n = np.zeros(64)
            plano = randint(0, 0xffffffffffffffff)
            cifrado = des.des(plano)
            planos.append(plano)
            cifrados.append(cifrado)

        # Realizamos el ataque propiamente dicho
        mascara_1, mascara_n, subclave_1, subclave_n, xor_clave_r1, xor_clave_rn = ataque(N, n_rondas, planos, cifrados)

        mascara_1 = des.deshacer_subclave_n(mascara_1, 1)
        mascara_n = des.deshacer_subclave_n(mascara_n, n_rondas)
        mascara = mascara_1 | mascara_n
        parte_clave_1 = des.deshacer_subclave_n(subclave_1, 1)
        parte_clave_n = des.deshacer_subclave_n(subclave_n, n_rondas)
        parte_clave = parte_clave_1 | parte_clave_n

        if (clave & mascara) ^ parte_clave == 0:
            prob_exito += 1
    probs_exito.append(prob_exito/muestras * 100)
    print(N)
    print(prob_exito/muestras)

plt.plot(intervalos, probs_exito)
plt.title('Probabilidad de éxito (%)')
plt.xlabel('Nº de textos usados')
plt.ylabel('Probabilidad')
plt.savefig('exito_lineal_4R_10_3000.png', format='png')



