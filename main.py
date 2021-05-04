from argparse import ArgumentParser
from os import path
from exportador.CriadorDeSessoes import criaListaSessoes, exportaParaArquivos, exportaParaArquivoSSH

if __name__ == '__main__':
    argParser = ArgumentParser(description='Exporta o registro com sessões do Putty e exporta para outro formato')
    argParser.add_argument("-f", "--file", required=True, help="Arquivo texto exportado")
    argParser.add_argument("-d", "--target", required=True, help="Onde serão salvos o(s) arquivo(s) de sessão(ôes)")
    argParser.add_argument("-k", "--keys", required=True, help="Diretório onde se encontram as chaves criptográficas")
    argParser.add_argument("-s", "--ssh", action='store_true', required=False, help="Exportar para formato a ser usado com cliente SSH")
    opt = argParser.parse_args()


    if path.exists(opt.file):
        s = criaListaSessoes(opt.file)

        if opt.ssh:
            exportaParaArquivoSSH(s, opt.keys)
            exit(0)

        if path.exists(opt.keys):
            exportaParaArquivos(s, opt.target, opt.keys)
        else:
            print(f'Diretório {opt.keys} não existe. Saindo...')
    else:
        print(f'O arquivo {opt.file} não existe. Nada a ser feito! Saindo...')
