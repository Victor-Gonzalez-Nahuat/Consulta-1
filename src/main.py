import os

import flet as ft
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

#INARMA01 CENTRO
#INARMA02 CBETIS

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.title = "Consulta de Producto"
    page.padding = 10

    

    logo = ft.Image(
    src="https://imgs.search.brave.com/IX5-u1cy5OWm_WE9kty0Q1SDUwJzKUriwYx7614BXPE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/cHJlbWl1bS12ZWN0/b3IvdmVjdG9yLWRl/c2lnbi1wb3MtdGVy/bWluYWwtaWNvbi1z/dHlsZV8xMjUwMDA2/LTM4OTc3LmpwZz9z/ZW10PWFpc19oeWJy/aWQmdz03NDA",
    width=60,
    height=60,
    fit=ft.ImageFit.CONTAIN
    )

    titulo_empresa = ft.Column([
        ft.Text(
        "Consulta Movil",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE
    ),
    ft.Text(
        "Punto de Venta",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE
    )
    ])
    titulo = ft.Text("Buscar Producto por Código", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    codigo_input = ft.TextField(label="Código del producto", width=1000, color=ft.colors.WHITE, border_color=ft.colors.WHITE, cursor_color=ft.colors.WHITE)
    nombre_input = ft.TextField(label="Nombre del producto", width=400)

    encabezado = ft.Container(
        content=ft.Column([
            ft.Row([
                logo,
                titulo_empresa
            ]),
            titulo,
            codigo_input
        ]),
        padding=20,
        bgcolor="#77c059",
        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left= 20, bottom_right= 20),  # Esquinas inferiores redondeadas
    )
    resultado_card = ft.Container(
        ft.Row([
            ft.Image(
            src="https://imgs.search.brave.com/IX5-u1cy5OWm_WE9kty0Q1SDUwJzKUriwYx7614BXPE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/cHJlbWl1bS12ZWN0/b3IvdmVjdG9yLWRl/c2lnbi1wb3MtdGVy/bWluYWwtaWNvbi1z/dHlsZV8xMjUwMDA2/LTM4OTc3LmpwZz9z/ZW10PWFpc19oeWJy/aWQmdz03NDA",
            width=250,
            height=250,
            fit=ft.ImageFit.CONTAIN
            )
        ], alignment=ft.MainAxisAlignment.CENTER))

    def formatear_fecha(fecha_str):
        if not fecha_str or len(fecha_str) != 6:
            return "Fecha no válida"
        try:
            anio = int(fecha_str[:2])
            mes = int(fecha_str[2:4])
            dia = int(fecha_str[4:])
            anio += 2000
            return f"{dia:02d}/{mes:02d}/{anio}"
        except:
            return "Fecha inválida"

    def buscar_producto(codigo):

        if not codigo:
            resultado_card.content = ft.Text("⚠️ Por favor, introduce un código válido.", size=16)
            page.update()
            return

        try:
            res = requests.get(API_URL + codigo)
            if res.status_code == 200:
                data_listas = res.json()

                columnas_resultado = []
                encontrado_al_menos_uno = False

                # Iteración sobre los dos resultados
                for indice, producto_data in enumerate(data_listas):

                    nombre_tabla = indice
                    color_fondo = ft.colors.BLUE_GREY_100 if indice == 0 else ft.colors.YELLOW_100

                    # 1. Verificamos si el diccionario NO está vacío ({})
                    if producto_data:
                        encontrado_al_menos_uno = True

                        # ... (Lógica para crear la tarjeta individual para este producto) ...
                        tarjeta_producto = ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("CENTRO" if nombre_tabla == 0 else "CBTIS", size=16, weight=ft.FontWeight.BOLD,
                                            color=ft.colors.BLACK, bgcolor=color_fondo),
                                    ft.Divider(),
                                    ft.Text(f"🛠 Nombre: {producto_data['nombre']}", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"🔢 Código: {producto_data['codigo']}"),
                                    ft.Text(f"📚 Grupo: {producto_data['grupo']}"),
                                    ft.Text(f"🔼 Máximo: {producto_data['maximo']}"),
                                    ft.Text(f"🔽 Mínimo: {producto_data['minimo']}"),
                                    ft.Text(f"💲 Precio: ${producto_data['precio']:.2f}"),
                                    ft.Text(f"📦 Existencia: {producto_data['existencia']}"),
                                    ft.Text(f"🧾 Último costo: ${producto_data['ultimo_costo']:.2f}"),
                                    ft.Text(f"📅 Última venta: {formatear_fecha(producto_data['ultima_venta'])}"),
                                    ft.Text(f"📅 Última compra: {formatear_fecha(producto_data['ultima_compra'])}"),
                                    ft.Text(f"🏭 Proveedor: {producto_data['proveedor']}"),
                                ]),
                                padding=20,
                            ),
                            elevation=4,
                            margin=10
                        )
                        columnas_resultado.append(tarjeta_producto)
                    # Si no se encuentra, añadir mensaje (necesario para la lógica 'else' de abajo)
                    else:
                        columnas_resultado.append(
                            ft.Text(f"⚠️ El código {codigo} NO se encontró en la tabla {nombre_tabla}.",
                                    size=14, color=ft.colors.RED_700, margin=10)
                        )

                # *****************************************************************
                # 👉 LÓGICA DE ASIGNACIÓN Y DIÁLOGO RESTAURADA AQUÍ:
                # *****************************************************************
                if encontrado_al_menos_uno:
                    # Caso 1: Se encontró al menos 1 producto (Muestra las tarjetas/mensajes)
                    resultado_card.content = ft.Column(columnas_resultado, scroll=ft.ScrollMode.AUTO)
                else:
                    # Caso 2: No se encontró NINGÚN producto (resultado fue [{}, {}])
                    resultado_card.content = ft.Text("❌ Producto no encontrado en ninguna tabla.", size=16)

                    # Diálogo de confirmación
                    confirmacion = ft.AlertDialog(title=ft.Text("Código no encontrado"),
                                                  content=ft.Column([
                                                      ft.Text("¿Desea buscar por nombre?"),
                                                      ft.Row([
                                                          ft.ElevatedButton("Si", width=150, height=40,
                                                                            on_click=lambda e: buscar_por_nombre(codigo,
                                                                                                                 confirmacion)),
                                                          ft.ElevatedButton("No", width=150, height=40,
                                                                            on_click=lambda e: page.close(confirmacion))
                                                      ], alignment=ft.MainAxisAlignment.CENTER)
                                                  ], height=80),
                                                  )
                    page.open(confirmacion)
                # *****************************************************************

            else:
                # Manejo de error de la API (status_code != 200)
                resultado_card.content = ft.Text("❌ Producto no encontrado.", size=16)

                # Diálogo de confirmación (tu lógica original para errores de la API)
                confirmacion = ft.AlertDialog(title=ft.Text("Código no encontrado"),
                                              content=ft.Column([
                                                  ft.Text("¿Desea buscar por nombre?"),
                                                  ft.Row([
                                                      ft.ElevatedButton("Si", width=150, height=40,
                                                                        on_click=lambda e: buscar_por_nombre(codigo,
                                                                                                             confirmacion)),
                                                      ft.ElevatedButton("No", width=150, height=40,
                                                                        on_click=lambda e: page.close(confirmacion))
                                                  ], alignment=ft.MainAxisAlignment.CENTER)
                                              ], height=80),
                                              )
                page.open(confirmacion)

        except Exception as ex:
            resultado_card.content = ft.Text(f"🚫 Error al conectar con la API: {str(ex)}", size=16)

        page.update()


    def copiar_al_portapapeles(codigo):
        page.set_clipboard(codigo)
        snack_bar = ft.SnackBar(
        content=ft.Text("✅ Código copiado al portapapeles."),
        bgcolor=ft.colors.GREEN
        )
        page.open(snack_bar)
        page.update()

    def buscar_por_nombre_inmediato(nombre):
        if not nombre.strip():
            resultado_card.content = ft.Text("⚠️ Por favor, introduce un nombre válido.", size=16)
            return

        try:
            res = requests.get(API_URL + f"nombre/{nombre}")
            if res.status_code == 200:
                data_listas_productos = res.json()

                todos_los_productos = []

                for producto in data_listas_productos[0]:
                    producto['origen'] = 'CENTRO'
                    todos_los_productos.append(producto)

                if len(data_listas_productos) > 1:
                    for producto in data_listas_productos[1]:
                        producto['origen'] = 'CBTIS'
                        todos_los_productos.append(producto)

                productos_ordenados = sorted(todos_los_productos, key=lambda p: p['nombre'])

                columnas = []

                for producto in productos_ordenados:
                    tabla_tag = producto['origen']
                    color_fondo = ft.Colors.ORANGE_800 if tabla_tag == "CENTRO" else ft.Colors.YELLOW_800

                    columnas.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"🛠 Nombre: {producto['nombre']}", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f"🔢 Código: {producto['codigo']}"),

                                ft.Text(
                                    tabla_tag,
                                    size=24,
                                    color=ft.Colors.WHITE,
                                    bgcolor=color_fondo,
                                    weight=ft.FontWeight.NORMAL,
                                ),
                                ft.ElevatedButton(
                                    "Seleccionar producto",
                                    icon=ft.icons.SELECT_ALL,
                                    icon_color=ft.colors.WHITE,
                                    width=400,
                                    height=40,
                                    bgcolor=ft.colors.GREEN,
                                    color=ft.colors.WHITE,
                                    # Pasamos el código y el origen si es necesario en buscar_producto
                                    on_click=lambda e, c=producto['codigo']: buscar_producto(c)
                                )
                            ]),
                            padding=10,
                            margin=5,
                            bgcolor=ft.colors.GREY_200,
                            border_radius=10
                        )
                    )

                resultado_card.content = ft.Column(columnas, scroll=ft.ScrollMode.AUTO)

            else:
                resultado_card.content = ft.Text("❌ Producto no encontrado por nombre.", size=16)
        except Exception as ex:
            resultado_card.content = ft.Text(f"🚫 Error al conectar con la API: {str(ex)}", size=16)

        page.update()

    def buscar_por_nombre(nombre, dialog):
        if not nombre.strip():
            resultado_card.content = ft.Text("⚠️ Por favor, introduce un nombre válido.", size=16)
            return

        try:
            res = requests.get(API_URL + f"nombre/{nombre}")
            if res.status_code == 200:
                data_listas_productos = res.json()

                todos_los_productos = []

                for producto in data_listas_productos[0]:
                    producto['origen'] = 'CENTRO'
                    todos_los_productos.append(producto)

                if len(data_listas_productos) > 1:
                    for producto in data_listas_productos[1]:
                        producto['origen'] = 'CBTIS'
                        todos_los_productos.append(producto)

                productos_ordenados = sorted(todos_los_productos, key=lambda p: p['nombre'])

                columnas = []

                for producto in productos_ordenados:
                    tabla_tag = producto['origen']
                    color_fondo = ft.Colors.ORANGE_800 if tabla_tag == "CENTRO" else ft.Colors.YELLOW_800

                    columnas.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"🛠 Nombre: {producto['nombre']}", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f"🔢 Código: {producto['codigo']}"),

                                ft.Text(
                                    tabla_tag,
                                    size=24,
                                    color=ft.Colors.WHITE,
                                    bgcolor=color_fondo,
                                    weight=ft.FontWeight.NORMAL,
                                ),
                                ft.ElevatedButton(
                                    "Seleccionar producto",
                                    icon=ft.icons.SELECT_ALL,
                                    icon_color=ft.colors.WHITE,
                                    width=400,
                                    height=40,
                                    bgcolor=ft.colors.GREEN,
                                    color=ft.colors.WHITE,
                                    # Pasamos el código y el origen si es necesario en buscar_producto
                                    on_click=lambda e, c=producto['codigo']: buscar_producto(c)
                                )
                            ]),
                            padding=10,
                            margin=5,
                            bgcolor=ft.colors.GREY_200,
                            border_radius=10
                        )
                    )

                resultado_card.content = ft.Column(columnas, scroll=ft.ScrollMode.AUTO)

            else:
                resultado_card.content = ft.Text("❌ Producto no encontrado por nombre.", size=16)
        except Exception as ex:
            resultado_card.content = ft.Text(f"🚫 Error al conectar con la API: {str(ex)}", size=16)

        page.close(dialog)
        nombre_input.value = ""
        cerrar_dialogo(dialog)
        page.update()


    def abrir_dialogo(e):
        page.open(dialogo_busqueda)
        page.update()

    def cerrar_dialogo(dialog):
        page.close(dialog)
        page.update()

    botones = ft.Row([
        ft.ElevatedButton("Buscar", on_click=lambda e: buscar_producto(codigo_input.value.strip()), width=180, height=40, icon=ft.icons.SEARCH),
        ft.ElevatedButton("Buscar por nombre", on_click=lambda e: buscar_por_nombre_inmediato(codigo_input.value), width=180, height=40, icon=ft.icons.SEARCH)
    ], alignment=ft.MainAxisAlignment.CENTER)
    dialogo_busqueda = ft.AlertDialog(
        modal=True,
        title=ft.Text("Buscar por nombre"),
        content=ft.Column([
            nombre_input,
            ft.ElevatedButton("Buscar", width=500, height=40, on_click=lambda e: buscar_por_nombre(nombre_input.value, dialogo_busqueda), icon=ft.icons.SEARCH)
        ], tight=True),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo_busqueda))],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.add(
        ft.Column([
            encabezado,
            botones,
            ft.Column([
                resultado_card
            ], scroll=ft.ScrollMode.AUTO, height=400)
        ], spacing=20)
    )

ft.app(target=main)
