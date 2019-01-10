#include <stdio.h>
#include <stdlib.h>

// gcc file.c -S -o file.S
// arm-linux-gnueabi-gcc exo1.c -S -o test.asm

int main() {
  int a = 10;
  int b = 16;
  int log_b = 4;
  int res = 1;

  if (b % 2 == 0)
    res = a << log_b;
  else
    res = a * b;
  return res;
}