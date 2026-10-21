# Trabalho Prático – Arquitetura de Computadores (UFMS)
Algoritmos do grupo: **Merge Sort** O(n log n) e **Gnome Sort** O(n²)

## Estrutura
```
trabalho_ac/
├── benchmark.sh              # script do professor (inalterado)
├── gerar_projeto.py          # gera os fontes C/Python/Java com o MESMO vetor
├── vetor_6800.txt            # o vetor (fixo; reaproveitado sempre)
├── compilar.sh               # gcc -O0 -O1 -O2 -O3 -Os -Ofast + javac + chmod +x
├── verificar.sh              # confere que todas as versões ordenam igual
├── preparar_ubuntu_live.sh   # instala perf, gcc, JDK, matplotlib
├── Merge/
│   ├── mergesort.c           -> executáveis mergesort_O0 ... _Of
│   ├── mergesort.py          -> script com shebang (+x)
│   ├── MergeSort.java        -> MergeSort.class
│   └── mergesort_java.sh     -> wrapper: "java MergeSort"
└── Gnome/                    # idem (gnomesort.*, GnomeSort.java)
```

## Passo a passo
```bash
# 1) (Ubuntu live) instalar dependências – refazer a cada boot do live!
./preparar_ubuntu_live.sh

# 2) Compilar e verificar (tudo deve sair [OK])
./compilar.sh            # 6 níveis de otimização (o que o enunciado pede)
# ./compilar.sh Ofast    # alternativa: só o -Ofast em C
./verificar.sh

# 3) Medir (uma vez por algoritmo). Em CPU híbrida (P/E-cores), fixe um núcleo:
taskset --cpu-list 1 ./benchmark.sh --all Merge
taskset --cpu-list 1 ./benchmark.sh --all Gnome
#   opcional: --r 30  (mais repetições; o padrão é 10)
```
Resultados (.txt e gráficos .pdf) ficam em `resultados_<Algoritmo>_<data>/`.

## Comparar os dois algoritmos (depois de medir os dois)
```bash
export LC_ALL=pt_BR.UTF-8      # mesmo locale usado na medição
python3 comparar.py resultados_Merge_*/resultado_Merge_*.txt resultados_Gnome_*/resultado_Gnome_*.txt
```
Gera `Comparacao_Merge_vs_Gnome_<data>.pdf` (barras lado a lado por implementação + razão Gnome/Merge).

Para trocar de algoritmo: `python3 gerar_projeto.py --lista` e depois, por exemplo,
`python3 gerar_projeto.py quick insertion` (apague as pastas antigas).

## Observações importantes
- **-Of do enunciado = `-Ofast` no gcc**: compila-se com `-Ofast`, mas o executável se chama
  `*_Of`, então o gráfico mostra `-Of`.
- O `benchmark.sh` roda tudo que tem permissão +x na pasta; fontes `.c/.java` ficam sem +x.
  O `.py` e o wrapper `.sh` têm +x de propósito.
- Nomes de pasta não podem ter `_`.
- O argumento `--verificar` (usado só pelo `verificar.sh`) checa o resultado
  **depois** da ordenação e não é usado no benchmark.
- **Ubuntu live**: nada é salvo ao desligar. Copie projeto e resultados para um pendrive.
- **Máquina virtual**: `cycles`/`instructions`/cache normalmente não funcionam no `perf`.
- Para o relatório, anote as versões que o `preparar_ubuntu_live.sh` imprime e o hardware
  (`lscpu`, `free -h`, `lsblk -d`).
