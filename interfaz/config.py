# Configuración general del sistema de monitoreo comunitario

APP_TITLE = "Centro de Monitoreo - Sirena Comunitaria IoT"
INTERVALO_TELEMETRIA_SEG = 2.0

# Parámetros de hardware ESP32 (Parcial 2)
ADC_MIN = 0
ADC_MAX = 4095
UMBRAL_GAS_DEFECTO = 2500
FRECUENCIA_BUZZER_DEFECTO = 1500

# Configuración futura para integración MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICO_COMANDO = "pueblo/sirena/comando"
TOPICO_SENSORES = "pueblo/sirena/sensores"
TOPICO_ESTADO = "pueblo/sirena/estado"