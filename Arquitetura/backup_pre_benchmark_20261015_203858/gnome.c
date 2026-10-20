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

    // Verifica se o vetor ficou ordenado.
    for (int i = 1; i < QUANTIDADE; i++) {
        if (vetor[i] < vetor[i - 1]) {
            fprintf(stderr, "ERRO: vetor nao ordenado.\n");
            return 1;
        }
    }

    // Exibe apenas uma confirmação, sem imprimir o vetor inteiro.
    printf("Gnome Sort: vetor ordenado com sucesso (%d elementos).\n",
           QUANTIDADE);

    printf("Primeiros 10 elementos ordenados:\n");
    for (int i = 0; i < 10; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");

    printf("Ultimos 10 elementos ordenados:\n");
    for (int i = QUANTIDADE - 10; i < QUANTIDADE; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");

    return 0;
}
