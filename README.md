
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



#### Execução dos testes

python -m unittest discover -s tests -v