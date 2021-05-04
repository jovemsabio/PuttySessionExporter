# PuttySessionExporter

Script para exportar as sessões salvas do Putty no Windows para arquivos reconhecidos pelo Putty no Linux.
Desta forma, se desejar usar o Putty para Linux, poderá exportar as sessões salvas deste programa do Windows.

Para exportar as sessões do Putty no Windows para um arquivo que será usado por este script, execute o seguinte comando no prompt de comandos do Windows:

reg export HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY c:\putty_sessions.reg

Onde:
- putty_sessions.reg é o arquivo exportado. O nome é arbitrário.

Esse arquivo gerado pode ser usado também como um backup das sessões do Putty ou ainda como uma forma de migrar as sessões do Putty de um computador com Windows para outro também com o Windows.

Este arquivo será usado por este script python para ser lido e então gerar os arquivos de sessão para ser usado pelo putty em Linux.
Note que as chaves privadas criadas com puttygen não serão exportadas automaticamente, você terá de copia-las manualmente e então imformar o diretório onde elas se encontram para o script python poder gerar as chaves privadas no formato usado por openssh (ssh).
Para o recurso de conversão de chaves privadas do putty para o openssh funcionar no Linux é necessário que previamente tenha instalado os pacotes putty e putty-tools.

Exemplo de execução:
python3 main.py -f /home/<nome_usuário>/putty_sessions.reg -d /home/<nome_usuário>/.putty/sessions -k /home/<nome_usuário>/.putty/chaves

Onde:
- /home/<nome_usuário>/.putty/sessions é o diretório onde, por padrão, o putty no Linux busca pelos arquivos de sessão (cada arquivo é uma sessão salva).
- /home/<nome_usuário>/.putty/chaves é uma sugestão de onde copiar as chaves privadas. O putty no Linux não faz qualquer referência a esse diretório por padrão. Sendo referenciado apenas em cada arquivo de sessão em /home/<nome_usuário>/.putty/sessions

