from machine import Pin, ADC

class Sensores:
    def __init__(self, pin_mq2=34, pin_boton=12):
        # Configuración del sensor de gas analógico (ADC)
        self.mq2 = ADC(Pin(pin_mq2))
        self.mq2.atten(ADC.ATTN_11DB) # Lectura en rango de 0 a 3.3V
        
        # Configuración del botón de pánico (PULL_UP interno)
        self.boton = Pin(pin_boton, Pin.IN, Pin.PULL_UP)
        self.estado_anterior_boton = 1 # 1 es NO presionado (Pull-Up)

    def leer_nivel_gas(self):
        return self.mq2.read()

    def detecto_pulsacion(self):
        """
        Detecta únicamente el instante EXACTO en que se presiona el botón (flanco de bajada),
        evitando lecturas falsas continuas mientras se mantiene presionado.
        """
        estado_actual = self.boton.value()
        pulsado = False
        
        # Si antes estaba en 1 (soltado) y ahora pasa a 0 (presionado)
        if self.estado_anterior_boton == 1 and estado_actual == 0:
            pulsado = True
            
        self.estado_anterior_boton = estado_actual
        return pulsado