from DES_personalizado import DES

expresiones_elegidas = [0] * 8
sesgos = [0] * 8
# Para cada S-Box
for i in range(8):
    sesgo = 0
    # Para cada posible expresión de la forma a_1X_1+...+a_6X_6 = b_1Y_1+...+b_4Y_4
    for expresion in range(1024):
        # Si todas las a_i o todos los b_i son 0, la ignoramos
        if (expresion & 0b1111 == 0 or ((expresion & 0b1111110000) >> 4) == 0):
            continue
        favorables = 0
        # Por cada posible valor de la entrada de esa S-Box
        for entrada in range(64):
            fila = (entrada & 0b1) | ((entrada & 0b100000) >> 4)
            columna = (entrada & 0b011110) >> 1
            salida = DES.S[i][fila][columna]
            izq = expresion >> 4 & entrada
            der = (expresion & 0b1111) & salida
            # Si se cumple la expresión incrementamos el contador de favorables
            if (bin(izq).count('1') % 2) == (bin(der).count('1') % 2):
                favorables += 1
        # Si la expresión actual tiene más sesgo que la que teníamos guardada previamente, la sobreescribimos
        if abs(favorables - 32) > sesgo:
            sesgo = abs(favorables - 32)
            sesgos[i] = favorables - 32
            expresiones_elegidas[i] = expresion

# Imprimimos la expresión lineal con más sesgo de cada S-Box
print('Las expresiones para cada S-box son:')
for i in range(8):
    print('S-box {} -> Expresión: {:010b}    Sesgo: {}/64'. format(i+1, expresiones_elegidas[i], sesgos[i]))

