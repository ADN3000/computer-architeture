#!/usr/bin/python3
"""
Gera os fontes (C, Python e Java) dos algoritmos de ordenação escolhidos,
todos com O MESMO vetor de 6800 posições embutido em tempo de compilação.

Uso:
    python3 gerar_projeto.py insertion quick
    python3 gerar_projeto.py --lista            (mostra os algoritmos)
    python3 gerar_projeto.py --novo-vetor ...   (sorteia outro vetor)

O vetor fica salvo em vetor_6800.txt e é reaproveitado nas próximas
execuções, garantindo que todas as implementações usem os mesmos valores.
"""
import argparse
import os
import random
import sys

TAMANHO = 6800
MAX_VALOR = 9999          # < 32768 (cabe no sipush do Java) e >= 0 (Radix Sort)
ARQ_VETOR = "vetor_6800.txt"

# ---------------------------------------------------------------------------
# Algoritmos. Os códigos de C e Java compartilham a mesma sintaxe básica:
# o Java é derivado do C (static + int[] v). Python é escrito à parte.
# 'extra_c' / 'extra_java' = vetores auxiliares globais (se necessário).
# ---------------------------------------------------------------------------
ALGOS = {}

def algo(chave, nome, pasta, classe, arquivo, complexidade, c, py, call_c, call_py,
         extra_c="", extra_java="", extra_py=""):
    ALGOS[chave] = dict(nome=nome, pasta=pasta, classe=classe, arquivo=arquivo,
                        complexidade=complexidade, c=c.strip("\n"), py=py.strip("\n"),
                        call_c=call_c, call_py=call_py, extra_c=extra_c,
                        extra_java=extra_java, extra_py=extra_py)

algo("insertion", "Insertion Sort", "Insertion", "InsertionSort", "insertionsort", "O(n^2)",
c='''
void insertionSort(int *v, int n) {
    for (int i = 1; i < n; i++) {
        int chave = v[i];
        int j = i - 1;
        while (j >= 0 && v[j] > chave) {
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = chave;
    }
}
''',
py='''
def insertion_sort(v, n):
    for i in range(1, n):
        chave = v[i]
        j = i - 1
        while j >= 0 and v[j] > chave:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = chave
''', call_c="insertionSort(a, MAX);", call_py="insertion_sort(a, MAX)")

algo("quick", "Quick Sort", "Quick", "QuickSort", "quicksort", "O(n log n)",
c='''
void quickSort(int *v, int lo, int hi) {
    if (lo >= hi) return;
    int pivo = v[lo + (hi - lo) / 2];
    int i = lo, j = hi;
    while (i <= j) {
        while (v[i] < pivo) i++;
        while (v[j] > pivo) j--;
        if (i <= j) {
            int t = v[i]; v[i] = v[j]; v[j] = t;
            i++; j--;
        }
    }
    quickSort(v, lo, j);
    quickSort(v, i, hi);
}
''',
py='''
def quick_sort(v, lo, hi):
    if lo >= hi:
        return
    pivo = v[lo + (hi - lo) // 2]
    i = lo
    j = hi
    while i <= j:
        while v[i] < pivo:
            i += 1
        while v[j] > pivo:
            j -= 1
        if i <= j:
            v[i], v[j] = v[j], v[i]
            i += 1
            j -= 1
    quick_sort(v, lo, j)
    quick_sort(v, i, hi)
''', call_c="quickSort(a, 0, MAX - 1);", call_py="quick_sort(a, 0, MAX - 1)")

algo("merge", "Merge Sort", "Merge", "MergeSort", "mergesort", "O(n log n)",
c='''
void mergeSort(int *v, int lo, int hi) {   /* ordena v[lo..hi-1] */
    if (hi - lo < 2) return;
    int mid = (lo + hi) / 2;
    mergeSort(v, lo, mid);
    mergeSort(v, mid, hi);
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (v[i] <= v[j]) aux[k++] = v[i++];
        else              aux[k++] = v[j++];
    }
    while (i < mid) aux[k++] = v[i++];
    while (j < hi)  aux[k++] = v[j++];
    for (k = lo; k < hi; k++) v[k] = aux[k];
}
''',
py='''
def merge_sort(v, lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    merge_sort(v, lo, mid)
    merge_sort(v, mid, hi)
    i = lo
    j = mid
    k = lo
    while i < mid and j < hi:
        if v[i] <= v[j]:
            aux[k] = v[i]
            i += 1
        else:
            aux[k] = v[j]
            j += 1
        k += 1
    while i < mid:
        aux[k] = v[i]
        i += 1
        k += 1
    while j < hi:
        aux[k] = v[j]
        j += 1
        k += 1
    for k in range(lo, hi):
        v[k] = aux[k]
''', call_c="mergeSort(a, 0, MAX);", call_py="merge_sort(a, 0, MAX)",
extra_c="int aux[MAX];", extra_java="static int[] aux = new int[MAX];", extra_py="aux = [0] * MAX")

