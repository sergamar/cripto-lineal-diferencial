from DES_personalizado import DES
import sys
import numpy as np
from random import randint
import keras as K

def recall(y_true, y_pred):
    true_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true * y_pred, 0, 1)))
    total_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true, 0, 1)))
    recall = true_positives / total_positives
    return recall

def precision(y_true, y_pred):
    true_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.backend.sum(K.backend.round(K.backend.clip(y_pred, 0, 1)))
    precision = true_positives / predicted_positives
    return precision

def f1(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * ((p * r) / (p + r))

custom_functions = {
    'recall': recall,
    'precision': precision,
    'f1': f1
}

def bits_a_lista(dif):
    dif_lista = []
    for i in range(64):
        dif_lista.append(dif % 2)
        dif = dif >> 1
    dif_lista.reverse()
    return dif_lista

if len(sys.argv) < 2:
    print("El uso del programa es: python3 DES_dif_4R.py clave")
    print("La clave debe proporcionarse en formato hexadecimal")
    exit()

clave = int(sys.argv[1], 16)
# Almacenaremos las veces que cada uno de los posibles candidatos a subclave cumpla la ecuación para cada S-Box de la 2 a la 8
posibilidades = np.zeros((7,64), dtype=int)

des = DES(clave, 4)
des.comprobar_paridad()

# Cargamos la red neuronal que distingue diferenciales de salida provenientes de 0x2000000000000000
model = K.models.load_model('model_full_4R.h5', custom_objects=custom_functions)

# Detectamos 15 (algo más del doble de diferenciales necesarios en el ataque por texto plano conocido) diferenciales provenientes del diferencial de entrada objetivo
textos_cifrados = []
encontrados = 0
iters = 0
while len(textos_cifrados) < 15:
    iters += 1
    plano1 = randint(0, 0xffffffffffffffff)
    plano2 = randint(0, 0xffffffffffffffff)
    cifrado1 = des.des(plano1)
    cifrado2 = des.des(plano2)
    diferencial = cifrado1^cifrado2
    pred = model.predict([bits_a_lista(diferencial)])
    # Si la red neuronal identifica el diferencial como proveniente del diferencial buscado, guardamos los dos textos cifrados
    if pred[0][0] > pred[0][1]:
        encontrados += 1
        print('Diferenciales detectados: ', encontrados)
        print(hex(plano1^plano2))
        print(pred[0][0], pred[0][1])
        textos_cifrados.append([cifrado1, cifrado2])

print('Se han necesitado ' + str(iters) + ' parejas de textos cifrados hasta encontrar los 15 diferenciales')

for pareja in textos_cifrados:
    cifrado1 = pareja[0]
    cifrado2 = pareja[1]
    S_E1 = des.expandir(cifrado1 & 0xffffffff)
    S_E2 = des.expandir(cifrado2 & 0xffffffff)
    l_dif = (cifrado1^cifrado2) >> 32
    # Solo usaremos las S-Boxes de 2 a 8
    S_O_dif = des.permutar_inv(l_dif)
    for i in range(1, 8):
        for clave_parcial in range(64):
            entrada_1 = ((S_E1 >> (48-6*(i+1))) & 0b111111) ^ clave_parcial
            fila_1 = ((entrada_1 >> 4) & 0b10) ^ (entrada_1 & 0b1)
            columna_1 = (entrada_1 >> 1) & 0b1111
            entrada_2 = ((S_E2 >> (48-6*(i+1))) & 0b111111) ^ clave_parcial
            fila_2 = ((entrada_2 >> 4) & 0b10) ^ (entrada_2 & 0b1)
            columna_2 = (entrada_2 >> 1) & 0b1111
            if des.S[i][fila_1][columna_1] ^ des.S[i][fila_2][columna_2] == ((S_O_dif >> (32-4*(i+1))) & 0b1111):
                posibilidades[i-1][clave_parcial] += 1

subclave = 0
for contador in posibilidades:
    parte = contador.argmax()
    subclave = subclave << 6
    subclave = subclave | parte

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

print('Clave obtenida: 0b'+ resultado)
print('Clave real:     '+ bin(clave))

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