# Sistema de Sirena y Alarma Comunitaria Inteligente (ESP32 - MicroPython)

**Asignatura:** Programacion 2  
**Estudiante:** Samuel Llanos  
**Plataforma de Simulacion:** Wokwi  
**Lenguaje:** MicroPython  
**Protocolo de Comunicacion:** MQTT  

---

## Enlace a la Simulacion en Wokwi
Puedes ejecutar y probar la simulacion interactiva directamente en el siguiente enlace:  
**[Ver Simulacion en Wokwi](https://wokwi.com/projects/479675991136103425)**

---

## Descripcion del Proyecto
Este proyecto consiste en el desarrollo del firmware para un **Sistema de Alarma y Sirena Comunitaria Inteligente** disenado para pequenos poblados o zonas rurales. El sistema permite:

1. **Gestion de Emergencias Locales:** Activacion automatica mediante un sensor de humo/gas (MQ-2) o activacion manual a traves de un boton fisico de panico con logica alternadora (*toggle*).
2. **Supervision y Control Remoto via MQTT:** Envio periodico de telemetria (nivel de gas y estado de la sirena) y recepcion de comandos remotos desde una interfaz grafica para activar o silenciar la sirena de forma instantanea.

---

## Componentes Simulados (Wokwi)
* **Microcontrolador:** ESP32 (programado en MicroPython)
* **Sensor de Humo/Gas:** Sensor analogico interactivo / Potenciometro (`wokwi-gas-sensor`) conectado al GPIO 34 (ADC)
* **Actuador de Potencia:** Modulo de Rele (`wokwi-relay-module`) conectado al GPIO 15
* **Salida Auditiva:** Buzzer Piezoelectrico con modulacion PWM (`wokwi-buzzer`) conectado al GPIO 14
* **Entrada Digital:** Boton de Emergencia (`wokwi-pushbutton`) conectado al GPIO 12 con `PULL_UP` interno
* **Indicadores Visuales:** LED Verde (GPIO 27 - Sistema Normal) y LED Rojo (GPIO 26 - Alerta Activa)

---

## Topicos MQTT Implementados

### Publicacion (ESP32 - Interfaz / Broker)
* `pueblo/sirena/estado`: Informa cuando la sirena se activa o inactiva y la causa del evento (ej. `BOTON_PANICO`, `SENSOR_GAS`, `SILENCIADO_MANUAL`).
* `pueblo/sirena/sensores`: Envia la telemetria periodica del nivel de gas (PPM) y el estado actual del sistema.
* `pueblo/sirena/conexion`: Publica el estado de conexion del microcontrolador (`ONLINE`).

### Suscripcion (Interfaz - ESP32)
* `pueblo/sirena/comando`: Recibe objetos JSON para control remoto. Ejemplos de comandos:
  * `{"accion": "ACTIVAR"}`: Enciende la sirena y el rele de forma remota.
  * `{"accion": "SILENCIAR"}`: Apaga la sirena de inmediato.

---

## Estructura del Firmware (MicroPython)
El codigo fue modularizado para mantener un firmware limpio y mantenible:

* `src/boot.py`: Configuracion inicial del entorno y limpieza de memoria RAM.
* `src/actuators.py`: Clase `Actuadores` encargada de controlar el rele, los LEDs y la generacion de tonos PWM en el buzzer.
* `src/sensors.py`: Clase `Sensores` para la lectura analogica (ADC) del sensor MQ-2 y la deteccion por flanco del boton de panico (*toggle*).
* `src/mqtt_client.py`: Clase `ClienteMQTT` que gestiona la conexion Wi-Fi (`Wokwi-GUEST`) y la comunicacion con el Broker `broker.hivemq.com`.
* `src/main.py`: Bucle principal no bloqueante basado en `time.ticks_ms()`, encargado de coordinar los sensores, actuadores y mensajes MQTT sin detener la ejecucion del microcontrolador.