algo("heap", "Heap Sort", "Heap", "HeapSort", "heapsort", "O(n log n)",
c='''
void peneirar(int *v, int n, int i) {
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && v[l] > v[m]) m = l;
        if (r < n && v[r] > v[m]) m = r;
        if (m == i) return;
        int t = v[i]; v[i] = v[m]; v[m] = t;
        i = m;
    }
}

void heapSort(int *v, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) peneirar(v, n, i);
    for (int fim = n - 1; fim > 0; fim--) {
        int t = v[0]; v[0] = v[fim]; v[fim] = t;
        peneirar(v, fim, 0);
    }
}
''',
py='''
def peneirar(v, n, i):
    while True:
        l = 2 * i + 1
        r = l + 1
        m = i
        if l < n and v[l] > v[m]:
            m = l
        if r < n and v[r] > v[m]:
            m = r
        if m == i:
            return
        v[i], v[m] = v[m], v[i]
        i = m


def heap_sort(v, n):
    for i in range(n // 2 - 1, -1, -1):
        peneirar(v, n, i)
    for fim in range(n - 1, 0, -1):
        v[0], v[fim] = v[fim], v[0]
        peneirar(v, fim, 0)
''', call_c="heapSort(a, MAX);", call_py="heap_sort(a, MAX)")

algo("shell", "Shell Sort", "Shell", "ShellSort", "shellsort", "Depende da sequência de gaps",
c='''
void shellSort(int *v, int n) {
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int tmp = v[i];
            int j = i;
            while (j >= gap && v[j - gap] > tmp) {
                v[j] = v[j - gap];
                j -= gap;
            }
            v[j] = tmp;
        }
    }
}
''',
py='''
def shell_sort(v, n):
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            tmp = v[i]
            j = i
            while j >= gap and v[j - gap] > tmp:
                v[j] = v[j - gap]
                j -= gap
            v[j] = tmp
        gap //= 2
''', call_c="shellSort(a, MAX);", call_py="shell_sort(a, MAX)")

algo("gnome", "Gnome Sort", "Gnome", "GnomeSort", "gnomesort", "O(n^2)",
c='''
void gnomeSort(int *v, int n) {
    int i = 0;
    while (i < n) {
        if (i == 0 || v[i - 1] <= v[i]) {
            i++;
        } else {
            int t = v[i]; v[i] = v[i - 1]; v[i - 1] = t;
            i--;
        }
    }
}
''',
py='''
def gnome_sort(v, n):
    i = 0
    while i < n:
        if i == 0 or v[i - 1] <= v[i]:
            i += 1
        else:
            v[i], v[i - 1] = v[i - 1], v[i]
            i -= 1
''', call_c="gnomeSort(a, MAX);", call_py="gnome_sort(a, MAX)")

algo("cocktail", "Cocktail Sort", "Cocktail", "CocktailSort", "cocktailsort", "O(n^2)",
c='''
void cocktailSort(int *v, int n) {
    int ini = 0, fim = n - 1, trocou = 1;
    while (trocou != 0) {
        trocou = 0;
        for (int i = ini; i < fim; i++) {
            if (v[i] > v[i + 1]) {
                int t = v[i]; v[i] = v[i + 1]; v[i + 1] = t;
                trocou = 1;
            }
        }
        if (trocou == 0) break;
        fim--;
        trocou = 0;
        for (int i = fim; i > ini; i--) {
            if (v[i - 1] > v[i]) {
                int t = v[i]; v[i] = v[i - 1]; v[i - 1] = t;
                trocou = 1;
            }
        }
        ini++;
    }
}
''',
py='''
def cocktail_sort(v, n):
    ini = 0
    fim = n - 1
    trocou = True
    while trocou:
        trocou = False
        for i in range(ini, fim):
            if v[i] > v[i + 1]:
                v[i], v[i + 1] = v[i + 1], v[i]
                trocou = True
        if not trocou:
            break
        fim -= 1
        trocou = False
        for i in range(fim, ini, -1):
            if v[i - 1] > v[i]:
                v[i], v[i - 1] = v[i - 1], v[i]
                trocou = True
        ini += 1
''', call_c="cocktailSort(a, MAX);", call_py="cocktail_sort(a, MAX)")

