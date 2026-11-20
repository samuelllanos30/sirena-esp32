class EstadoSistema:
    """Almacena y gestiona el estado simulado de la Sirena Comunitaria IoT."""
    def __init__(self):
        self.sirena_activa: bool = False
        self.motivo_alarma: str = "Sin novedades"
        self.nivel_gas: int = 850          # Escala ADC 12 bits (0 - 4095)
        self.umbral_gas: int = 2500        # Mismo umbral configurado en firmware
        self.frecuencia_hz: int = 1500     # Frecuencia PWM del buzzer
        self.sector: str = "Sector Centro - Parque Principal"
        self.simulacion_auto: bool = True  # Fluctuación periódica de sensores