from machine import Pin, PWM
import time

class Actuadores:
    def __init__(self, pin_rele=15, pin_buzzer=14, pin_led_rojo=26, pin_led_verde=27):
        # Configuración de salidas
        self.rele = Pin(pin_rele, Pin.OUT)
        self.led_rojo = Pin(pin_led_rojo, Pin.OUT)
        self.led_verde = Pin(pin_led_verde, Pin.OUT)
        
        # Configuración de PWM para el Buzzer
        self.buzzer = PWM(Pin(pin_buzzer))
        self.buzzer.duty(0) # Apagado inicialmente
        
        # Estado inicial (Sistema en Reposo)
        self.establecer_estado_normal()

    def establecer_estado_normal(self):
        self.led_verde.value(1)
        self.led_rojo.value(0)
        self.apagar_sirena()

    def activar_sirena(self, frecuencia=1000):
        self.rele.value(1)
        self.led_verde.value(0)
        self.led_rojo.value(1)
        self.buzzer.freq(frecuencia)
        self.buzzer.duty(512) # 50% ciclo de trabajo (sonido)

    def apagar_sirena(self):
        self.rele.value(0)
        self.buzzer.duty(0)