algo("selection", "Selection Sort", "Selection", "SelectionSort", "selectionsort", "O(n^2)",
c='''
void selectionSort(int *v, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++) {
            if (v[j] < v[min]) min = j;
        }
        if (min != i) {
            int t = v[i]; v[i] = v[min]; v[min] = t;
        }
    }
}
''',
py='''
def selection_sort(v, n):
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if v[j] < v[menor]:
                menor = j
        if menor != i:
            v[i], v[menor] = v[menor], v[i]
''', call_c="selectionSort(a, MAX);", call_py="selection_sort(a, MAX)")

algo("comb", "Comb Sort", "Comb", "CombSort", "combsort", "Omega(n^2 / 2^p) no caso médio",
c='''
void combSort(int *v, int n) {
    int gap = n, trocou = 1;
    while (gap > 1 || trocou != 0) {
        gap = gap * 10 / 13;           /* fator de encolhimento ~1.3 */
        if (gap < 1) gap = 1;
        trocou = 0;
        for (int i = 0; i + gap < n; i++) {
            if (v[i] > v[i + gap]) {
                int t = v[i]; v[i] = v[i + gap]; v[i + gap] = t;
                trocou = 1;
            }
        }
    }
}
''',
py='''
def comb_sort(v, n):
    gap = n
    trocou = True
    while gap > 1 or trocou:
        gap = gap * 10 // 13
        if gap < 1:
            gap = 1
        trocou = False
        for i in range(n - gap):
            if v[i] > v[i + gap]:
                v[i], v[i + gap] = v[i + gap], v[i]
                trocou = True
''', call_c="combSort(a, MAX);", call_py="comb_sort(a, MAX)")

algo("radix", "Radix Sort", "Radix", "RadixSort", "radixsort", "O(d * n)",
c='''
void radixSort(int *v, int n) {
    int maior = v[0];
    for (int i = 1; i < n; i++) if (v[i] > maior) maior = v[i];
    for (int exp = 1; maior / exp > 0; exp *= 10) {
        for (int d = 0; d < 10; d++) cnt[d] = 0;
        for (int i = 0; i < n; i++) cnt[(v[i] / exp) % 10]++;
        for (int d = 1; d < 10; d++) cnt[d] += cnt[d - 1];
        for (int i = n - 1; i >= 0; i--) {
            int d = (v[i] / exp) % 10;
            aux[--cnt[d]] = v[i];
        }
        for (int i = 0; i < n; i++) v[i] = aux[i];
    }
}
''',
py='''
def radix_sort(v, n):
    maior = max(v)
    exp = 1
    while maior // exp > 0:
        for d in range(10):
            cnt[d] = 0
        for i in range(n):
            cnt[(v[i] // exp) % 10] += 1
        for d in range(1, 10):
            cnt[d] += cnt[d - 1]
        for i in range(n - 1, -1, -1):
            d = (v[i] // exp) % 10
            cnt[d] -= 1
            aux[cnt[d]] = v[i]
        for i in range(n):
            v[i] = aux[i]
        exp *= 10
''', call_c="radixSort(a, MAX);", call_py="radix_sort(a, MAX)",
extra_c="int aux[MAX];\nint cnt[10];",
extra_java="static int[] aux = new int[MAX];\nstatic int[] cnt = new int[10];",
extra_py="aux = [0] * MAX\ncnt = [0] * 10")

# ---------------------------------------------------------------------------
# Vetor
# ---------------------------------------------------------------------------
def carregar_vetor(novo, seed):
    if os.path.exists(ARQ_VETOR) and not novo:
        with open(ARQ_VETOR) as f:
            v = [int(x) for x in f.read().split()]
        if len(v) != TAMANHO:
            sys.exit(f"[ERRO] {ARQ_VETOR} não tem {TAMANHO} valores. Use --novo-vetor.")
        print(f"[vetor] reaproveitando {ARQ_VETOR}")
        return v
    rng = random.Random(seed)
    v = [rng.randint(0, MAX_VALOR) for _ in range(TAMANHO)]
    with open(ARQ_VETOR, "w") as f:
        f.write("\n".join(map(str, v)) + "\n")
    print(f"[vetor] novo vetor gerado (seed={seed}) e salvo em {ARQ_VETOR}")
    return v

def formata(v, por_linha=20, indent="    "):
    linhas = [indent + ", ".join(map(str, v[i:i + por_linha])) for i in range(0, len(v), por_linha)]
    return ",\n".join(linhas)

