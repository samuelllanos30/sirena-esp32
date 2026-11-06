# Cliente MQTT configurado para broker público (broker.hivemq.com)
import network
import time
import umqtt.simple

class ClienteMQTT:
    def __init__(self, client_id, server="broker.hivemq.com"):
        self.client_id = client_id
        self.server = server
        self.client = None

    def conectar_wifi(self, ssid="Wokwi-GUEST", password=""):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print("Conectando a la red Wi-Fi simulada...")
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                time.sleep(0.5)
        print("Wi-Fi Conectado. IP:", wlan.ifconfig()[0])

    def conectar_broker(self, callback_sub):
        self.client = umqtt.simple.MQTTClient(self.client_id, self.server)
        self.client.set_callback(callback_sub)
        print("Conectando al Broker MQTT:", self.server)
        self.client.connect()
        print("Conectado con éxito al Broker MQTT")

    def suscribir(self, topico):
        self.client.subscribe(topico)
        print("Suscrito al tópico:", topico)

    def publicar(self, topico, mensaje):
        self.client.publish(topico, mensaje)

    def verificar_mensajes(self):
        self.client.check_msg()
