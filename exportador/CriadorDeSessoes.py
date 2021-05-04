from typing import List
import os
from os import path, makedirs
from urllib.parse import unquote, quote

class Sessao:
    """"
    Classe para armazenar os dados da sessão.
    Desta forma facilita a obtenção dos dados específicos da sessão putty.

    Atributos:
        nome: contém o nome (string) obtido do nome fornecido quando é salva a sessão no
            programa Putty no Windows.
        campo: é um dicionário python para armazenar o campo de dados da sessão.
            cada chave do dicionário contém o nome do campo obtido do arquivo de registro
            referente à sessão lida.
    """
    def __init__(self, nome=''):
        self.nome = nome
        self.campo = {}

    def __str__(self):
        return str(self.campo)


def criaListaSessoes(arq=''):
    """
    Cria uma lista de instâncias da classe Sessao, onde cada instância armazena os dados
    da sessão lida.

    :param arq: nome do arquivo exportado do registro do windows. É esperado que o formato
        codificado do conteúdo do arquivo seja 'utf-10-le' (como é feito pelo comando reg
        no windows).
    :return: uma lista de instâncias da class Sessao, cada uma contendo dados da sessão lida
    """
    sessoes: List[Sessao] = list()
    nomeSess = ''
    chave = ''
    valor = ''
    isSess = False
    count = 0

    f = open(arq, 'rt', encoding='utf-16-le')
    line = f.readline()
    while line:
        count += 1
        # print('line#:', count, sep='')
        try:
            campos = line.strip().split('\\SimonTatham\\PuTTY\\Sessions\\')
            # print('campos#: {}; lineSize: {}'.format(len(campos), len(line)), sep='')
            if len(line) == 1:
                isSess = False

            if len(campos) > 1:
                isSess = True
                nomeSess = campos[-1].strip().strip(']')
                # print(nomeSess)
                s = Sessao(quote(unquote(nomeSess)))
                sessoes.append(s)
                # print('NomeSess: ', s.nome, sep='')
            elif isSess:
                camposSess = line.strip().split('=', 1)
                chave = camposSess[0].strip().strip('"')
                valor = camposSess[1].strip().strip('"')
                if valor.startswith('dword'):
                    valor = int(valor.replace('dword:', '', 1), 16)
                sessoes[-1].campo[chave] = valor
                # print(len(sessoes))

        except IndexError as e:
            # print(e)
            pass
        except ValueError as e:
            pass

        line = f.readline()
    f.close()
    # print(sessoes[-1])
    return sessoes


def exportaParaArquivos(ListaSessoes: List[Sessao], destino='.', chaves_dir=''):
    """
    Exporta a lista de sessões criadas com a função criaListaSessoes() no forma de arquivo adequado para o programa
        putty no Linux.

    :param ListaSessoes: uma lista de instãncias da classe Sessao, contendo dados de cada sessão.
    :param destino: diretório onde armazenar cada arquivo de sessão usado pelo programa putty no Linux.
    :param chaves_dir: diretório onde armazernar as chaves privadas.
    :return: Nada
    """
    # Cria o diretório destino caso não exista
    if chaves_dir == '':
        raise Exception('Deve ser informado o diretório onde se encontram as chaves!')
    if not path.exists(destino):
        makedirs(destino, mode=511, exist_ok=True)

    for sess in ListaSessoes:
        # with open(path.join(destino, unquote(sess.nome).replace(' ', '-').replace('(', '_').replace(')', '_')), 'w') as sessArq:
        with open(path.join(destino, sess.nome), 'w') as sessArq:
            for chave in sess.campo.keys():
                if chave == 'BellWaveFile':
                    valor = ''
                elif chave == 'Font':
                    valor = 'Fixed'
                elif chave == 'PublicKeyFile':
                    if valor != '':
                        valor = path.basename(sess.campo[chave])
                        if os.name == 'posix':
                            valor = path.join(chaves_dir, path.basename(sess.campo[chave].replace('\\', '/')))
                else:
                    valor = sess.campo[chave]

                try:
                    sessArq.write(f'{chave}={valor}\n')
                except (IOError, AttributeError):
                    pass


def exportaParaArquivoSSH(ListaSessoes: List[Sessao], chaves_dir=''):
    """
    Exparta a lista de sessões (instâncias da classe Sessão contendo os dados de cada sessão) para o formato adequado
        ao programa ssh.
        Esta função não retorna valor algum, mas direciona para a saída padrão o conteúdo a ser armazenado, por padrão,
        no arquivo ~/.ssh/config. Portanto para gerar esse arquivo, basta redirecionar a saída padrão para o arquivo,
        como no exemplo: > ~/.ssh/config

    :param ListaSessoes: uma lista de instãncias da classe Sessao, contendo dados de cada sessão.
    :param chaves_dir: diretório onde serão armazenadas as chaves privadas oriundas das chaves privadas no formato
        usado pelo programa putty do Windows. Note que para esse recurso funcinoar é necessário ter o pacote putty-tools
        instalado, mais especificamente puttygen
    :return: nada
    """
    sshText = "Host {host}\n" + \
              "   HostName {host_name}\n" + "   User {user_name}\n" + "   Port {port_number}\n" + "   IdentityFile {identity_file}\n"

    for sess in ListaSessoes:
        hostname = ''
        username = ''

        host = unquote(sess.nome).replace(' ', '-').replace('(', '_').replace(')', '_')

        if sess.campo['HostName'] != '':
            hostname = sess.campo['HostName']
        else:
            hostname = 'Desconhecido'

        if sess.campo['UserName'] != '':
            username = sess.campo['UserName']
        else:
            username = 'Desconhecido'

        if sess.campo['PublicKeyFile'] != '':
            ppkfile = path.join(chaves_dir, path.basename(sess.campo['PublicKeyFile'].replace('\\','/')))
            if path.exists(ppkfile):
                rsafile = path.splitext(ppkfile)[0]+'.rsa'
                errStatus = os.system(f'puttygen {ppkfile} -O private-openssh -o {rsafile}')
                if (errStatus):
                    print('Algo deu errado ao gerar a chave privada a partir do arquivo PPK.')
        else:
            rsafile = 'None'

        # print(sess.campo['PublicKeyFile'])
        # print(ppkfile)
        # print(rsafile)

        print(sshText.format(
            host=host,
            host_name=hostname,
            user_name=username,
            port_number=sess.campo['PortNumber'],
            identity_file=rsafile
        ))


if __name__ == '__main__':
    pass