# ---------------------------------------------------------------------------
# Geração dos fontes
# ---------------------------------------------------------------------------
def gera_c(al, vetor):
    return f'''/* {al["nome"]} - complexidade: {al["complexidade"]}
 * Gerado por gerar_projeto.py (vetor global preenchido em tempo de compilacao). */
#include <stdio.h>

#define MAX {TAMANHO}

int a[MAX] = {{
{formata(vetor)}
}};
{al["extra_c"]}

{al["c"]}

int main(int argc, char **argv) {{
    {al["call_c"]}

    if (argc > 1) {{   /* modo de verificacao: so roda com argumento (nao afeta o benchmark) */
        long long soma = 0;
        int ok = 1;
        for (int i = 0; i < MAX; i++) {{
            soma += (long long)a[i] * (i + 1);
            if (i > 0 && a[i - 1] > a[i]) ok = 0;
        }}
        printf("%s soma=%lld\\n", ok ? "ORDENADO" : "ERRO", soma);
    }}
    return 0;
}}
'''

def gera_py(al, vetor):
    extra = ("\n" + al["extra_py"] + "\n") if al["extra_py"] else ""
    return f'''#!/usr/bin/python3
# {al["nome"]} - complexidade: {al["complexidade"]}
# Gerado por gerar_projeto.py (vetor global preenchido no proprio codigo-fonte).
import sys

MAX = {TAMANHO}

a = [
{formata(vetor)}
]
{extra}

{al["py"]}


{al["call_py"]}

if len(sys.argv) > 1:   # modo de verificacao: so roda com argumento
    soma = 0
    ok = True
    for i in range(MAX):
        soma += a[i] * (i + 1)
        if i > 0 and a[i - 1] > a[i]:
            ok = False
    print("ORDENADO" if ok else "ERRO", "soma=%d" % soma)
'''

def gera_java(al, vetor):
    corpo = "static " + al["c"].replace("int *v", "int[] v")
    # métodos auxiliares (ex.: peneirar no Heap) também precisam de static
    corpo = corpo.replace("\n\nvoid ", "\n\nstatic void ")
    corpo = "\n".join("    " + l if l.strip() else l for l in corpo.split("\n"))
    extra = "\n".join("    " + l for l in al["extra_java"].split("\n")) if al["extra_java"] else ""
    call = al["call_c"]
    return f'''// {al["nome"]} - complexidade: {al["complexidade"]}
// Gerado por gerar_projeto.py (vetor membro da classe, preenchido em tempo de compilacao).
public class {al["classe"]} {{
    static final int MAX = {TAMANHO};

    static int[] a = {{
{formata(vetor, indent="        ")}
    }};
{extra}

{corpo}

    public static void main(String[] args) {{
        {call}

        if (args.length > 0) {{   // modo de verificacao: so roda com argumento
            long soma = 0;
            boolean ok = true;
            for (int i = 0; i < MAX; i++) {{
                soma += (long) a[i] * (i + 1);
                if (i > 0 && a[i - 1] > a[i]) ok = false;
            }}
            System.out.println((ok ? "ORDENADO" : "ERRO") + " soma=" + soma);
        }}
    }}
}}
'''

def gera_wrapper_java(al):
    # IMPORTANTE: a ULTIMA linha util deve ser "java NomeDaClasse" - o benchmark.sh
    # usa essa linha para dar nome a barra do grafico.
    return f'#!/bin/bash\n\njava {al["classe"]} "$@"\n'

def escreve(caminho, texto, executavel=False):
    with open(caminho, "w") as f:
        f.write(texto)
    os.chmod(caminho, 0o755 if executavel else 0o644)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("algoritmos", nargs="*", help="chaves: " + ", ".join(ALGOS))
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--novo-vetor", action="store_true", help="sorteia um novo vetor")
    ap.add_argument("--seed", type=int, default=20261006)
    a = ap.parse_args()

    if a.lista or not a.algoritmos:
        print("Algoritmos disponíveis:")
        for k, al in ALGOS.items():
            print(f"  {k:10s} {al['nome']:15s} {al['complexidade']}")
        if not a.lista:
            print("\nExemplo: python3 gerar_projeto.py insertion quick")
        return
    for k in a.algoritmos:
        if k not in ALGOS:
            sys.exit(f"[ERRO] algoritmo desconhecido: {k}")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vetor = carregar_vetor(a.novo_vetor, a.seed)

    for k in a.algoritmos:
        al = ALGOS[k]
        pasta = al["pasta"]
        os.makedirs(pasta, exist_ok=True)
        escreve(f"{pasta}/{al['arquivo']}.c", gera_c(al, vetor))
        escreve(f"{pasta}/{al['arquivo']}.py", gera_py(al, vetor), executavel=True)
        escreve(f"{pasta}/{al['classe']}.java", gera_java(al, vetor))
        escreve(f"{pasta}/{al['arquivo']}_java.sh", gera_wrapper_java(al), executavel=True)
        print(f"[ok] {pasta}/  ({al['nome']}, {al['complexidade']})")
    print("\nPróximo passo: ./compilar.sh && ./verificar.sh")

if __name__ == "__main__":
    main()
