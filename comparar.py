#!/usr/bin/python3
"""
Compara algoritmos usando os .txt gerados pelo benchmark.sh (nao altera o benchmark.sh).

Uso (na raiz do projeto):
    python3 comparar.py resultados_Merge_*/resultado_Merge_*.txt resultados_Gnome_*/resultado_Gnome_*.txt

Gera Comparacao_<A>_vs_<B>_<data>.pdf com:
  pagina 1: uma figura por metrica, barras agrupadas por implementacao
            (C -O0..-Of, Java, Python), uma cor por algoritmo;
  pagina 2: (so com 2 algoritmos) razao B/A para tempo, instrucoes e ciclos.

IMPORTANTE: medir com o mesmo locale usado no benchmark (export LC_ALL=pt_BR.UTF-8),
pois o numero e lido no formato brasileiro (ponto = milhar, virgula = decimal),
exatamente como o benchmark.sh faz.
"""
import datetime
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

NOMES = {
    "ipc": "Instruções por Ciclo (IPC)",
    "task-clock:u": "Tempo de Execução (ms)",
    "page-faults": "Page Faults",
    "cycles": "Ciclos de CPU",
    "instructions": "Instruções Executadas",
    "cache-misses": "Cache Misses (Geral)",
    "branches": "Branches (Total)",
    "branch-misses": "Branch Misses",
    "L1-dcache-loads": "L1 Cache Loads",
    "L1-dcache-load-misses": "L1 Cache Misses",
    "LLC-loads": "LLC Loads",
    "LLC-load-misses": "LLC Misses",
}
ORDEM = ["task-clock:u", "cycles", "instructions", "ipc", "branches", "branch-misses",
         "L1-dcache-loads", "LLC-loads", "L1-dcache-load-misses", "LLC-load-misses",
         "cache-misses", "page-faults"]
CORES = ["#2ca02c", "#d62728", "#1f77b4", "#ff7f0e"]
ORDEM_C = ["O0", "O1", "O2", "O3", "Os", "Of", "Ofast"]
NUCLEOS = ["Total", "P-Core", "E-Core"]


def classifica(rotulo):
    """Converte o rotulo da barra do benchmark.sh em (ordem, nome curto da implementacao)."""
    if rotulo.endswith(".py"):
        return (100, "Python")
    m = re.search(r"[_-](O[0-3sf]|Ofast)$", rotulo)
    if m:
        o = m.group(1)
        return (ORDEM_C.index(o), "C -" + o)
    return (50, "Java")


def numero(txt):
    return float(txt.replace(".", "").replace(",", "."))


def le_arquivo(caminho):
    """Retorna {impl: {metrica: {nucleo: (valor, desvio_abs)}}}."""
    dados = {}
    alvo = None
    atual = None
    for linha in open(caminho, encoding="utf-8", errors="replace"):
        m = re.search(r"^### ALVO_BARRA: (.+) ###", linha)
        if m:
            alvo = m.group(1)
            continue
        m = re.search(r"Performance counter stats for '([^']+)'", linha)
        if m:
            rot = alvo or m.group(1).split("/")[-1]
            alvo = None
            atual = classifica(rot)[1]
            dados.setdefault(atual, {})
            dados[atual].setdefault("_ordem", classifica(rot)[0])
            continue
        if atual is None:
            continue
        m = re.search(r"^\s*([\d\.,]+)(?:\s+(msec))?\s+([a-zA-Z0-9_/\-:]+)"
                      r"(?:.*?\(\s*\+-\s*([\d\.,]+)%\s*\))?", linha)
        if not m:
            continue
        try:
            valor = numero(m.group(1))
        except ValueError:
            continue
        bruto = m.group(3)
        if "cpu_core" in bruto:
            nucleo, base = "P-Core", bruto.replace("cpu_core/", "").strip("/")
        elif "cpu_atom" in bruto:
            nucleo, base = "E-Core", bruto.replace("cpu_atom/", "").strip("/")
        else:
            nucleo, base = "Total", bruto.strip("/")
        if base not in NOMES:
            continue
        desvio = valor * numero(m.group(4)) / 100.0 if m.group(4) else 0.0
        if base == "task-clock:u" and m.group(2) is None:
            valor, desvio = valor / 1e6, desvio / 1e6
        dados[atual].setdefault(base, {})[nucleo] = (valor, desvio)

    # IPC = instrucoes / ciclos
    for impl, mets in dados.items():
        for n in NUCLEOS:
            if n in mets.get("instructions", {}) and n in mets.get("cycles", {}):
                i, di = mets["instructions"][n]
                c, dc = mets["cycles"][n]
                if c > 0:
                    ipc = i / c
                    mets.setdefault("ipc", {})[n] = (ipc, ipc * ((di / i if i else 0) + (dc / c)))
    return dados


