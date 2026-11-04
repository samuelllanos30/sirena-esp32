import time
import ujson
from actuators import Actuadores
from sensors import Sensores
from mqtt_client import ClienteMQTT

# Inicialización de hardware y módulos
actuadores = Actuadores()
sensores = Sensores()
mqtt = ClienteMQTT(client_id="ESP32_Sirena_Pueblo")

# Variables de control de estado
sirena_activa = False
tiempo_previo_telemetria = time.ticks_ms()
INTERVALO_TELEMETRIA = 2000 # Publicar telemetría cada 2 segundos
UMBRAL_GAS_ALERTA = 2500    # Umbral de gas en Wokwi (0 - 4095)

# Función callback para procesar comandos recibidos por MQTT
def procesar_comando_mqtt(topic, msg):
    global sirena_activa
    topico_str = topic.decode('utf-8')
    mensaje_str = msg.decode('utf-8')
    print("📥 MQTT Recibido ->", topico_str, ":", mensaje_str)
    
    try:
        data = ujson.loads(mensaje_str)
        if "accion" in data:
            if data["accion"] == "ACTIVAR":
                sirena_activa = True
                actuadores.activar_sirena(frecuencia=1200)
                print("🔊 Sirena ACTIVADA por MQTT")
            elif data["accion"] == "SILENCIAR":
                sirena_activa = False
                actuadores.establecer_estado_normal()
                print("🔇 Sirena SILENCIADA por MQTT")
    except Exception as e:
        print("Error en JSON:", e)

# Conexión Wi-Fi y Broker MQTT
mqtt.conectar_wifi()
mqtt.conectar_broker(procesar_comando_mqtt)
mqtt.suscribir(b"pueblo/sirena/comando")
mqtt.publicar(b"pueblo/sirena/conexion", ujson.dumps({"estado": "ONLINE"}))

print("=== Sistema de Sirena Comunitaria Listo ===")

# Bucle Principal
while True:
    # A. Revisar si llegaron mensajes MQTT
    mqtt.verificar_mensajes()
    
    # B. Lecturas de hardware
    nivel_gas = sensores.leer_nivel_gas()
    boton_presionado = sensores.detecto_pulsacion() # True solo en el instante que se presiona
    
    # C. Lógica del Botón de Emergencia (Alternador ON / OFF)
    if boton_presionado:
        sirena_activa = not sirena_activa # Invierte el estado actual
        
        if sirena_activa:
            actuadores.activar_sirena(frecuencia=1500)
            print("🚨 Sirena ACTIVADA manualmente con el Botón")
            mqtt.publicar(b"pueblo/sirena/estado", ujson.dumps({"sirena": "ACTIVA", "causa": "BOTON_PANICO"}))
        else:
            actuadores.establecer_estado_normal()
            print("🔇 Sirena SILENCIADA manualmente con el Botón")
            mqtt.publicar(b"pueblo/sirena/estado", ujson.dumps({"sirena": "INACTIVA", "causa": "SILENCIADO_MANUAL"}))

    # D. Activación automática por Sensor de Humo/Gas
    elif nivel_gas > UMBRAL_GAS_ALERTA and not sirena_activa:
        sirena_activa = True
        actuadores.activar_sirena(frecuencia=1800)
        print("🔥 ALERTA DE HUMO DETECTADA! (Lectura Nivel:", nivel_gas, ")")
        mqtt.publicar(b"pueblo/sirena/estado", ujson.dumps({"sirena": "ACTIVA", "causa": "SENSOR_GAS"}))

    # E. Envío periódico de datos (Telemetría)
    if time.ticks_diff(time.ticks_ms(), tiempo_previo_telemetria) >= INTERVALO_TELEMETRIA:
        tiempo_previo_telemetria = time.ticks_ms()
        payload = {
            "humo_ppm": nivel_gas,
            "sirena_activa": sirena_activa
        }
        mqtt.publicar(b"pueblo/sirena/sensores", ujson.dumps(payload))
    
    time.sleep_ms(50)