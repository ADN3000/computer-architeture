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
    # Copia os dados para preservar o vetor original do módulo.
    vetor = VETOR

    gnome_sort(vetor)

    # Verifica se a ordenação está correta.
    assert len(vetor) == QUANTIDADE
    assert all(
        vetor[i] >= vetor[i - 1]
        for i in range(1, len(vetor))
    )

    print(
        f"Gnome Sort: vetor ordenado com sucesso "
        f"({QUANTIDADE} elementos)."
    )
    print("Primeiros 10 elementos ordenados:")
    print(*vetor[:10])

    print("Últimos 10 elementos ordenados:")
    print(*vetor[-10:])


if __name__ == "__main__":
    main()
