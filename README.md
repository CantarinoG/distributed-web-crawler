# Objetivo

Esse projeto consiste num web crawler distribuído cujo objetivo é recomendar livros a partir de palavras-chave fornecidas pelo usuário.

# Funcionamento

O projeto utiliza do framework Scrapy para criação de web crawlers e usa o Redis para manter informações necessárias para os crawlers num local centralizado.

Os crawlers realizam buscas no site [GoodReads](https://www.goodreads.com/), partindo de seeds que contém a pesquisa de livros com as palavras-chave fornecidas pelo usuário. 

As seeds são inicialmente inseridas numa fila do Redis. Os crawlers visitam o primeiro item dessa lista, e adicionam a ela novos links de livros que encontrarem.

Para garantir que não haja a repetição de páginas visitadas, os crawlers adicionam todas as urls que já foram encontradas previamente em um conjunto no Redis. Dessa forma, quando visitam um site e encontram um novo link, eles primeiro checam se esse link já foi encontrado previamente e não o adicionam na fila se esse for o caso. Os crawlers também checam se o link encontrado é uma página de livro do site, para evitar que sejam visitadas páginas que não pertencem ao site ou ainda páginas gerais do site, que iriam conter o link de livros não relacionados as palavras-chave inseridas pelo usuário.

Para cada visita de página, os crawler salvam as informações do livro(nome, nota, descrição e url) no formato .json em um conjunto no Redis. Para que essa informação depois possa ser lida e processada pelo usuário como ele bem enteder.

# Instalação

* Criar um ambiente virtual no projeto com `python3 -m venv venv`
* Ativar o ambiente virtual no projet com `source venv/bin/activate`
* Instalar as dependências(scrapy e scrapy-redis) com `pip install scrapy scrapy-redis`
* Criar no diretório root do projeto um arquivo chamado de `db_secrets.py`, que deve conter uma variável chamada `redis_url` com a string da URL de conexão ao Redis (pode ser uma instância local ou em cloud, que pode ser adquirida gratuitamente no site oficial do Redis).

# Utilização

* Para definir as palavras-chave, basta inserí-las no vetor `key_words`, dentro de `user_settings.py`. O arquivo também possui outras variáveis de configuração que podem ser mudadas.
* Para definir o nome do conjunto que obterá os resultados, basta mudar o valor de `result_set_name` em `user_settings.py`.
* Antes de rodar os crawlers, é necessário limpar e popular a fila do Redis com as seeds utilizando `python3 reset_queue.py`.
* Para rodar os crawlers, basta rodar `scrapy crawl distributed_spider`. Múltiplos crawlers podem ser rodados simultaneamente, inclusive a partir de diferente máquinas.     
    
Os crawlers podem ser parados e resumidos a qualquer hora. Entretanto, se deseja mudar as palavras-chave, deve-se rodar `python3 reset_queue.py` novamente. Se o nome do conjunto que armazena os resultados não for alterado, os novos dados ficarão juntos no mesmo conjunto que os antigos.

# Pontos de Problemas e Melhorias

Realizada dessa forma, a aplicação precisa fazer um grande número de requisições ao Redis.      
Para saber qual URL deve ser visitada, é necessário requisitar essa informação ao Redis(esse número pode ser diminuido aumentando o `batch_size` em `user_settings.py`, para cada requisição, o crawler pegará o valor determinado de URLs).       
Para cada página visitada, é inserido uma informação num conjunto do Redis.       
Para cada URL visitado, é necessário requerer informações do Redis(checar se a URL encontrada já está no conjunto de URLs encontrados anteriormente) e inserir a nova URL.    
    
Utilizando uma instância do Redis hospedada na nuvem, a aplicação requer então um enorme consumo de banda e tempo para comunicação. Esse problema não é tão grave se a instância do Redis é local, dentro da mesma rede, já que o tempo de comunicação é reduzido.

**Portanto, essa aplicação performa melhor com instâncias locais do Redis, e não hospedadas da nuvem.**

Outro ponto é o registro das informações coletadas. O Redis não possui uma estrutura de dados nativa que se assemelhe a uma tabela tradicional para registros de dados. Atualmente, os dados são armazenados em formato JSON em um conjunto do Redis. Para um registro mais estruturado e consultas avançadas, **seria ideal utilizar um banco de dados tradicional ou um banco de dados NoSQL apropriado**.

# Questões Éticas

Algumas das questões éticas comumente levantadas quando se fala sobre web crawlers são a questão de respeito ao `robots.txt` e a sobrecarga de servidores web.   
   
O Scrapy dá suporte para respeitar o `robots.txt` do site visitado, bastando selecionar isso dentro das suas configurações. Nesse projeto, o respeito a essa política de exclusão de sites está ativada por padrão, mas é possível ser alterado dentro do arquivo `redis-python-scrapy-examples/settings.py`, mudando o valor da variável `ROBOTSTXT_OBEY`.

Quanto à sobrecarga de servidores web, alguns `robots.txt` definem o valor `crawl-delay`, que define um mínimo de tempo entre as requisições ao site. Isso será respeitado se o Scrapy estiver configurada para respeitar o `robots.txt`.    
Do contrário, o projeto possui um intervalo padrão de 1 segundo entre cada requisição. Esse valor pode ser mudado dentro de `user_settings.py`.     
Esse intervalo é respeitado para cada crawler, então se há muitos crawlers requisitando do mesmo servidor web em paralelo, seria ideal aumentá-lo um pouco, a depender do número de crawlers, para não sobrecarregar o servidor.

# Cenários de Falha

A aplicação é bem flexível, crawlers podem ser iniciados, parados e resumidos a qualquer momento, independente de quantos sejam.

Entretanto, para o funcionamento da aplicação, **a instância do Redis precisa estar ativa**.

Caso não exista uma instância ativa do Redis, os crawlers irão aguardar um tempo determinado esperando a conexão retornar. Uma vez que esse tempo passe, eles irão se desligar sozinhos, oque evita consumo ocioso da CPU com os crawlers. Esse tempo tem valor padrão de 60 segundos mas pode ser alterado em `user_settings.py`.

No caso de uma instância do Redis hospedada na nuvem, isso não é um problema tão grande para o desenvolvedor, pois a não ser que a cloud do Redis tenha caído, a instância do Redis sempre estará ativa.       
Entretanto, é importante proteger a chave para conexão ao banco, bem como nome de usuário e senha, e utilizar criptografia caso a coleta de dados envolva dados sensíveis.

Caso a instância do Redis esteja sendo hospedada localmente, é importante prevenir para que o sistema não tenha algum problema e fique inativo. É importante haver proteção contra falhas e acessos não autorizados.    
Isso pode ser feito com coisas como:
* Monitoramento em tempo real e configuração de alertas para problemas como alto uso de CPU, memória insuficiente ou falha de conexões.
* Backups automáticos e testes de restauração.
* Autenticação e configuração de Firewall para permitir que apenas IPs autorizados acessem o Redis.
* Encriptação de dados, caso a aplicação seja adaptada para coletar algum tipo de dados sensíveis.
* Manter o Redis e outros serviços utilizados sempre na versão mais atual.