def pega(dados_impl, metrica):
    """Escolhe o primeiro nucleo disponivel (Total > P-Core > E-Core)."""
    for n in NUCLEOS:
        if n in dados_impl.get(metrica, {}):
            return dados_impl[metrica][n]
    return None


def fmt(v, metrica):
    if metrica in ("ipc", "task-clock:u"):
        return f"{v:.2f}"
    if v >= 1e9:
        return f"{v / 1e9:.2f}G"
    if v >= 1e6:
        return f"{v / 1e6:.2f}M"
    if v >= 1e4:
        return f"{v / 1e3:.1f}k"
    return f"{v:,.0f}"


def main():
    arquivos = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(arquivos) < 2:
        sys.exit(__doc__)

    # Um arquivo por algoritmo: se houver varios (medicoes antigas), usa o mais recente
    # (o nome do arquivo termina com a data, entao a ordenacao alfabetica serve).
    def nome_alg(arq):
        partes = os.path.basename(arq).split("_")
        return partes[1].capitalize() if len(partes) > 1 else os.path.basename(arq)

    ordem_args = []                      # ordem em que os algoritmos foram passados
    for arq in arquivos:
        if nome_alg(arq) not in ordem_args:
            ordem_args.append(nome_alg(arq))
    por_nome = {}
    for arq in sorted(arquivos, key=os.path.basename):
        partes = os.path.basename(arq).split("_")
        nome = partes[1].capitalize() if len(partes) > 1 else os.path.basename(arq)
        if nome in por_nome:
            print(f"[AVISO] mais de um arquivo de {nome}: ignorando {por_nome[nome]}\n"
                  f"        usando o mais recente: {arq}")
        por_nome[nome] = arq

    algs = []   # [(nome, dados)]
    esperado = {"C -O0", "C -O1", "C -O2", "C -O3", "C -Os", "C -Of", "Java", "Python"}
    for nome in ordem_args:
        arq = por_nome[nome]
        d = le_arquivo(arq)
        if not d:
            sys.exit(f"[ERRO] nenhum dado lido de {arq}")
        algs.append((nome, d))
        print(f"[ok] {nome}: {len(d)} implementações ({', '.join(sorted(d, key=lambda k: d[k]['_ordem']))})")
        faltam = esperado - set(d)
        if faltam:
            print(f"[AVISO] {nome}: faltam {', '.join(sorted(faltam))} "
                  f"(os executáveis existiam e estavam compilados na hora da medição?)")
    if len(algs) < 2:
        sys.exit("[ERRO] preciso de arquivos de pelo menos 2 algoritmos diferentes.")

    impls = {}
    for _, d in algs:
        for k, v in d.items():
            impls[k] = v["_ordem"]
    impls = sorted(impls, key=lambda k: impls[k])

    metricas = [m for m in ORDEM if any(m in d[i] for _, d in algs for i in d)]
    cols = 2
    rows = (len(metricas) + 1) // 2
    nomes = " vs ".join(n for n, _ in algs)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    saida = f"Comparacao_{'_vs_'.join(n for n, _ in algs)}_{ts}.pdf"

    with PdfPages(saida) as pdf:
        # ---- pagina 1: grade de metricas ----
        fig, axs = plt.subplots(rows, cols, figsize=(8 * cols, 5 * rows))
        fig.suptitle(f"Comparação: {nomes} (média e SD)", fontsize=20, fontweight="bold")
        axs = axs.flatten() if len(metricas) > 1 else [axs]
        n_alg = len(algs)
        larg = 0.8 / n_alg
        for ax, met in zip(axs, metricas):
            maximo, minimo = 1, None
            for ai, (nome, d) in enumerate(algs):
                xs, vs, es = [], [], []
                for xi, impl in enumerate(impls):
                    r = pega(d.get(impl, {}), met)
                    if r is None or r[0] <= 0:
                        continue
                    xs.append(xi + (ai - (n_alg - 1) / 2) * larg)
                    vs.append(r[0]); es.append(r[1])
                if not vs:
                    continue
                ax.bar(xs, vs, larg, yerr=es, capsize=3, color=CORES[ai % len(CORES)],
                       edgecolor="black", alpha=0.85, ecolor="red", label=nome)
                maximo = max(maximo, max(v + e for v, e in zip(vs, es)))
                minimo = min(vs) if minimo is None else min(minimo, min(vs))
                for x, v, e in zip(xs, vs, es):
                    y = (v + e) * (1.35 if met != "ipc" else 1.0) + (0 if met != "ipc" else 0.02)
                    ax.text(x, y, fmt(v, met), ha="center", va="bottom", fontsize=7,
                            fontweight="bold", rotation=60)
            if met != "ipc" and minimo:
                ax.set_yscale("log")
                ax.set_ylim(minimo * 0.3, maximo * 25)
            else:
                ax.set_ylim(0, maximo * 1.3)
            ax.set_title(NOMES[met], fontsize=13, pad=12)
            ax.set_xticks(range(len(impls)))
            ax.set_xticklabels(impls, rotation=25, ha="right", fontsize=9)
            ax.grid(axis="y", linestyle="--", alpha=0.6)
            ax.legend(fontsize=9, loc="upper right")
        for ax in axs[len(metricas):]:
            ax.axis("off")
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        METS3 = [m for m in ("task-clock:u", "instructions", "cycles") if m in metricas]

        def barras_razao(ax, titulo, xs_labels, series, linha1=True):
            """series: [(nome, cor, [valores ou None])] alinhados com xs_labels."""
            n = len(series)
            larg = 0.8 / n
            todos = []
            for si, (nome, cor, vals) in enumerate(series):
                xs = [i + (si - (n - 1) / 2) * larg for i, v in enumerate(vals) if v]
                vs = [v for v in vals if v]
                if not vs:
                    continue
                ax.bar(xs, vs, larg, color=cor, edgecolor="black", alpha=0.85, label=nome)
                for x, v in zip(xs, vs):
                    ax.text(x, v * 1.12, f"{v:.2f}x" if v < 10 else f"{v:.1f}x", ha="center",
                            va="bottom", fontsize=8, fontweight="bold", rotation=0 if n == 1 else 60)
                todos += vs
            if linha1:
                ax.axhline(1, color="black", linewidth=1)
            ax.set_yscale("log")
            if todos:
                ax.set_ylim(min(min(todos), 1) * 0.5, max(max(todos), 1) * 8)
            ax.set_title(titulo, fontsize=12, pad=10)
            ax.set_xticks(range(len(xs_labels)))
            ax.set_xticklabels(xs_labels, rotation=25, ha="right", fontsize=9)
            ax.grid(axis="y", linestyle="--", alpha=0.6)
            if n > 1:
                ax.legend(fontsize=9, loc="upper right")

        # ---- pagina 2: razao B/A em TODAS as metricas (so com 2 algoritmos) ----
        if n_alg == 2:
            (na, da), (nb, db) = algs
            ordem_r = METS3 + [m for m in metricas if m not in METS3]
            rows_r = (len(ordem_r) + 1) // 2
            fig, axs = plt.subplots(rows_r, 2, figsize=(16, 4.6 * rows_r), squeeze=False)
            fig.suptitle(f"Razão {nb} / {na} em cada métrica (>1: {nb} maior; <1: {nb} menor)",
                         fontsize=17, fontweight="bold")
            axs = axs.flatten()
            for ax, met in zip(axs, ordem_r):
                vals = []
                for impl in impls:
                    a, b = pega(da.get(impl, {}), met), pega(db.get(impl, {}), met)
                    vals.append(b[0] / a[0] if a and b and a[0] > 0 and b[0] > 0 else None)
                barras_razao(ax, f"{NOMES[met]}: {nb}/{na}", impls, [("", "#9467bd", vals)])
            for ax in axs[len(ordem_r):]:
                ax.axis("off")
            fig.tight_layout()
            fig.subplots_adjust(top=0.94)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

        # ---- pagina 3: efeito das otimizacoes do gcc (ganho em relacao ao -O0) ----
        c_impls = [i for i in impls if i.startswith("C -") and i != "C -O0"]
        if "C -O0" in impls and c_impls and METS3:
            fig, axs = plt.subplots(1, len(METS3), figsize=(7 * len(METS3), 5.5), squeeze=False)
            fig.suptitle("Ganho de cada otimização em relação ao -O0 (>1: melhor que -O0, <1: pior)",
                         fontsize=16, fontweight="bold")
            for ax, met in zip(axs[0], METS3):
                series = []
                for ai, (nome, d) in enumerate(algs):
                    base = pega(d.get("C -O0", {}), met)
                    vals = []
                    for i in c_impls:
                        r = pega(d.get(i, {}), met)
                        vals.append(base[0] / r[0] if base and r and r[0] > 0 and base[0] > 0 else None)
                    series.append((nome, CORES[ai % len(CORES)], vals))
                barras_razao(ax, f"{NOMES[met]}: -O0 / otimizado", c_impls, series)
            fig.tight_layout()
            fig.subplots_adjust(top=0.86)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

        # ---- pagina 4: Java e Python em relacao ao melhor C ----
        outras = [i for i in impls if not i.startswith("C -")]
        cs = [i for i in impls if i.startswith("C -")]
        if outras and cs and METS3:
            fig, axs = plt.subplots(1, len(METS3), figsize=(7 * len(METS3), 5.5), squeeze=False)
            fig.suptitle("Java e Python em relação ao melhor nível de C (quantas vezes maior)",
                         fontsize=16, fontweight="bold")
            for ax, met in zip(axs[0], METS3):
                series = []
                for ai, (nome, d) in enumerate(algs):
                    cvals = [pega(d.get(i, {}), met) for i in cs]
                    cvals = [v[0] for v in cvals if v and v[0] > 0]
                    melhor = min(cvals) if cvals else None
                    vals = []
                    for i in outras:
                        r = pega(d.get(i, {}), met)
                        vals.append(r[0] / melhor if melhor and r and r[0] > 0 else None)
                    series.append((nome, CORES[ai % len(CORES)], vals))
                barras_razao(ax, f"{NOMES[met]}: linguagem / melhor C", outras, series)
            fig.tight_layout()
            fig.subplots_adjust(top=0.86)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

    # ---- CSV com todos os valores (para montar tabelas do relatorio) ----
    csv_nome = saida.replace(".pdf", "_dados.csv")
    with open(csv_nome, "w", encoding="utf-8") as f:
        f.write("algoritmo;implementacao;metrica;nucleo;valor;desvio_abs\n")
        for nome, d in algs:
            for impl in impls:
                for met in metricas:
                    for n in NUCLEOS:
                        if n in d.get(impl, {}).get(met, {}):
                            v, e = d[impl][met][n]
                            f.write(f"{nome};{impl};{NOMES[met]};{n};{v:.6g};{e:.6g}\n".replace(".", ","))
    print(f"[OK] CSV gerado: {csv_nome}")
    print(f"[OK] PDF gerado: {saida}")


if __name__ == "__main__":
    main()
