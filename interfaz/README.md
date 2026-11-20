# Interfaz Gráfica - Sirena Comunitaria IoT (Parcial 3)

Panel de supervisión y control desarrollado en **Python** utilizando el framework **Flet**, diseñado para monitorear en tiempo real las variables ambientales y gestionar las alertas del sistema comunitario basado en **ESP32**.

## Funcionalidades principales

- **Banner de estado y selección de nodo:** Indicador visual dinámico (vigilancia normal o alerta activa) y selector de sector comunitario monitoreado.
- **Monitoreo de Gas / Humo (GPIO 34 - ADC):** Visualización en escala de 12 bits (`0 - 4095 ADC`) con barra de progreso dinámica, modo de fluctuación automática y control deslizante manual para pruebas.
- **Control de Sirena y Actuadores:** Botones de activación de pánico y silenciado remoto, junto con indicadores de estado para el relé de potencia (`GPIO 15`) y la frecuencia PWM del buzzer (`GPIO 14`).
- **Configuración con Validación:** Formulario para ajustar el umbral crítico de detección (`100 - 4095 ADC`) y seleccionar la frecuencia del tono de alarma (`1000 Hz`, `1500 Hz` o `2200 Hz`).
- **Historial de Eventos:** Registro cronológico en tiempo real con marca de hora, origen de cada alerta y opción para limpiar el historial.

## Requisitos e instalación

1. Tener instalado **Python 3.9** o superior.
2. Instalar la dependencia principal de interfaz gráfica:
   ```bash
   pip install flet
   ```
   *(O usando el archivo de dependencias: `pip install -r interfaz/requirements.txt`)*

## Ejecución

Desde la carpeta raíz del repositorio (`sirena-esp32`):

```bash
python interfaz/main.py
```
