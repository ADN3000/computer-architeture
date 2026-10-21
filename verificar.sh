#!/bin/bash
# Confere se TODAS as versões (C -O0..-Ofast, Python, Java) ordenam corretamente
# e produzem o mesmo resultado. Não faz parte da medição de desempenho.
cd "$(dirname "$0")" || exit 1

ESPERADO=$(python3 -c "
v = sorted(int(x) for x in open('vetor_6800.txt').read().split())
print(sum(x * (i + 1) for i, x in enumerate(v)))")
echo "Checksum esperado (vetor ordenado): $ESPERADO"
echo

FALHAS=0
for dir in */; do
    d=${dir%/}
    ls "$d"/*.c >/dev/null 2>&1 || continue
    echo "=== $d ==="
    for app in "$d"/*; do
        [ -f "$app" ] && [ -x "$app" ] || continue
        nome=$(basename "$app")
        saida=$( ( cd "$d" && ./"$nome" --verificar ) 2>&1 )
        if [ "$saida" == "ORDENADO soma=$ESPERADO" ]; then
            printf "  [OK]   %-26s %s\n" "$nome" "$saida"
        else
            printf "  [ERRO] %-26s %s\n" "$nome" "$saida"
            FALHAS=$((FALHAS + 1))
        fi
    done
done
echo
[ "$FALHAS" -eq 0 ] && echo "Tudo certo: todas as versões ordenam o mesmo vetor corretamente." \
                    || echo "ATENÇÃO: $FALHAS versão(ões) com problema."
exit $FALHAS
