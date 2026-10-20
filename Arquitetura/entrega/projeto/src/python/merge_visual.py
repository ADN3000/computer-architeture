import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vetor_dados import VETOR

vetor = VETOR.copy()

def desenhar(v, operacoes, comparacoes, trocas, inicio, taxa, final=False):
    os.system("clear")
    print("归并排序 — 实时可视化")
    print("=" * 70)
    print(f"元素数量：{len(v):,}")
    print(f"比较次数：{comparacoes:,}")
    print(f"合并操作次数：{operacoes:,}")
    print(f"数组写入次数：{trocas:,}")
    print(f"已用时间：{time.perf_counter() - inicio:.2f} s")
    print(f"每秒操作次数：{taxa:,.0f}")
    print()

    largura = 70
    amostra = v[::max(1, len(v) // largura)][:largura]
    minimo, maximo = min(v), max(v)
    intervalo = max(1, maximo - minimo)

    for valor in amostra:
        tamanho = int((valor - minimo) / intervalo * 40) + 1
        print(" " * (40 - tamanho) + "█" * tamanho)

    print("-" * 70)
    print("每一列代表数组中的一个样本。")
    print("图表显示数值的分布。")
    print("状态：", "已排序" if final else "正在排序……")

def merge_sort(v):
    comparacoes = 0
    operacoes = 0
    escritas = 0
    inicio = time.perf_counter()
    ultimo_tempo = inicio
    operacoes_intervalo = 0

    desenhar(v, operacoes, comparacoes, escritas, inicio, 0)
    time.sleep(0.5)

    def ordenar(esquerda, direita):
        nonlocal comparacoes, operacoes, escritas
        nonlocal ultimo_tempo, operacoes_intervalo

        if direita - esquerda <= 1:
            return

        meio = (esquerda + direita) // 2
        ordenar(esquerda, meio)
        ordenar(meio, direita)

        temporario = []
        i, j = esquerda, meio

        while i < meio and j < direita:
            comparacoes += 1
            operacoes += 1
            operacoes_intervalo += 1

            if v[i] <= v[j]:
                temporario.append(v[i])
                i += 1
            else:
                temporario.append(v[j])
                j += 1

        temporario.extend(v[i:meio])
        temporario.extend(v[j:direita])

        v[esquerda:direita] = temporario
        escritas += len(temporario)

        if operacoes and operacoes % 10000 < len(temporario):
            agora = time.perf_counter()
            duracao = agora - ultimo_tempo
            taxa = operacoes_intervalo / duracao if duracao > 0 else 0
            desenhar(v, operacoes, comparacoes, escritas, inicio, taxa)
            ultimo_tempo = time.perf_counter()
            operacoes_intervalo = 0
            time.sleep(0.03)

    ordenar(0, len(vetor))

    agora = time.perf_counter()
    taxa = operacoes_intervalo / (agora - ultimo_tempo) if agora > ultimo_tempo else 0
    desenhar(vetor, operacoes, comparacoes, escritas, inicio, taxa, True)

    print(f"\n总耗时：{time.perf_counter() - inicio:.2f} s")
    print("数组是否正确排序：", vetor == sorted(VETOR))

if __name__ == "__main__":
    merge_sort(vetor)
