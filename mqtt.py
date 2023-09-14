# Importa a biblioteca paho.mqtt.client para usar MQTT.
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, broker_host, broker_port):
        self.client = mqtt.Client()  # Cria uma instância do cliente MQTT.
        self.broker_host = broker_host  # Armazena o endereço do Broker MQTT.
        self.broker_port = broker_port  # Armazena a porta do Broker MQTT.
        # Define a função de callback para conexão.
        self.client.on_connect = self.on_connect
        # Define a função de callback para mensagens recebidas.
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # Mensagem de sucesso ao conectar ao Broker MQTT.
            print("Conectado ao Broker MQTT")
        else:
            print(f'Falha na conexão com o Broker MQTT, código de resultado: {rc}')

    def on_message(self, client, userdata, msg):
        print(
            f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

    def connect(self):
        # Conecta ao Broker MQTT.
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()  # Inicia o loop para processar mensagens.

    def subscribe(self, topic):
        self.client.subscribe(topic)  # Subscreve a um tópico MQTT.

    def publish(self, topic, message):
        # Publica uma mensagem em um tópico MQTT.
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.loop_stop()  # Para o loop de processamento de mensagens.
        self.client.disconnect()  # Desconecta do Broker MQTT.


if __name__ == "__main__":
    broker_host = "localhost"  # Altere para o endereço do seu Broker MQTT.
    broker_port = 1883         # Altere para a porta do seu Broker MQTT.

    # Cria uma instância da classe MqttClient.
    mqtt_client = MqttClient(broker_host, broker_port)
    mqtt_client.connect()  # Conecta ao Broker MQTT.

    topic = "exemplo/topico"  # Altere para o tópico desejado.

    while True:
        # Solicita ao usuário uma mensagem para publicar.
        message = input("Digite a mensagem para publicar (ou 'q' para sair): ")
        if message.lower() == "q":
            break  # Sai do loop se o usuário digitar 'q'.
        # Publica a mensagem no tópico MQTT especificado.
        mqtt_client.publish(topic, message)

    mqtt_client.disconnect()  # Desconecta do Broker MQTT ao finalizar.
