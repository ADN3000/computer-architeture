import random
from pathlib import Path

QUANTIDADE = 6800
SEMENTE = 42

# Gera uma única sequência reproduzível.
random.seed(SEMENTE)

valores = [
    random.randint(0, 99999)
    for _ in range(QUANTIDADE)
]

assert len(valores) == QUANTIDADE

# Diretório raiz do projeto.
raiz = Path(__file__).resolve().parent.parent

# Representação dos valores como literais inteiros.
lista_c = ",\n    ".join(map(str, valores))
lista_python = ",\n    ".join(map(str, valores))
lista_java = ",\n        ".join(map(str, valores))

# 1. C: vetor global com inicialização no código-fonte.
arquivo_c = raiz / "src/c/vetor_dados.h"
arquivo_c.write_text(
    "#ifndef VETOR_DADOS_H\n"
    "#define VETOR_DADOS_H\n\n"
    "#define QUANTIDADE 6800\n\n"
    "int vetor[QUANTIDADE] = {\n    "
    + lista_c
    + "\n};\n\n"
    "#endif\n",
    encoding="utf-8"
)

# 2. Python: sequência fixa declarada no módulo.
arquivo_python = raiz / "src/python/vetor_dados.py"
arquivo_python.write_text(
    "QUANTIDADE = 6800\n\n"
    "VETOR = [\n    "
    + lista_python
    + "\n]\n",
    encoding="utf-8"
)

# 3. Java: vetor declarado no escopo da classe.
arquivo_java = raiz / "src/java/VetorDados.java"
arquivo_java.write_text(
    "public class VetorDados {\n"
    "    public static final int QUANTIDADE = 6800;\n\n"
    "    public static final int[] VALORES = {\n        "
    + lista_java
    + "\n    };\n"
    "}\n",
    encoding="utf-8"
)

print("Arquivos gerados com sucesso.")
print(f"Quantidade de elementos: {len(valores)}")
print(f"Semente utilizada: {SEMENTE}")
print(f"Primeiros 10 elementos: {valores[:10]}")
print(f"Últimos 10 elementos: {valores[-10:]}")
print()
print("Arquivos criados:")
print(arquivo_c)
print(arquivo_python)
print(arquivo_java)

