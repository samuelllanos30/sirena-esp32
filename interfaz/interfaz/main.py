import asyncio
import random
from datetime import datetime
import flet as ft
from estado import EstadoSistema

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
    page.title = "Centro de Monitoreo - Sirena Comunitaria IoT"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 1150
    page.window.height = 820

    estado = EstadoSistema()

    # --- ELEMENTOS VISUALES REACTIVOS ---
    # 1. Banner de Alarma Visual
    icono_banner = ft.Icon(ft.Icons.SHIELD_ROUNDED, color=ft.Colors.GREEN_300, size=34)
    titulo_banner = ft.Text(
        "SISTEMA EN VIGILANCIA NORMAL",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_200,
    )
    subtitulo_banner = ft.Text(
        "Monitoreo activo • Todos los parámetros dentro del rango seguro",
        size=13,
        color=ft.Colors.WHITE70,
    )
    banner_alarma = ft.Container(
        content=ft.Row(
            [
                icono_banner,
                ft.Column([titulo_banner, subtitulo_banner], spacing=2, expand=True),
                ft.Container(
                    content=ft.Text("MODO SIMULACIÓN", size=11, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.BLUE_GREY_800,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=ft.Colors.GREEN_900,
        border=ft.border.all(2, ft.Colors.GREEN_500),
        border_radius=12,
        padding=15,
    )

    # 2. Selector de Sector / Nodo (Dropdown)
    dropdown_sector = ft.Dropdown(
        label="Nodo Comunitario Monitoreado",
        value=estado.sector,
        options=[
            ft.dropdown.Option("Sector Centro - Parque Principal"),
            ft.dropdown.Option("Sector Norte - Salón Comunal"),
            ft.dropdown.Option("Sector Sur - Zona Industrial"),
        ],
        width=320,
    )

    # 3. Visualización de Sensor de Gas / Humo (ADC 0 - 4095)
    txt_valor_gas = ft.Text(f"{estado.nivel_gas} / 4095 ADC", size=28, weight=ft.FontWeight.BOLD)
    txt_estado_gas = ft.Text("Nivel Seguro", color=ft.Colors.GREEN_400, weight=ft.FontWeight.W_600)
    barra_gas = ft.ProgressBar(
        value=estado.nivel_gas / 4095,
        height=14,
        color=ft.Colors.GREEN_400,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=8,
    )

    # Slider para probar picos de gas manualmente durante la sustentación
    slider_gas_manual = ft.Slider(
        min=0,
        max=4095,
        divisions=81,
        value=estado.nivel_gas,
        label="{value} ADC",
    )

    # 4. Indicadores de Estado de Hardware (LEDs / Relé / PWM)
    badge_sirena = ft.Container(
        content=ft.Text("APAGADA", weight=ft.FontWeight.BOLD, size=12),
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
    )
    badge_rele = ft.Container(
        content=ft.Text("ABIERTO (0V)", weight=ft.FontWeight.BOLD, size=12),
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
    )
    txt_pwm_actual = ft.Text("0 Hz (Inactivo)", size=13, color=ft.Colors.WHITE70)

    # 5. Formulario de Configuración de Parámetros
    input_umbral = ft.TextField(
        label="Umbral Crítico de Gas (100 - 4095)",
        value=str(estado.umbral_gas),
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.SPEED,
        width=260,
    )
    dropdown_frecuencia = ft.Dropdown(
        label="Tono de Sirena (PWM)",
        value="1500",
        options=[
            ft.dropdown.Option("1000", "1000 Hz - Alerta Preventiva"),
            ft.dropdown.Option("1500", "1500 Hz - Emergencia Estándar"),
            ft.dropdown.Option("2200", "2200 Hz - Evacuación Aguda"),
        ],
        width=260,
    )
    txt_error_config = ft.Text("", color=ft.Colors.RED_400, size=12)

    # 6. Historial de Eventos
    lista_historial = ft.ListView(expand=True, spacing=8, auto_scroll=False)

    # --- FUNCIONES DE LÓGICA DE LA INTERFAZ ---
    def registrar_evento(titulo: str, detalle: str, es_alerta: bool = False):
        hora = datetime.now().strftime("%H:%M:%S")
        color_borde = ft.Colors.RED_400 if es_alerta else ft.Colors.BLUE_GREY_600
        icono = ft.Icons.WARNING_AMBER_ROUNDED if es_alerta else ft.Icons.INFO_OUTLINE

        item = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icono, color=color_borde, size=20),
                    ft.Column(
                        [
                            ft.Text(f"[{hora}] {titulo}", weight=ft.FontWeight.BOLD, size=13),
                            ft.Text(detalle, size=12, color=ft.Colors.WHITE70),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ]
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            border=ft.border.only(left=ft.BorderSide(4, color_borde)),
            padding=10,
            border_radius=6,
        )
        lista_historial.controls.insert(0, item)
        if len(lista_historial.controls) > 30:
            lista_historial.controls.pop()

    def refrescar_vista():
        # Actualizar indicadores de gas
        txt_valor_gas.value = f"{estado.nivel_gas} / 4095 ADC"
        barra_gas.value = min(max(estado.nivel_gas / 4095, 0.0), 1.0)
        slider_gas_manual.value = estado.nivel_gas

        if estado.nivel_gas >= estado.umbral_gas:
            barra_gas.color = ft.Colors.RED_500
            txt_estado_gas.value = f"¡PELIGRO! Supera umbral ({estado.umbral_gas})"
            txt_estado_gas.color = ft.Colors.RED_400
        elif estado.nivel_gas >= estado.umbral_gas * 0.75:
            barra_gas.color = ft.Colors.AMBER_400
            txt_estado_gas.value = "Precaución - Nivel Elevado"
            txt_estado_gas.color = ft.Colors.AMBER_300
        else:
            barra_gas.color = ft.Colors.GREEN_400
            txt_estado_gas.value = "Nivel Seguro"
            txt_estado_gas.color = ft.Colors.GREEN_400

        # Actualizar estado de sirena y banner visual
        if estado.sirena_activa:
            banner_alarma.bgcolor = ft.Colors.RED_900
            banner_alarma.border = ft.border.all(2, ft.Colors.RED_400)
            icono_banner.name = ft.Icons.NOTIFICATIONS_ACTIVE
            icono_banner.color = ft.Colors.RED_200
            titulo_banner.value = "¡ALERTA COMUNITARIA ACTIVADA!"
            titulo_banner.color = ft.Colors.WHITE
            subtitulo_banner.value = f"Motivo: {estado.motivo_alarma} • {estado.sector}"

            badge_sirena.content.value = "SONANDO (ON)"
            badge_sirena.bgcolor = ft.Colors.RED_600
            badge_rele.content.value = "CERRADO (110V ON)"
            badge_rele.bgcolor = ft.Colors.AMBER_700
            txt_pwm_actual.value = f"{estado.frecuencia_hz} Hz • Duty 50% (512)"
        else:
            banner_alarma.bgcolor = ft.Colors.GREEN_900
            banner_alarma.border = ft.border.all(2, ft.Colors.GREEN_500)
            icono_banner.name = ft.Icons.SHIELD_ROUNDED
            icono_banner.color = ft.Colors.GREEN_300
            titulo_banner.value = "SISTEMA EN VIGILANCIA NORMAL"
            titulo_banner.color = ft.Colors.GREEN_200
            subtitulo_banner.value = f"Monitoreo activo en {estado.sector} • Sin novedades"

            badge_sirena.content.value = "APAGADA (OFF)"
            badge_sirena.bgcolor = ft.Colors.BLUE_GREY_700
            badge_rele.content.value = "ABIERTO (0V)"
            badge_rele.bgcolor = ft.Colors.BLUE_GREY_700
            txt_pwm_actual.value = "0 Hz (Inactivo)"

        page.update()

    def activar_sirena(motivo: str):
        if not estado.sirena_activa:
            estado.sirena_activa = True
            estado.motivo_alarma = motivo
            registrar_evento("SIRENA ACTIVADA", f"Origen: {motivo} ({estado.sector})", es_alerta=True)
            refrescar_vista()

    def silenciar_sirena(e=None):
        if estado.sirena_activa:
            estado.sirena_activa = False
            estado.motivo_alarma = "Sin novedades"
            registrar_evento("SIRENA SILENCIADA", "Alarma desactivada manualmente desde el panel", es_alerta=False)
            refrescar_vista()

    def cambiar_gas_manual(e):
        estado.simulacion_auto = False
        switch_auto.value = False
        estado.nivel_gas = int(e.control.value)
        if estado.nivel_gas >= estado.umbral_gas:
            activar_sirena(f"Detección crítica de Gas/Humo ({estado.nivel_gas} ADC)")
        refrescar_vista()

    def toggle_simulacion_auto(e):
        estado.simulacion_auto = e.control.value
        modo = "activada" if estado.simulacion_auto else "pausada (control manual)"
        registrar_evento("Modo Simulación", f"Lectura periódica automática {modo}")
        page.update()

    def cambiar_sector(e):
        estado.sector = e.control.value
        registrar_evento("Cambio de Nodo", f"Monitoreando ahora: {estado.sector}")
        refrescar_vista()

    def guardar_parametros(e):
        txt_error_config.value = ""
        try:
            nuevo_umbral = int(input_umbral.value)
            if not (100 <= nuevo_umbral <= 4095):
                txt_error_config.value = "Error: El umbral debe estar entre 100 y 4095."
                page.update()
                return

            estado.umbral_gas = nuevo_umbral
            estado.frecuencia_hz = int(dropdown_frecuencia.value)
            registrar_evento(
                "Parámetros Actualizados",
                f"Nuevo umbral: {estado.umbral_gas} ADC | Frecuencia PWM: {estado.frecuencia_hz} Hz",
            )
            page.open(ft.SnackBar(ft.Text("Configuración guardada correctamente"), bgcolor=ft.Colors.GREEN_700))

            if estado.nivel_gas >= estado.umbral_gas:
                activar_sirena(f"Nivel de gas ({estado.nivel_gas}) supera nuevo umbral ({estado.umbral_gas})")
            refrescar_vista()
        except ValueError:
            txt_error_config.value = "Error: Ingresa únicamente números enteros válidos."
            page.update()

    def limpiar_historial(e):
        lista_historial.controls.clear()
        registrar_evento("Historial Reiniciado", "Registro de eventos limpiado por el operador")
        page.update()

    # Asignar eventos a controles
    slider_gas_manual.on_change = cambiar_gas_manual
    switch_auto = ft.Switch(label="Fluctuación automática de sensor", value=True, on_change=toggle_simulacion_auto)
    dropdown_sector.on_change = cambiar_sector

    # --- TAREA PERIÓDICA ASÍNCRONA (SIMULACIÓN EN TIEMPO REAL) ---
    async def ciclo_telemetria():
        while True:
            await asyncio.sleep(2.0)
            if estado.simulacion_auto:
                # Simula pequeñas variaciones ambientales alrededor de un valor base
                variacion = random.randint(-120, 140)
                estado.nivel_gas = max(200, min(2300, estado.nivel_gas + variacion))
                refrescar_vista()

    # --- CONSTRUCCIÓN DEL LAYOUT (TARJETAS) ---
    header = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Sirena Comunitaria Inteligente • Panel IoT", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Interfaz de Supervisión y Control (ESP32 + MQTT)", size=13, color=ft.Colors.WHITE70),
                ],
                spacing=2,
                expand=True,
            ),
            dropdown_sector,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    card_sensor = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AIR, color=ft.Colors.CYAN_300),
                        ft.Text("Sensor de Gas / Humo (GPIO 34 - ADC)", size=16, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(height=10, color=ft.Colors.WHITE12),
                ft.Row([txt_valor_gas, txt_estado_gas], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                barra_gas,
                ft.Text("Simulador Manual de Concentración (Desliza para probar alarma):", size=12, color=ft.Colors.WHITE70),
                slider_gas_manual,
                switch_auto,
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=18,
        border_radius=12,
    )

    card_actuadores = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CAMPAIGN, color=ft.Colors.AMBER_300),
                        ft.Text("Control de Sirena y Actuadores", size=16, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(height=10, color=ft.Colors.WHITE12),
                ft.Row([ft.Text("Estado Sirena:"), badge_sirena], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Relé Potencia (GPIO 15):"), badge_rele], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Señal Buzzer (GPIO 14):"), txt_pwm_actual], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=10, color=ft.Colors.WHITE12),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "ACTIVAR PÁNICO",
                            icon=ft.Icons.WARNING_ROUNDED,
                            bgcolor=ft.Colors.RED_700,
                            color=ft.Colors.WHITE,
                            expand=True,
                            height=45,
                            on_click=lambda _: activar_sirena("Botón de Pánico Manual (Operador)"),
                        ),
                        ft.ElevatedButton(
                            "SILENCIAR",
                            icon=ft.Icons.VOLUME_OFF,
                            bgcolor=ft.Colors.BLUE_GREY_700,
                            color=ft.Colors.WHITE,
                            expand=True,
                            height=45,
                            on_click=silenciar_sirena,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=18,
        border_radius=12,
    )

    card_config = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.TUNE, color=ft.Colors.TEAL_300),
                        ft.Text("Configuración de Parámetros", size=16, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(height=10, color=ft.Colors.WHITE12),
                ft.Row([input_umbral, dropdown_frecuencia], wrap=True, spacing=12),
                txt_error_config,
                ft.ElevatedButton(
                    "Guardar Parámetros",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.TEAL_700,
                    color=ft.Colors.WHITE,
                    on_click=guardar_parametros,
                ),
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=18,
        border_radius=12,
    )

    card_historial = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row([ft.Icon(ft.Icons.HISTORY, color=ft.Colors.PURPLE_300), ft.Text("Historial de Eventos", size=16, weight=ft.FontWeight.BOLD)]),
                        ft.IconButton(ft.Icons.DELETE_SWEEP, tooltip="Limpiar historial", on_click=limpiar_historial),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=10, color=ft.Colors.WHITE12),
                ft.Container(content=lista_historial, height=340),
            ],
            spacing=8,
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=18,
        border_radius=12,
    )

    card_info_tecnica = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.MEMORY, color=ft.Colors.BLUE_300), ft.Text("Arquitectura del Nodo (ESP32)", size=15, weight=ft.FontWeight.BOLD)]),
                ft.Text("• Broker MQTT: broker.hivemq.com", size=12, color=ft.Colors.WHITE70),
                ft.Text("• Tópico Comandos: pueblo/sirena/comando", size=12, color=ft.Colors.WHITE70),
                ft.Text("• Tópico Sensores: pueblo/sirena/sensores", size=12, color=ft.Colors.WHITE70),
                ft.Text("• Pines GPIO: Gas(34) | Botón(12) | Relé(15) | PWM(14)", size=12, color=ft.Colors.WHITE70),
            ],
            spacing=4,
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=16,
        border_radius=12,
    )

    # Ensamblaje de columnas responsivas
    columna_izquierda = ft.Column([card_sensor, card_actuadores, card_config], expand=6, spacing=15)
    columna_derecha = ft.Column([card_historial, card_info_tecnica], expand=5, spacing=15)

    page.add(
        header,
        banner_alarma,
        ft.Row([columna_izquierda, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
    )

    # Evento inicial y arranque del bucle asíncrono
    registrar_evento("Sistema Iniciado", "Interfaz gráfica conectada al simulador local")
    refrescar_vista()
    page.run_task(ciclo_telemetria)


if __name__ == "__main__":
    ft.app(target=main)