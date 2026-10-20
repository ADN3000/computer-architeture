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
        // Copia os dados fixos antes de iniciar a ordenação.
        int[] vetor = VetorDados.VALORES;

        // Reserva o vetor auxiliar antes da ordenação.
        int[] auxiliar = new int[VetorDados.QUANTIDADE];

        mergeSort(
            vetor,
            auxiliar,
            0,
            vetor.length - 1
        );

        // Verifica a ordenação.
        for (int i = 1; i < vetor.length; i++) {
            if (vetor[i] < vetor[i - 1]) {
                System.err.println("ERRO: vetor nao ordenado.");
                System.exit(1);
            }
        }

        System.out.println(
            "Merge Sort: vetor ordenado com sucesso ("
            + vetor.length + " elementos)."
        );

        System.out.println("Primeiros 10 elementos ordenados:");
        for (int i = 0; i < 10; i++) {
            System.out.print(vetor[i] + " ");
        }
        System.out.println();

        System.out.println("Últimos 10 elementos ordenados:");
        for (int i = vetor.length - 10; i < vetor.length; i++) {
            System.out.print(vetor[i] + " ");
        }
        System.out.println();
    }
}
