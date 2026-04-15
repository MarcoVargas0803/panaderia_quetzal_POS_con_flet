import flet as ft

class ConsultaVentasView:
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
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            border_radius=15,
            alignment = ft.Alignment(0.0,0.0),
            width=80
        )

    def crear_fila(self, folio, fecha, cajero, producto, cantidad, precio, subtotal, es_apartado):
        # Esta función recibe los datos puros (como vendrían de tu fetch de MySQL) y arma la fila.
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(folio))),
                ft.DataCell(ft.Text(fecha)),
                ft.DataCell(ft.Text(cajero)),
                ft.DataCell(ft.Text(producto)),
                ft.DataCell(ft.Text(str(cantidad))),
                ft.DataCell(ft.Text(f"${precio:.2f}")),
                ft.DataCell(ft.Text(f"${subtotal:.2f}")),
                ft.DataCell(self.badge_apartado(es_apartado)),
            ]
        )

    # --- CONSTRUCCIÓN DE LA VISTA ---
    def build(self):
        # 1. HEADER
        header = ft.Container(
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

        # 2. TÍTULO DE LA SECCIÓN
        seccion_titulo = ft.Container(
            content=ft.Row([
                ft.Text("Consulta de Ventas", size=32, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
                self.btn_blanco("Consultar", icon=ft.Icons.REFRESH)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
        )

        # 3. BARRA DE BÚSQUEDA
        barra_busqueda = ft.Container(
            content=ft.Row([
                ft.TextField(
                    hint_text="Buscar", 
                    prefix_icon=ft.Icons.SEARCH, 
                    border_radius=5, 
                    border_color=self.COLOR_MARINO,
                    height=40,
                    width=250,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=0)
                )
            ], alignment=ft.MainAxisAlignment.END), # Alineado a la derecha como en Figma
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )

       # 4. TABLA DE DATOS (Lista para MySQL)
        tabla_ventas = ft.Container(
            content=ft.Row([
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Folio", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Cajero", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("Precio Unitario", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("¿Es apartado?", weight=ft.FontWeight.BOLD)),
                    ],
                    rows=[
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Bolillo", 10, 2.50, 25.00, False),
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Baguette", 1, 10.00, 10.00, False),
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Concha", 1, 8.00, 8.00, False),
                        self.crear_fila(2, "2026-03-18 14:27:21", "Marco A. Vargas Valle", "Borracho", 10, 12.00, 120.00, True),
                        self.crear_fila(3, "2026-03-18 14:27:21", "Marco A. Vargas Valle", "Ojo de Pancha", 1, 10.00, 10.00, True),
                    ],
                    heading_row_color=ft.Colors.GREY_200,
                )
            ], scroll=ft.ScrollMode.AUTO, expand=True), # El Row envuelve la tabla para el scroll horizontal
            padding=ft.padding.symmetric(horizontal=20),
            expand=True
        )
        
        # Ajuste para que la tabla esté dentro del Row con scroll
        tabla_ventas.content.controls.append(tabla_ventas.content) # Reasignación segura
        tabla_ventas = ft.Container(
            content=ft.Row([
                ft.DataTable(
                    # ... (Misma configuración de arriba)
                    columns=[
                        ft.DataColumn(ft.Text("Folio", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Cajero", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("Precio Unitario", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD), numeric=True),
                        ft.DataColumn(ft.Text("¿Es apartado?", weight=ft.FontWeight.BOLD)),
                    ],
                    rows=[
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Bolillo", 10, 2.50, 25.00, False),
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Baguette", 1, 10.00, 10.00, False),
                        self.crear_fila(1, "2026-03-18 14:27:21", "Laura Cajera", "Concha", 1, 8.00, 8.00, False),
                        self.crear_fila(2, "2026-03-18 14:27:21", "Marco A. Vargas Valle", "Borracho", 10, 12.00, 120.00, True),
                        self.crear_fila(3, "2026-03-18 14:27:21", "Marco A. Vargas Valle", "Ojo de Pancha", 1, 10.00, 10.00, True),
                    ],
                    heading_row_color=ft.Colors.GREY_200,
                )
            ], scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.symmetric(horizontal=20),
            expand=True
        )

        # ENSAMBLE FINAL
        return ft.View(
            route="/consulta_ventas",
            bgcolor=ft.Colors.WHITE,
            padding=0,
            controls=[
                header,
                seccion_titulo,
                barra_busqueda,
                tabla_ventas
            ]
        )