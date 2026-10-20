#include <stdio.h>
#include <stdbool.h>
#include "vetor_dados.h"

int main(void) {
    int indice = 0;

    while (indice < QUANTIDADE) {
        if (indice == 0) {
            indice++;
        } else if (vetor[indice] >= vetor[indice - 1]) {
            indice++;
        } else {
            int temporario = vetor[indice];
            vetor[indice] = vetor[indice - 1];
            vetor[indice - 1] = temporario;
            indice--;
        }
    }

    return 0;
}
