#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "rijndael.h"

#define KEYBITS 128
#define DATASET_TRAIN 700000
#define DATASET_TEST 300000

char random_byte()
{
  return (char) (random() % 256);
}

int main(int argc, char **argv)
{
  unsigned long rk[RKLENGTH(KEYBITS)];
  unsigned char key[KEYLENGTH(KEYBITS)];
  unsigned char plaintext[16];
  unsigned char ciphertext[16];
  int i, j;
  int nrounds;
  FILE *fp;
  srandom(time(NULL));
  for (i=0; i<KEYLENGTH(KEYBITS); i++)
  {
    key[i] = random_byte();
  }
  nrounds = rijndaelSetupEncrypt(rk, key, 128);

  fp = fopen("dataset_10R_iter_train.txt", "w");
  for (i=0; i<DATASET_TRAIN; i++)
  {
    for (j=0; j<KEYLENGTH(KEYBITS); j++)
    {
      plaintext[j] = random_byte();
    }
    rijndaelEncrypt(rk, nrounds, plaintext, ciphertext, fp);
  }
  if (fp != NULL)
    fclose(fp);

  fp = fopen("dataset_10R_iter_test.txt", "w");
  for (i=0; i<DATASET_TEST; i++)
  {
    for (j=0; j<KEYLENGTH(KEYBITS); j++)
    {
      plaintext[j] = random_byte();
    }
    rijndaelEncrypt(rk, nrounds, plaintext, ciphertext, fp);
  }
  if (fp != NULL)
    fclose(fp);

}