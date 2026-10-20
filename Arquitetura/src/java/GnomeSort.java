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

    }
}
