
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


#### Escopo Técnico

Deverão ser feitos 2 microservices: 

**Microservice1**: deverá expor uma API REST que permitirá uma solicitação de consulta de previsão do tempo em algum provedor e persistirá o resultado dessa consulta em um banco de dados local

**Microservice2**: será responsável pela consulta no provedor de informações. Nessa POC o provedor será o OpenWeatherMap, também conhecido simplesmente como OpenWeather.

A comunicação entre os dois microservices deverá ser feita por algum serviço de mensageria. Aqui será utilizado o RabbitMQ.



#### Testando o código

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

Obtendo os fontes

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

Construindo e subindo o ambiente docker
```bash
docker-compose up -d --build
```
##### Testando o sistema

Junto com os fontes segue um pequeno utilitário para testar o sistema, o weather.py

Exemplos:

Solicita a previsão do tempo no OpenWeather e grava no banco (sempre no format Cidade, Codigo País ou apenas cidade):_
```bash
python weather.py -r Indaial,BR
```

lista a previsão previamente gravada:_
```bash
python weather.py -l Indaial,BR
```

solicita e lista a previsão (delay de 1 segundo para dar tempo de buscar no OpenWeather):_
```bash
python weather.py -s Blumenau,BR
```

#### Todos comandos de uma vez (linux)
```bash
git clone https://github.com/cassioeskelsen/open-weather-ms.git
source ./env.sh
docker-compose up -d --build
python weather.py -r Indaial,BR
python weather.py -l Indaial,BR
python weather.py -s Blumenau,BR
```

##### Testes unitários
```bash
python -m unittest discover -s tests -v
```