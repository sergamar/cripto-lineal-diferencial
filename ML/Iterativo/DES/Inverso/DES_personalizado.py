class DES:

    S = [
        #S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
        #S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
            ],
        #S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
            ],
        #S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
            ],
        #S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
            ],
        #S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
            ],
        #S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
            ],
        #S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
            ]
        ]

    PC_1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ]

    PC_2 = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ]

    E = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]

    P = [
            16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25,
        ]

    P_1 = [
            9, 17, 23, 31,
            13, 28, 2, 18,
            24, 16, 30, 6,
            26, 20, 10, 1,
            8, 14, 25, 3,
            4, 29, 11, 19,
            32, 12, 22, 7,
            5, 27, 15, 21
        ]

    KS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self, clave, rondas):
        self.clave = clave
        self.rondas = rondas

    # Permuted Choice 1 del DES
    def PC1(self, bits):
        reduc = 0
        for bit in self.PC_1:
            reduc = reduc << 1
            reduc = reduc | ((bits >> (64 - bit)) & 0x1)
        return reduc

    # Inversa de la Permuted Choice 1 del DES
    def PC1_1(self, bits):
        entrada = 0
        i = 1
        for bit in self.PC_1:
            entrada = entrada | (((bits >> (56 - i)) & 0x1) << (64 - bit))
            i += 1
        return entrada

    # Permuted Choice 2 del DES
    def PC2(self, bits):
        salida = 0
        for bit in self.PC_2:
            salida = salida << 1
            salida = salida | ((bits >> (56 - bit)) & 0x1)
        return salida

    # Inversa de la Permuted Choice 2 del DES
    def PC2_1(self, bits):
        entrada = 0
        i = 1
        for bit in self.PC_2:
            entrada = entrada | (((bits >> (48 - i)) & 0x1) << (56 - bit))
            i += 1
        return entrada

    # Comprobación y corrección de la paridad de una clave
    def comprobar_paridad(self):
        nueva_clave = 0
        for i in range(8):
            byte = (self.clave & (0xff << (56 - 8*i))) >> (56 - 8*i)
            byte_correcto = (byte & 0b11111110)| (1 - (bin(byte >> 1).count('1') % 2))
            if byte != byte_correcto:
                self.calcular_paridad()
                print("La paridad de la clave suministrada es incorrecta, se ha recalculado y el resultado es: ", hex(self.clave))
                break

    # Cálculo de la paridad de una clave
    def calcular_paridad(self):
        nueva_clave = 0
        for i in range(8):
            byte = (self.clave & (0xff << (56 - 8*i))) >> (56 - 8*i)
            byte = (byte & 0b11111110)| (1 - (bin(byte >> 1).count('1') % 2))
            nueva_clave = nueva_clave << 8
            nueva_clave = nueva_clave | byte
        self.clave = nueva_clave

    # Subrutina de generación de subclaves
    def generar_subclaves(self):
        subclaves = []
        reduc = self.PC1(self.clave)
        l = (reduc >> 28) & 0xfffffff
        r = reduc & 0xfffffff
        for i in range(self.rondas):
            if self.KS[i] == 1:
                bits_l = l >> 27
                bits_r = r >> 27
            else:
                bits_l = l >> 26
                bits_r = r >> 26
            l = ((l << self.KS[i]) & 0xfffffff) ^ bits_l
            r = ((r << self.KS[i]) & 0xfffffff) ^ bits_r
            subclaves.append(self.PC2((l << 28) ^ r))
        return subclaves

    # Traducción de los bits de la subclave de la ronda n a sus
    # correspondientes bits de la clave original
    def deshacer_subclave_n(self, subclave, n):
        entrada = self.PC2_1(subclave)
        l = entrada >> 28
        r = entrada & 0xfffffff
        for despl in reversed(self.KS[:n]):
            if despl == 1:
                l = (l >> 1) | (l & 0b1) << 27
                r = (r >> 1) | (r & 0b1) << 27
            elif despl == 2:
                l = (l >> 2) | (l & 0b11) << 26
                r = (r >> 2) | (r & 0b11) << 26
        return self.PC1_1(l << 28 | r)

    # Traducción de los bits de la subclave de la última ronda a sus
    # correspondientes bits de la clave original
    def deshacer_subclave(self, subclave):
        return self.deshacer_subclave_n(subclave, self.rondas)

    # Salida de las 8 S-Boxes dada una entrada determinada
    def salida_SBOXES(self, entrada):
        salida = 0
        for i in range(8):
            inp = (entrada >> 6*(7 - i)) & 0b111111
            fila = ((inp >> 4) & 0b10) ^ (inp & 0b1)
            columna = (inp >> 1) & 0b1111
            salida = salida << 4
            salida = salida ^ self.S[i][fila][columna]
        return salida

    # Permutación P del DES
    def permutar(self, s):
        p = 0
        for bit in self.P:
            p = p << 1
            p = p ^ ((s >> (32 - bit)) & 0x1)
        return p

    # Función inversa de la permutación P del DES
    def permutar_inv(self, s):
        p = 0
        for bit in self.P_1:
            p = p << 1
            p = p ^ ((s >> (32 - bit)) & 0x1)
        return p

    # Función que traduce una fila y columna de una S-Box a la entrada correspondiente
    # que se debe introducir a la S-Box
    def entrada_fc(self, fila, columna):
        entrada = 0
        if fila == 2 or fila == 3:
            entrada = 1
        entrada = entrada << 4
        entrada = entrada ^ columna
        entrada = entrada << 1
        if fila == 1 or fila == 3:
            entrada = entrada ^ 1
        return entrada

    # Expansión E del DES
    def expandir(self, r):
        e = 0
        for bit in self.E:
            e = e << 1
            e = e ^ ((r >> (32 - bit)) & 0x1)
        return e

    # Función F del DES
    def feistel(self, r, subclave):
        e = self.expandir(r)
        entrada = e ^ subclave
        s = self.salida_SBOXES(entrada)
        return self.permutar(s)

    # Ronda del DES
    def ronda(self, l, r, subclave):
        temp = r
        r = l ^ self.feistel(r, subclave)
        l = temp
        return l, r

    # Cifrado DES
    def des(self, plano):
        l = plano >> 32
        r = plano & 0xffffffff
        subclaves = self.generar_subclaves()
        for i in range(self.rondas):
            l,r = self.ronda(l, r, subclaves[i])
        temp = l
        l = r
        r = temp
        return l << 32 | r
