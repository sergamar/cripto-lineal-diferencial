from speck import SpeckCipher
from random import randint

ejemplos = 1000000

if __name__ == "__main__":
    clave = randint(0, 0xffffffffffffffffffffffff) # 12 bytes
    cipher = SpeckCipher(clave, 96, 96, 'ECB', 'dataset_2R_96_dir_train_test.txt')
    for i in range(ejemplos):
        plano = randint(0, 0xffffffffffffffffffffffff) # 12 bytes
        cipher.encrypt(plano)