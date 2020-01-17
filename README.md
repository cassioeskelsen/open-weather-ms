
### OpenWeatherMap microservice client

Exemplo de utilização da API do OpenWeatherMap através de um micro serviço.

#### Escopo Geral

Sabendo que o clima influencia diretamente no consumo de bebidas e que dias chuvosos atrasam a entrega de pedidos, é necessário fazer a consulta da previsão para os próximos 5 dias e cadastrá-las localmente. 
A previsão será composta das temperaturas máxima, mínima e do dia, sensação térmica durante o dia, umidade relativa do ar e possibilidade de chuva.
Essa previsão deverá ser cadastrada em um banco de dados local e cada consulta sobrescreverá consultas anteriores.
A consulta será feita pelo nome da cidade e não pelo seu "_id_" em um serviço específico, dessa forma não ficamos amarrados com um único provedor de informação.

#####Limitações e Restrições

a) Sabe-se que uma cidade grande pode ter vários microclimas diferentes e para isso seria interessante a consulta por coordenadas ou mesmo pelo CEP.
 No entanto, para essa POC a consulta será feita pela cidade inteira, ou seja, teremos uma "média" dos microclimas.

b) Será utilizado o SI (Sistema Métrico) para os valores.

c) A API REST tem apenas a função de solicitar a consulta ao OpenWeather e gravar a resposta, ela não será responsável por exibir os dados para o usuário final.


#### Escopo Técnico

Deverão ser feitos 2 microservices: 

**Microservice1**: deverá expor uma API REST que permitirá uma solicitação de consulta de previsão do tempo em algum provedor e persistirá o resultado dessa consulta em um banco de dados local

**Microservice2**: será responsável pela consulta no provedor de informações. Nessa POC o provedor será o OpenWeatherMap, também conhecido simplesmente como OpenWeather.

A comunicação entre os dois microservices deverá ser feita por algum serviço de mensageria. Aqui será utilizado o RabbitMQ.

#### Explicação do Funcionamento/Design

O código roda todo em containers Docker, sendo que temos 4 amarradas por um docker-compose:

**a)** Microservice1 / **b)** Microservice2 / **c)** RabbitMQ / **d)** PostgreSQL

Os containers RabbitMQ e PostgreSQL são containers pré-compilados pelos seus mantenedores e utilizados praticamente as-is.

O **Microservice2** tem como responsabilidade escutar as solicitações de previsão do tempo vindas do broker e fazer a consulta no OpenWeather. 
O script responsável por ouvir as solicitações é o **WeatherUpdatesHandler**. Ele está construído de tal forma que pode ser convertido facilmente  em um Facade caso deseja-se tornar esse microservice compatível com outros provedores do clima ou facilitar a criação de um novo para um outro provider.

Ao receber uma solicitação de update de previsão, ele instancia um objeto do tipo **OpenWeatherClient** que é responsável pela efetiva consulta no OpenWeather. 
A resposta é devolvida em um objeto **Forecast** para WeatherUpdatesHandler que é responsável também por devolver os resultados ao broker. 

O **Microservice1** expõe uma API rest para solicitar a consulta tendo parâmetros o nome da cidade e o código do país (ISO-3166) ou apenas o nome da cidade (nesse caso o microservice adicionará automaticamente BR).
Pode-se ver as duas formas nas chamadas abaixo:
```bash
curl http://localhost:5000/weather/v1.0/updateForecasts/Ibirama,BR
curl http://localhost:5000/weather/v1.0/updateForecasts/Blumenau
curl http://localhost:5000/weather/v1.0/updateForecasts/Oslo,NO  
```

Uma vez requisitado pela API REST (que está no script app.py), a requisição é enviada para o broker de forma assíncrona.

Uma instância da classe **WeatherResponseHandler** fica em execução em uma thread separada ouvindo as respostas vindas do broker. 

A resposta é persistida no banco de dados PostgreSQL através da library SQLAlchemy. No entanto, antes de persistir os dados é verificado se já existe uma previsão para aquele dia e para aquela cidade. Se existir os dados são sobrescritos pois não faz sentido manter duas previsões do tempo para o mesmo dia e para a mesma cidade.

##### Comunicação com o broker

A comunicação é feita através de dois objetos que estão nas pastas broker_interface: GenericProducer e GenericConsumer. Fica como to-do converter essas classes em uma library. No momento optou-se em duplicá-las dentro de cada microservice para facilitar o build do container. Também é necessário implementar/melhorar alguns mecanismos de tolerância à falhas como re-conexão. 

As requisições do microservice1 para o microservice2 são feitas pelo tópico **weatherUpdateRequest** enquanto que as respostas trafegam pelo **weatherUpdateResponse**.

#### Testando o código

**Estou considerando que você já tenha instalado o Python3, o PIP3, docker e docker-compose**

Eu [gravei um vídeo](https://www.youtube.com/watch?v=mO0oCRzTnSg) com a execução dos passos/testes caso você deseje apenas ter uma visão geral sem instalar nada

:warning: **Atenção**

Você deve setar a variável de ambiente OWMAPI com sua chave de API do OpenWeather. Essa chave não é gravada no GITHUB pois é individual

Exemplos: supondo que sua chave seja XPTO:

No linux:
```bash
export OWMAPI=XPTO
```
No Windows:
```bash
set OWMAPI=XPTO
```

##### Obtendo os fontes

```bash
git clone https://github.com/cassioeskelsen/open-weather-ms.git
```

Setando as variáveis de ambiente

```bash
Linux:
source ./env.sh

Windows:
env.bat
```

##### Construindo e subindo o ambiente docker
```bash
docker-compose up -d --build
```
##### Testando o sistema

Instalar requerimentos localmente (para rodar o script e testes)

```bash
pip3 install -r requirements.txt
```

Junto com os fontes segue um pequeno utilitário para testar o sistema, o weather.py

Exemplos:

Solicita a previsão do tempo no OpenWeather e grava no banco (sempre no format Cidade, Codigo País ou apenas cidade):_
```bash
python3 weather.py -r Indaial,BR
```

lista a previsão previamente gravada:
```bash
python3 weather.py -l Indaial,BR
```

solicita e lista a previsão (delay de 1 segundo para dar tempo de buscar no OpenWeather):_
```bash
python3 weather.py -s Blumenau,BR
```

Alternativamente pode ser usado o curl para solicitar a previsão no OpenWeather, Exemplo:

```bash
curl  http://localhost:5000/weather/v1.0/updateForecasts/Lontras,BR
```


##### Todos comandos de uma vez (linux)
```bash
git clone https://github.com/cassioeskelsen/open-weather-ms.git
cd open-weather-ms
export OWMAPI=SUA_API
source ./env.sh
docker-compose up -d --build
pip3 install -r requirements.txt
python3 weather.py -r Indaial,BR
python3 weather.py -l Indaial,BR
python3 weather.py -s Blumenau,BR
```

##### Testes unitários e de Integração

Obs: por enquanto os testes rodam na base quente e não foi feito mock-up do broker, ele precisa estar no ar para os testes passarem.

```bash
python3 -W ignore  -m unittest discover -s . -b
```