#!/bin/bash
# Instala as dependências no Ubuntu em modo live (nada é salvo após reiniciar!).
set -e
sudo add-apt-repository -y universe >/dev/null 2>&1 || true
sudo apt update
sudo apt install -y build-essential default-jdk-headless python3 python3-matplotlib linux-tools-common

# perf precisa ser compatível com o kernel em execução
if ! sudo apt install -y "linux-tools-$(uname -r)"; then
    echo "[aviso] linux-tools-$(uname -r) indisponível; tentando linux-tools-generic"
    sudo apt install -y linux-tools-generic
fi

echo
echo "=== Versões instaladas (anote para o relatório) ==="
gcc --version | head -1
javac -version
java -version 2>&1 | head -1
python3 --version
perf --version || echo "[ERRO] perf não está funcionando com este kernel"
lsb_release -d 2>/dev/null || cat /etc/os-release | head -2
