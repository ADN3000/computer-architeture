from vetor_dados import VETOR, QUANTIDADE


def gnome_sort(vetor):
    indice = 0
    tamanho = len(vetor)

    while indice < tamanho:
        if indice == 0:
            indice += 1
        elif vetor[indice] >= vetor[indice - 1]:
            indice += 1
        else:
            vetor[indice], vetor[indice - 1] = (
                vetor[indice - 1],
                vetor[indice]
            )
            indice -= 1


def main():
    # Usa a lista fixa do módulo; a ordenação modifica a lista em memória.
    vetor = VETOR

    gnome_sort(vetor)


if __name__ == "__main__":
    main()
