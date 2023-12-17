# AWS - Monitoramento ambiental com IoT, Timestream e Grafana


![Texto Alternativo]([https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Imagens/DALL%C2%B7E%202023-10-25%2017.54.23%20-%20Black%20and%20white%20vector%20illustration%20where%20a%20Raspberry%20Pi%20in%20grayscale%20floats%20over%20a%20white%20ground.%20Above%2C%20an%20accurate%20representation%20of%20the%20AWS%20logo%20is.png])



Nesse projeto utilizei os serviços da Cloud AWS, um Raspberry Pi e um sensor (BME 680) para coletar e armazenar dados ambientais em tempo real, incluindo temperatura, umidade e qualidade do ar. Os dados são transmitidos para o AWS IoT Core através do protocolo MQTT e processados com uma rule para armazenamento no AWS Time Stream. Também mostro como criar visualizações dos dados usando o Grafana, gerando painéis de controle para monitoramento de temperatura, umidade e qualidade do ar.

[Vídeo do Projeto sendo implementado](https://youtu.be/YhJjQmOE6ZA)


Itens de Hardware:

* Raspberri Pi4B
* Sensor de temperatura, humidade, pressão atmosférica e qualidade do ar [BME680](https://pt.aliexpress.com/item/1005003676224000.html?src=google&src=google&albch=shopping&acnt=768-202-3196&slnk=&plac=&mtctp=&albbt=Google_7_shopping&isSmbAutoCall=false&needSmbHouyi=false&albcp=17364768653&albag=&trgt=&crea=pt1005003676224000&netw=x&device=c&albpg=&albpd=pt1005003676224000&gad_source=1&gclid=CjwKCAiA1fqrBhA1EiwAMU5m_81T6J-Q4jQ46njKIGjvVhr39i4Et92919IejDmZDfCoh-hK6Xi6zhoCwMIQAvD_BwE&gclsrc=aw.ds&aff_fcid=8d9868ed4be34ec0965a8b7567401973-1702816871135-09958-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=8d9868ed4be34ec0965a8b7567401973-1702816871135-09958-UneMJZVf&terminal_id=3c1f40854543484b9515cc2ef271eb40&afSmartRedirect=y)


* Breadboard

* Led (usado para debugging, não realmente necessário)
 
* Jumpers (fios para conexões)

Software para coleta dos dados e escrita de um arquivo csv com as leituras.

[Software: programa em python](https://github.com/wspCoder29/aws-iot-monitoramento-ambiental/blob/main/Software/AWS_IoT.py)

