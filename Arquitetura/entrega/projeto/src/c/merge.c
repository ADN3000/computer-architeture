#include <stdio.h>
#include <stdlib.h>
#include "vetor_dados.h"

int auxiliar[QUANTIDADE];

void merge(int inicio, int meio, int fim) {
    int i = inicio;
    int j = meio + 1;
    int k = inicio;

    while (i <= meio && j <= fim) {
        if (vetor[i] <= vetor[j]) {
            auxiliar[k++] = vetor[i++];
        } else {
            auxiliar[k++] = vetor[j++];
        }
    }

    while (i <= meio) {
        auxiliar[k++] = vetor[i++];
    }

    while (j <= fim) {
        auxiliar[k++] = vetor[j++];
    }

    for (i = inicio; i <= fim; i++) {
        vetor[i] = auxiliar[i];
    }
}

void merge_sort(int inicio, int fim) {
    if (inicio >= fim) {
        return;
    }

    int meio = inicio + (fim - inicio) / 2;

    merge_sort(inicio, meio);
    merge_sort(meio + 1, fim);
    merge(inicio, meio, fim);
}

int main(void) {
    merge_sort(0, QUANTIDADE - 1);

    return 0;
}
