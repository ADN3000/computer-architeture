import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from vetor_dados import VETOR

vetor = VETOR.copy()

LARGURA = 70
ALTURA = 15
ATUALIZAR_A_CADA = 100_000
INTERVALO = 0.03

def desenhar(v, operacoes, comparacoes, inicio, taxa, final=False):
    os.system("clear")

    maximo = max(v)
    passo = max(1, len(v) // LARGURA)
    amostra = v[::passo][:LARGURA]

    alturas = [
        int(valor / maximo * (ALTURA - 1))
        for valor in amostra
    ]

    print("侏儒排序 — 实时可视化")
    print("=" * LARGURA)
    print(f"元素数量： {len(v)}")
    print(f"比较次数： {comparacoes:,}")
    print(f"交换次数： {operacoes:,}")
    tempo = time.perf_counter() - inicio
    print(f"已用时间： {tempo:.2f} s")
    print(f"每秒操作次数： {taxa:,.0f}")
    print()

    for nivel in range(ALTURA - 1, -1, -1):
        linha = "".join(
            "█" if altura >= nivel else " "
            for altura in alturas
        )
        print(linha)

    print("-" * LARGURA)
    print("每一列代表数组中的一个样本。")
    print("图表显示数值的分布。")
    print("状态： " + ("已排序" if final else "正在排序……"))

def gnome_sort(v):
    indice = 0
    comparacoes = 0
    trocas = 0
    inicio = time.perf_counter()
    operacoes = 0

    ultimo_tempo = inicio
    operacoes_intervalo = 0
    desenhar(v, trocas, comparacoes, inicio, 0)
    time.sleep(0.5)

    while indice < len(v):
        if indice == 0 or v[indice] >= v[indice - 1]:
            indice += 1
        else:
            v[indice], v[indice - 1] = v[indice - 1], v[indice]
            indice -= 1
            trocas += 1

        comparacoes += 1
        operacoes += 1
        operacoes_intervalo += 1

        if operacoes % ATUALIZAR_A_CADA == 0:
            agora = time.perf_counter()
            duracao = agora - ultimo_tempo
            taxa = operacoes_intervalo / duracao if duracao > 0 else 0
            desenhar(v, trocas, comparacoes, inicio, taxa)
            ultimo_tempo = time.perf_counter()
            operacoes_intervalo = 0
            time.sleep(INTERVALO)

    agora = time.perf_counter()
    duracao = agora - ultimo_tempo
    taxa = operacoes_intervalo / duracao if duracao > 0 else 0
    desenhar(v, trocas, comparacoes, inicio, taxa, final=True)

    print(f"\n总耗时： {time.perf_counter() - inicio:.2f} s")
    print("数组是否正确排序：", v == sorted(VETOR))

if __name__ == "__main__":
    gnome_sort(vetor)
