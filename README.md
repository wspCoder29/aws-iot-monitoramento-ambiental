# AWS - Monitoramento ambiental com IoT, Timestream e Grafana




<div align="center">
  <img src="https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Imagens/imagem%20por%20DALLE.jpg" width="500" height="500">
</div>


Nesse projeto utilizei os serviços da Cloud AWS, um Raspberry Pi e um sensor (BME 680) para coletar e armazenar dados ambientais em tempo real, incluindo temperatura, umidade e qualidade do ar. Os dados são transmitidos para o AWS IoT Core através do protocolo MQTT e processados com uma rule para armazenamento no AWS Time Stream. Também mostro como criar visualizações dos dados usando o Grafana, gerando painéis de controle para monitoramento de temperatura, umidade e qualidade do ar.

É possível reproduzir este projeto seguindo o vídeo abaixo. 
É necessário ter uma conta na AWS, o uso dos serviços: AWS Timestream e AWS Grafana não excederam 10 reais no total, incluindo testes durante o aprendizado e desenvolvimento e implementação.

[Vídeo do Projeto sendo implementado](https://youtu.be/YhJjQmOE6ZA)


Itens de Hardware:

* 1x Raspberri Pi4B
* 1x Sensor de temperatura, humidade, pressão atmosférica e qualidade do ar [BME680](https://pt.aliexpress.com/item/1005003676224000.html?src=google&src=google&albch=shopping&acnt=768-202-3196&slnk=&plac=&mtctp=&albbt=Google_7_shopping&isSmbAutoCall=false&needSmbHouyi=false&albcp=17364768653&albag=&trgt=&crea=pt1005003676224000&netw=x&device=c&albpg=&albpd=pt1005003676224000&gad_source=1&gclid=CjwKCAiA1fqrBhA1EiwAMU5m_81T6J-Q4jQ46njKIGjvVhr39i4Et92919IejDmZDfCoh-hK6Xi6zhoCwMIQAvD_BwE&gclsrc=aw.ds&aff_fcid=8d9868ed4be34ec0965a8b7567401973-1702816871135-09958-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=8d9868ed4be34ec0965a8b7567401973-1702816871135-09958-UneMJZVf&terminal_id=3c1f40854543484b9515cc2ef271eb40&afSmartRedirect=y)


* 1x Breadboard

* 1x Led (usado para debugging, não realmente necessário)
 
* 4x Jumpers (fios para conexões)

Software para coleta dos dados e escrita de um arquivo csv com as leituras.

[Software: programa em python](https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Software/AWS_IoT.py)




* Layout do Projeto

<div align="center">
  <img src="https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Imagens/Layout%20do%20projeto.png" width="1000" height="500">
</div>

Os dados são coletados pelo raspberri pi e enviados via mqtt para a cloud AWS, uma rule direciona os dados para o Timestream, onde ocorre a persistência.
Uma vez configurado, o Grafana gerenciado pela AWS permite a criação de dashboards para visualização.


* Conexões de Hardware

<div align="center">
  <img src="https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Imagens/bmeCONECTIONS.png" width="1000" height="500">
</div>


