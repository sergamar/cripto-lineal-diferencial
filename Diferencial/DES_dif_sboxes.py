from DES_personalizado import DES

filas = 64
columnas = 16
ocurrencias = []
posibilidades = []
# Primera parte: para cada S-Box
for i in range(8):
    # Generamos una matriz de ocurrencias de cada pareja de diferencias de entrada y de salida
    ocurrencias.append([[0] * columnas for j in range(filas)])
    aux = []
    for k in range(filas):
        aux_fila = []
        for l in range(columnas):
            aux_fila.append(set())
        aux.append(aux_fila)
    # Generamos una matriz donde guardaremos, para cada pareja de diferencias de entrada y salida, las posibles parejas de entradas que la generan
    posibilidades.append(aux)

# Segunda parte: para cada S-Box
for i in range(8):
    # Para cada posible pareja de entradas a la S-Box
    for entrada_1 in range(64):
        fila = (entrada_1 & 0b1) | ((entrada_1 & 0b100000) >> 4)
        columna = (entrada_1 & 0b011110) >> 1
        salida_1 = DES.S[i][fila][columna]
        for entrada_2 in range(64):
            fila = (entrada_2 & 0b1) | ((entrada_2 & 0b100000) >> 4)
            columna = (entrada_2 & 0b011110) >> 1
            salida_2 = DES.S[i][fila][columna]
            # Actualizamos las ocurrencias y las entradas que han dado lugar a ese diferencial
            ocurrencias[i][entrada_1^entrada_2][salida_1^salida_2] += 1
            posibilidades[i][entrada_1^entrada_2][salida_1^salida_2].add(entrada_1)
            posibilidades[i][entrada_1^entrada_2][salida_1^salida_2].add(entrada_2)

# Imprimimos por pantalla, para cada S-Box, las ocurrencias de cada diferencial
for i in range(8):
    print("S-Box {}:".format(i+1))
    for j in range(filas):
        print(ocurrencias[i][j])

# Imprimimos por pantalla, para cada S-Box, las posibles entradas que dan lugar a cada diferencial
for i in range(8):
    print("S-Box {}:".format(i+1))
    for j in range(filas):
        for k in range(columnas):
            if len(posibilidades[i][j][k]) > 0:
                print(hex(j), "->", hex(k), [hex(x) for x in posibilidades[i][j][k]])
            else:
                print(hex(j), "->", hex(k), "[]")

