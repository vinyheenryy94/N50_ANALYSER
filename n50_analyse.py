
#!/usr/bin/env python3

import os
import shutil
import sys

def calcular_n50(fasta_path):
    """Calcula o N50 de um arquivo FASTA."""
    tamanhos = []
    with open(fasta_path, "r") as f:
        seq = ""
        for line in f:
            if line.startswith(">"):
                if seq:
                    tamanhos.append(len(seq))
                seq = ""
            else:
                seq += line.strip()
        if seq:
            tamanhos.append(len(seq))  # Adiciona o último contig

    if not tamanhos:
        return 0  # Arquivo sem contigs

    tamanhos.sort(reverse=True)
    soma_total = sum(tamanhos)
    soma_acumulada = 0

    for tamanho in tamanhos:
        soma_acumulada += tamanho
        if soma_acumulada >= soma_total / 2:
            return tamanho  # Retorna o N50 calculado

    return 0  # Caso não tenha sido possível calcular

def filtrar_genomas(diretorio, destino, limite_n50=20000):
    """Filtra arquivos FASTA cujo N50 seja maior ou igual ao limite e os move para outra pasta."""
    if not os.path.exists(destino):
        os.makedirs(destino)  # Cria a pasta se não existir

    log_path = os.path.join(destino, "N50_log.txt")
    with open(log_path, "w") as log_file:
        log_file.write("Arquivo\tN50\n")  # Cabeçalho do log

        for arquivo in os.listdir(diretorio):
            if arquivo.endswith(".fna"):
                caminho_completo = os.path.join(diretorio, arquivo)
                n50 = calcular_n50(caminho_completo)

                # Escreve no log
                log_file.write(f"{arquivo}\t{n50}\n")

                if n50 >= limite_n50:  # Mantém apenas N50 >= 20 kb
                    shutil.copy(caminho_completo, os.path.join(destino, arquivo))
                    print(f"Arquivo {arquivo} copiado (N50 = {n50})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("É necessário fornecer o caminho da pasta como argumento.")
        sys.exit(1)

    pasta_origem = sys.argv[1]
    pasta_destino = os.path.join(pasta_origem, "N50")  # Nome corrigido da pasta

    filtrar_genomas(pasta_origem, pasta_destino, limite_n50=20000)

