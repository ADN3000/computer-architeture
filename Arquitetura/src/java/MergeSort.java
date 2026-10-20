public class MergeSort {

    private static void merge(
        int[] vetor,
        int[] auxiliar,
        int inicio,
        int meio,
        int fim
    ) {
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

    private static void mergeSort(
        int[] vetor,
        int[] auxiliar,
        int inicio,
        int fim
    ) {
        if (inicio >= fim) {
            return;
        }

        int meio = inicio + (fim - inicio) / 2;

        mergeSort(vetor, auxiliar, inicio, meio);
        mergeSort(vetor, auxiliar, meio + 1, fim);

        merge(vetor, auxiliar, inicio, meio, fim);
    }

    public static void main(String[] args) {
        // Usa o vetor fixo da classe; a ordenação modifica o array em memória.
        int[] vetor = VetorDados.VALORES;

        // Reserva o vetor auxiliar antes da ordenação.
        int[] auxiliar = new int[VetorDados.QUANTIDADE];

        mergeSort(
            vetor,
            auxiliar,
            0,
            vetor.length - 1
        );

    }
}
