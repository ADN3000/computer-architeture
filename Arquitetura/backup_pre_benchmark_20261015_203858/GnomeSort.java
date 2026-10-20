public class GnomeSort {

    public static void main(String[] args) {
        // Copia os valores fixos para preservar o vetor original.
       int[] vetor = VetorDados.VALORES;

        int indice = 0;

        while (indice < vetor.length) {
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

        // Verifica se o vetor foi ordenado corretamente.
        for (int i = 1; i < vetor.length; i++) {
            if (vetor[i] < vetor[i - 1]) {
                System.err.println("ERRO: vetor nao ordenado.");
                System.exit(1);
            }
        }

        System.out.println(
            "Gnome Sort: vetor ordenado com sucesso ("
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
