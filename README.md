# Comparative Performance Analysis of Sorting Algorithms

**Computer Architecture Practical Project — Federal University of Mato Grosso do Sul (UFMS)**

This repository contains the source code, scripts, experimental input data, and selected results used in a comparative performance study of **Merge Sort** and **Gnome Sort** implemented in **C, Python 3, and Java**.

The experiment uses a fixed input vector containing 6,800 elements. The implementations are prepared to use the same input data so that their measured performance can be compared under the same workload.

## Algorithms

| Algorithm | Time complexity |
|---|---:|
| Merge Sort | O(n log n) |
| Gnome Sort | O(n²) |

The C implementations are compiled with multiple GCC optimization levels. Python and Java implementations are also included for cross-language comparison.

## Repository contents

```text
.
├── benchmark.sh                 # Benchmarking script
├── gerar_projeto.py             # Generates algorithm source files
├── vetor_6800.txt               # Fixed input vector (6,800 elements)
├── compilar.sh                  # Compiles C and Java implementations
├── verificar.sh                 # Checks sorting correctness
├── preparar_ubuntu_live.sh      # Installs the experimental dependencies
├── comparar.py                  # Generates a comparison report from result files
├── ambiente_pesquisa.txt        # Experimental environment information
├── Merge/                       # Merge Sort implementations
├── Gnome/                       # Gnome Sort implementations
├── resultados_Merge_*/          # Stored Merge Sort results
├── resultados_Gnome_*/          # Stored Gnome Sort results
├── Comparacao_Merge_vs_Gnome_*.pdf
└── Comparacao_Merge_vs_Gnome_*_dados.csv
```

The result directories and comparison files in the repository are examples of the experiment outputs retained in this project. New runs generate timestamped result directories.

## Experimental environment

The scripts are intended to run in an Ubuntu environment with the required development and performance-analysis tools.

The setup script installs or requests the following dependencies:

- GCC and standard build tools
- Java Development Kit (JDK)
- Python 3
- Matplotlib
- Linux `perf` tools compatible with the running kernel

The script prints the installed tool and operating-system versions. Record these versions, along with the hardware information, when documenting a new experiment.

Useful hardware-inspection commands:

```bash
lscpu
free -h
lsblk -d
```

## Requirements

- Ubuntu (physical machine recommended for hardware performance-counter measurements)
- Bash
- GCC
- Java compiler and runtime (`javac` and `java`)
- Python 3
- Python Matplotlib
- Linux `perf`
- `taskset` (for CPU affinity, when required)

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/ADN3000/computer-architeture.git
cd computer-architeture
```

On an Ubuntu Live session, install the dependencies:

```bash
./preparar_ubuntu_live.sh
```

**Ubuntu Live note:** the installed environment may be temporary. Save the project and generated results to persistent storage before shutting down. The setup script may need to be run again after a reboot.

## Compile and validate

Compile the C implementations using the optimization levels configured in the project, compile the Java implementations, and set the required executable permissions:

```bash
./compilar.sh
```

Run the correctness checks:

```bash
./verificar.sh
```

The verification script checks whether the implementations produce the expected sorted output. Complete the validation before collecting benchmark measurements.

The default C compilation levels are:

- `-O0`
- `-O1`
- `-O2`
- `-O3`
- `-Os`
- `-Ofast`

**Optimization-label note:** the project maps GCC's `-Ofast` build to an executable suffix named `_Of`, so the benchmark output uses the label `-Of`. This is a project naming convention; the compiler flag actually used is `-Ofast`.

To compile only a selected optimization level, pass it to the script. For example:

```bash
./compilar.sh Ofast
```

## Run the benchmarks

Run the benchmark for each algorithm:

```bash
./benchmark.sh --all Merge
./benchmark.sh --all Gnome
```

The default number of repetitions is 10. To request 30 repetitions:

```bash
./benchmark.sh --all --r 30 Merge
./benchmark.sh --all --r 30 Gnome
```

On systems with hybrid Performance and Efficiency cores, CPU affinity can be used to constrain execution to a selected logical CPU. The following commands reproduce the CPU-affinity example used in the project's current instructions:

```bash
taskset --cpu-list 1 ./benchmark.sh --all Merge
taskset --cpu-list 1 ./benchmark.sh --all Gnome
```

Use the same CPU-affinity policy for both algorithms and report the logical CPU actually selected in the experimental description. Do not assume that CPU 1 is the correct choice on every machine.

The benchmark script collects the performance events supported by the system and generates text result files and PDF plots. Available hardware-counter events depend on the processor, kernel, permissions, and `perf` support. Events that are unavailable or unsupported should be reported as such rather than interpreted as measured values.

## Compare the results

After running both algorithms, generate the comparison report:

```bash
export LC_ALL=pt_BR.UTF-8
python3 comparar.py \
  resultados_Merge_*/resultado_Merge_*.txt \
  resultados_Gnome_*/resultado_Gnome_*.txt
```

The script generates a PDF comparison report with side-by-side bars for the implementations and the Gnome Sort/Merge Sort ratio. It also produces a CSV data file.

The locale shown above matches the setting in the project's original execution instructions. Use a consistent locale when processing and comparing result files.

## Additional notes

- The `benchmark.sh` script executes files with executable permission in the algorithm directories. Source files (`.c` and `.java`) are not intended to be executed directly; the Python scripts and Java wrapper scripts receive executable permission as part of compilation setup.
- Directory names used as benchmark targets must not contain underscores.
- The `--verificar` argument is used by `verificar.sh` for correctness checking and is not part of the benchmark measurement.
- Measurements collected inside a virtual machine may not expose hardware performance counters such as CPU cycles, instructions, or cache events reliably. A physical machine is recommended for those measurements.
- Keep the generated result files, the input vector, and the environment information together so that the experimental run can be inspected later.
- The repository includes a script capable of generating other sorting-algorithm projects. List the available algorithms with `python3 gerar_projeto.py --lista`. For example, `python3 gerar_projeto.py quick insertion` generates the selected projects; remove previous generated algorithm directories first if necessary.

## Reproducibility

For a reproducible report, preserve and identify:

1. The exact repository revision used for the experiment.
2. The input vector (`vetor_6800.txt`).
3. The operating-system and kernel versions.
4. The CPU model and relevant hardware details.
5. GCC, Java, Python, Matplotlib, and `perf` versions.
6. The compiler optimization flags.
7. The number of benchmark repetitions and CPU-affinity settings.
8. The raw benchmark output files and generated analysis files.

The repository's `ambiente_pesquisa.txt` file provides additional environment information. Check that it corresponds to the same experimental run before citing it as the environment for a particular set of results.

## Citation

If you use this repository in academic work, cite the repository and identify the exact revision or release used. The repository URL is:

```text
https://github.com/ADN3000/computer-architeture
```

For a formal, versioned software citation, a release and a `CITATION.cff` file should be added once the author list and citation metadata have been confirmed.

## License

No license file is currently provided in this repository. Until a license is added, do not assume that the source code is available for unrestricted reuse or redistribution.
