import os
import sys
from pathlib import Path
import torch

# --- 1. CONFIGURAÇÃO DE PASTAS ---
pasta_raiz = Path(__file__).parent.resolve()
pasta_modelos = pasta_raiz / "modelos"
pasta_clientes = pasta_raiz / "clientes"
pasta_resultados = pasta_raiz / "resultados"

for p in [pasta_modelos, pasta_clientes, pasta_resultados]:
    p.mkdir(parents=True, exist_ok=True)

os.environ["TTS_HOME"] = str(pasta_modelos)

# --- 2. IMPORTAÇÃO E CARREGAMENTO ---
try:
    from TTS.api import TTS
except ImportError:
    print("\033[91mErro: A biblioteca TTS não está instalada. Use: pip install TTS\033[0m")
    sys.exit()

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"\n--- [LOG] Iniciando Sistema de Clonagem ---")
print(f"--- [LOG] Usando: {device.upper()} ---")

# Carregamento do modelo
# Nota: A primeira vez pode demorar pois ele baixa cerca de 2GB
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# --- 3. INTERAÇÃO COM O USUÁRIO ---
print("\n" + "="*30)
print(" MENU DE CLONAGEM DE VOZ ")
print("="*30)

arquivos_voz = [f for f in os.listdir(pasta_clientes) if f.lower().endswith(('.wav', '.mp3', '.flac'))]

if arquivos_voz:
    print(f"Vozes disponíveis na pasta 'clientes':")
    for idx, voz in enumerate(arquivos_voz):
        print(f"[{idx}] {voz}")
else:
    print("\033[93mAVISO: A pasta 'clientes' está vazia! Coloque um arquivo de voz lá.\033[0m")
    sys.exit()

escolha = input("\nDigite o nome do arquivo ou o número: ").strip()

# Lógica para aceitar número ou nome
if escolha.isdigit() and int(escolha) < len(arquivos_voz):
    nome_arquivo = arquivos_voz[int(escolha)]
else:
    nome_arquivo = escolha if escolha.lower().endswith('.wav') else escolha + ".wav"

texto_roteiro = input("Cole o roteiro que a voz deve falar: ").strip()

caminho_voz_exemplo = pasta_clientes / nome_arquivo
# Nome do arquivo de saída limpo
caminho_saida = pasta_resultados / f"voz_clonada_{Path(nome_arquivo).stem}.wav"

# --- 4. EXECUÇÃO DA MÁGICA ---
if caminho_voz_exemplo.exists():
    try:
        print(f"\n[AGUARDE] Clonando a voz de {nome_arquivo}...")
        
        # O XTTS v2 faz a clonagem aqui
        tts.tts_to_file(
            text=texto_roteiro,
            speaker_wav=str(caminho_voz_exemplo),
            language="pt",
            file_path=str(caminho_saida)
        )
        
        print(f"\n✅ SUCESSO! Áudio salvo em: {caminho_saida}")
        print(f"💡 DICA: Agora use este arquivo no seu script do Wav2Lip.")
        
    except Exception as e:
        print(f"\n❌ ERRO ao gerar o áudio: {e}")
else:
    print(f"\n❌ ERRO: O arquivo '{caminho_voz_exemplo}' não foi encontrado.")