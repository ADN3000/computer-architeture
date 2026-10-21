#!/bin/bash
# Compila tudo: C em 6 níveis de otimização + Java, e dá permissão +x aos scripts.
# Rode na raiz do projeto (onde está o benchmark.sh).
cd "$(dirname "$0")" || exit 1

# Uso: ./compilar.sh            -> gera os 6 níveis (O0 O1 O2 O3 Os Ofast)
#      ./compilar.sh Ofast      -> gera só o(s) nível(is) informado(s)
# No gcc, o "-Of" do enunciado é o -Ofast: compila com -Ofast, mas o executável
# se chama *_Of, para o gráfico do benchmark.sh mostrar "-Of".
if [ "$#" -gt 0 ]; then OTIMIZACOES=("$@"); else OTIMIZACOES=(O0 O1 O2 O3 Os Ofast); fi

for dir in */; do
    d=${dir%/}
    ls "$d"/*.c >/dev/null 2>&1 || continue
    echo "=== $d ==="
    ( cd "$d" || exit 1

      for src in *.c; do
          base=${src%.c}
          rm -f "${base}"_O*      # remove executáveis antigos de outros níveis
          for o in "${OTIMIZACOES[@]}"; do
              sufixo=$o
              [ "$o" == "Ofast" ] && sufixo=Of    # barra do gráfico aparece como "-Of"
              rm -f "${base}_${sufixo}"
              gcc "-$o" -o "${base}_${sufixo}" "$src" || exit 1
              echo "  gcc -$o  ->  ${base}_${sufixo}"
          done
      done

      rm -f ./*.class
      javac ./*.java || exit 1
      echo "  javac    ->  $(ls ./*.class | tr '\n' ' ')"

      chmod +x ./*.py ./*_java.sh
    ) || { echo "[ERRO] falha ao compilar $d"; exit 1; }
done
echo
echo "Compilação concluída. Rode ./verificar.sh para conferir os resultados."
