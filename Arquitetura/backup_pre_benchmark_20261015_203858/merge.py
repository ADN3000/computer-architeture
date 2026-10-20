from vetor_dados import VETOR, QUANTIDADE


def merge(vetor, auxiliar, inicio, meio, fim):
    i = inicio
    j = meio + 1
    k = inicio

    while i <= meio and j <= fim:
        if vetor[i] <= vetor[j]:
            auxiliar[k] = vetor[i]
            i += 1
        else:
            auxiliar[k] = vetor[j]
            j += 1

        k += 1

    while i <= meio:
        auxiliar[k] = vetor[i]
        i += 1
        k += 1

    while j <= fim:
        auxiliar[k] = vetor[j]
        j += 1
        k += 1

    for i in range(inicio, fim + 1):
        vetor[i] = auxiliar[i]


def merge_sort(vetor, auxiliar, inicio, fim):
    if inicio >= fim:
        return

    meio = inicio + (fim - inicio) // 2

    merge_sort(vetor, auxiliar, inicio, meio)
    merge_sort(vetor, auxiliar, meio + 1, fim)

    merge(vetor, auxiliar, inicio, meio, fim)


def main():
    # Copia os dados fixos para preservar o vetor original.
    vetor = VETOR

    # Aloca a memória auxiliar antes de iniciar a ordenação.
    auxiliar = [0] * QUANTIDADE

    merge_sort(vetor, auxiliar, 0, QUANTIDADE - 1)

    # Verifica a quantidade e a ordem dos elementos.
    assert len(vetor) == QUANTIDADE
    assert all(
        vetor[i] >= vetor[i - 1]
        for i in range(1, len(vetor))
    )

    print(
        f"Merge Sort: vetor ordenado com sucesso "
        f"({QUANTIDADE} elementos)."
    )

    print("Primeiros 10 elementos ordenados:")
    print(*vetor[:10])

    print("Últimos 10 elementos ordenados:")
    print(*vetor[-10:])


if __name__ == "__main__":
    main()
