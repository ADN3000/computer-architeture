# Computer Architecture — Sorting Algorithms

Projeto prático de Arquitetura de Computadores para comparar algoritmos de ordenação em diferentes linguagens e configurações de compilação.

## Objetivo

Comparar **Gnome Sort** e **Merge Sort** observando tempo de execução, instruções executadas, ciclos de CPU, IPC e eventos de cache/branch disponibilizados pelo Linux `perf`.

- **Gnome Sort:** complexidade de tempo quadrática, `O(n^2)`.
- **Merge Sort:** complexidade de tempo `O(n log n)` e memória auxiliar `O(n)`.

As implementações atuais estão em C, Python 3 e Java. O vetor utilizado possui **6.800 inteiros** e é armazenado nos arquivos de dados de cada linguagem para manter a mesma entrada entre as execuções.

## Estrutura principal

```text
Arquitetura/
├── src/
│   ├── c/                 # Implementações C e vetor de dados
│   ├── python/            # Implementações Python e vetor de dados
│   └── java/              # Implementações Java e vetor de dados
├── scripts/
│   └── gerar_vetor.py     # Gera o vetor determinístico nas três linguagens
├── benchmark.sh           # Script de benchmark
├── benchmark_local.sh     # Variante local do script de benchmark
└── ambiente_experimental.txt
```

O diretório `entrega/` contém materiais preparados para entrega, enquanto as pastas de resultados registram execuções anteriores.

## Requisitos

Conforme a etapa que será executada:

- Linux;
- GCC para compilar C;
- Python 3;
- Java JDK (`javac` e `java`);
- `perf` do Linux e permissão para coletar contadores de hardware;
- `matplotlib` no Python para gerar os gráficos.

Em Ubuntu/Debian, o Matplotlib pode ser instalado com `python3 -m pip install matplotlib`, conforme as políticas do sistema. Se a distribuição bloquear instalações no Python do sistema, use um ambiente virtual.

## Compilar e executar as implementações

Execute os comandos a partir da pasta `Arquitetura`.

### C

```bash
mkdir -p build/c
gcc -std=c11 -Wall -Wextra -O0 src/c/gnome.c -o build/c/gnome_O0
gcc -std=c11 -Wall -Wextra -O0 src/c/merge.c -o build/c/merge_O0

./build/c/gnome_O0
./build/c/merge_O0
```

Para comparar otimizações, compile cada algoritmo separadamente para cada nível exigido pelo experimento e identifique os executáveis pelo nível usado.

### Python 3

```bash
cd src/python
python3 gnome.py
python3 merge.py
cd ../..
```

### Java

```bash
mkdir -p build/java
javac -d build/java src/java/VetorDados.java src/java/GnomeSort.java src/java/MergeSort.java
java -cp build/java GnomeSort
java -cp build/java MergeSort
```

As versões atuais ordenam o vetor em memória e não imprimem os elementos, para evitar que a saída de texto interfira nas medições. Faça a validação de correção separadamente do caminho cronometrado.

## Executar o benchmark

Consulte as opções disponíveis antes de iniciar:

```bash
./benchmark_local.sh --help
```

O script espera diretórios-alvo contendo executáveis ou scripts executáveis. Execute-o a partir do diretório que contém esses alvos, passando os nomes das pastas como argumentos ou usando o modo sem argumentos para processar as pastas daquele diretório. Exemplo genérico:

```bash
/path/para/Arquitetura/benchmark_local.sh --all --run 10 pasta_alvo_1 pasta_alvo_2
```

Use caminhos válidos a partir do diretório corrente. Para limitar a execução a um processador lógico, o comando pode ser prefixado com `taskset`, por exemplo `taskset -c 0 ...`. Registre o processador lógico escolhido e o ambiente experimental, especialmente ao comparar máquinas diferentes.

Os contadores disponíveis variam conforme o processador, o kernel e a configuração do `perf`. Eventos indisponíveis devem ser registrados como indisponíveis, não tratados como zero.

## Vetor de dados

O script `scripts/gerar_vetor.py` recria os arquivos de dados a partir de uma semente fixa. Se o vetor for regenerado, gere os dados uma única vez e confira se a sequência é idêntica nas três linguagens antes de realizar novas medições.

## Observações sobre otimizações

Os níveis `-O0`, `-O1`, `-O2`, `-O3` e `-Os` são opções conhecidas do GCC. A opção `-Of` não é aceita pelo GCC utilizado no ambiente registrado neste projeto; `-Ofast` e `-Oz` são opções diferentes e **não devem ser apresentados como equivalentes a `-Of`**. Se forem usados como experimentos alternativos, identifique-os explicitamente na coleta e na análise.

## Reprodutibilidade

Antes de comparar resultados, registre pelo menos o modelo de CPU, sistema operacional/kernel, versões de GCC/Python/Java, opções de compilação, número de repetições, processador lógico usado e eventos efetivamente coletados. Não misture dados de execuções com configurações diferentes sem identificá-las.
