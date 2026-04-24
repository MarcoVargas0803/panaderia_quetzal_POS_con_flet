import flet as ft

class ConsultaPagosView:
    def __init__(self, navegar_callback):
        self.navegar = navegar_callback
        
        # Paleta de Colores
        self.COLOR_MARINO = "#2C3545"
        self.COLOR_GRIS_CLARO = "#9BA4B5"
        self.COLOR_FONDO_CARRITO = "#E0E5EC"
        
        # Colores para los Badges (Aproximación a tu Figma)
        self.COLOR_NARANJA = "#F6921E" 
        self.COLOR_VERDE = "#2ECC71"

    # --- COMPONENTES REUTILIZABLES ---
    def btn_oscuro(self, texto, expand=0,on_click=None):
        return ft.Button(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), 
            style=ft.ButtonStyle(
                bgcolor=self.COLOR_MARINO, 
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            expand=expand,
            on_click=on_click
        )

    def btn_blanco(self, texto, expand=0, icon=None,on_click=None):
        return ft.Button(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), 
            icon=icon,
            style=ft.ButtonStyle(
                color=self.COLOR_MARINO,
                side=ft.BorderSide(1, self.COLOR_MARINO),
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            expand=expand,
            on_click=on_click
        )

    # --- HELPERS PARA LA TABLA DINÁMICA ---
    def badge_apartado(self, es_apartado: bool):
        texto = "SI" if es_apartado else "NO"
        color_fondo = self.COLOR_VERDE if es_apartado else self.COLOR_NARANJA
        
        return ft.Container(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
            bgcolor=color_fondo,
            padding=ft.Padding.symmetric(horizontal=15, vertical=5),
            border_radius=15,
            alignment = ft.Alignment(0.0,0.0),
            width=80
        )

    def crear_fila(self, datos: dict):
        # Usamos un diccionario 'datos' para que sea más fácil de manejar
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(datos.get("apartados_id", "")))),
                ft.DataCell(ft.Text(datos.get("cliente", ""))),
                ft.DataCell(ft.Text(datos.get("telefono", ""))),
                # Formateo de moneda para la Panadería
                ft.DataCell(ft.Text(f"${datos.get('total_apartado', 0):.2f}")),
                ft.DataCell(ft.Text(f"${datos.get('total_pagado', 0):.2f}")),
                ft.DataCell(ft.Text(f"${datos.get('saldo_pendiente', 0):.2f}", 
                                    color="red" if datos.get('saldo_pendiente', 0) > 0 else "green")),
                ft.DataCell(ft.Text(str(datos.get("fecha_apartado", "")))),
                ft.DataCell(ft.Text(str(datos.get("fecha_entrega", "")))),
                ft.DataCell(self.badge_apartado(datos.get("es_apartado", False))),
            ]
        )

    def _crear_header(self):
        return ft.Container(
            content=ft.Row([
                self.btn_oscuro("Ventana Principal"),
                # Menú central de navegación
                ft.Row([
                    ft.TextButton("Venta", icon=ft.Icons.SHOPPING_CART, style=ft.ButtonStyle(color=ft.Colors.GREY)),
                    ft.TextButton("Catálogo", icon=ft.Icons.MENU_BOOK, style=ft.ButtonStyle(color=ft.Colors.GREY)),
                    # Consultas está "activo" (marino)
                    ft.TextButton("Consultas", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=self.COLOR_MARINO)),
                ], spacing=20),
                # Botones derechos
                ft.Row([
                    self.btn_blanco("Volver a Venta", on_click=lambda _: self.navegar("/ventana_principal")),
                    self.btn_oscuro("Cerrar Sesión", on_click=lambda _: self.navegar("/"))
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
        )

    def _crear_seccion_titulo(self):
        return ft.Container(
            content=ft.Row([
                ft.Text("Registros de Pagos", size=32, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
                self.btn_blanco("Consultar", icon=ft.Icons.REFRESH)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
        )
    
    def _crear_barra_busqueda(self):
        return ft.Container(
            content=ft.Row([
                ft.TextField(
                    hint_text="Buscar", 
                    prefix_icon=ft.Icons.SEARCH, 
                    border_radius=5, 
                    border_color=self.COLOR_MARINO,
                    height=40,
                    width=250,
                    content_padding=ft.Padding.symmetric(horizontal=10, vertical=0)
                ),
            ], alignment=ft.MainAxisAlignment.END), # Alineado a la derecha como en Figma
            padding=ft.Padding.symmetric(horizontal=20, vertical=10)
        )

    # --- CONSTRUCCIÓN DE LA VISTA ---
    
    def build(self):
        # 1. Componentes (Referencia rápida)
        header = self._crear_header() # Deberías mover la lógica aquí
        titulo = self._crear_seccion_titulo()
        busqueda = self._crear_barra_busqueda()

        # 2. Definición de la Tabla (Una sola vez y bien hecha)
        self.tabla_datos = ft.DataTable(
            heading_row_color=ft.Colors.GREY_200,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Total"), numeric=True),
                ft.DataColumn(ft.Text("Pagado"), numeric=True),
                ft.DataColumn(ft.Text("Saldo"), numeric=True),
                ft.DataColumn(ft.Text("F. Apartado")),
                ft.DataColumn(ft.Text("F. Entrega")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[] # Empezamos vacío para llenar con el Fetch después
        )

        # 3. Datos de prueba (Simulando lo que vendrá de MySQL)
        datos_prueba = [
            {
                "apartados_id": 1, "cliente": "Laura Cajera", "telefono": "2291234567",
                "total_apartado": 100.0, "total_pagado": 40.0, "saldo_pendiente": 60.0,
                "fecha_apartado": "2026-04-20", "fecha_entrega": "2026-04-25", "es_apartado": True
            }
        ]
        
        for d in datos_prueba:
            self.tabla_datos.rows.append(self.crear_fila(d))

        contenedor_tabla = ft.Container(
            content=ft.Column([
                ft.Row([self.tabla_datos], scroll=ft.ScrollMode.ALWAYS)
            ], scroll=ft.ScrollMode.ALWAYS),
            expand=True,
            padding=20
        )

        return ft.View(
            route="/consulta_pagos",
            bgcolor=ft.Colors.WHITE,
            padding=0,
            controls=[header, titulo, busqueda, contenedor_tabla]
        )