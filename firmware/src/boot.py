# boot.py - Ejecución inicial del microcontrolador
import esp
esp.osdebug(None) # Desactiva mensajes innecesarios de depuración
import gc
gc.collect() # Limpieza de memoria RAM
print("Iniciando firmware de la ESP32...")