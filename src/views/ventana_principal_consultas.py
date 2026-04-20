import flet as ft

class PrincipalConsultasView:
    def __init__(self, navegar_callback):
        self.navegar = navegar_callback
        
        # Paleta de Colores
        self.COLOR_MARINO = "#2C3545"
        self.COLOR_GRIS_CLARO = "#9BA4B5"
        self.COLOR_FONDO_CARRITO = "#E0E5EC"
        self.COLOR_ITEM_CARRITO = "#768296"

    # --- COMPONENTES REUTILIZABLES ---
    def btn_oscuro(self, texto, expand=0, on_click=None):
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

    def btn_blanco(self, texto, expand=0, icon=None, on_click=None):
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

    def categoria_pill(self, texto):
        return ft.Container(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
            bgcolor=self.COLOR_GRIS_CLARO,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border_radius=15,
        )

    def tarjeta_producto(self, titulo, precio, url_imagen="https://picsum.photos/150/100"):
        return ft.Container(
            content=ft.Column([
                # Placeholder de imagen
                ft.Image(src=url_imagen, width=150, height=100, fit=1, border_radius=ft.border_radius.only(top_left=10, top_right=10)),
                ft.Container(
                    content=ft.Column([
                        ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16, color=self.COLOR_MARINO),
                        ft.Text(f"${precio:.2f}", size=14, color=self.COLOR_MARINO)
                    ], spacing=2),
                    padding=10
                )
            ], spacing=0),
            bgcolor=self.COLOR_FONDO_CARRITO,
            border_radius=10,
            width=150,
        )

    def item_carrito(self, titulo, precio, cantidad):
        return ft.Container(
            content=ft.Row([
                ft.Container(width=50, height=40, bgcolor=ft.Colors.BLUE_200, border_radius=5), # Placeholder imagen pequeña
                ft.Column([
                    ft.Text(titulo, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=14),
                    ft.Text(f"${precio:.2f}", color=ft.Colors.WHITE70, size=12)
                ], expand=True, spacing=0),
                ft.Text(f"x{cantidad}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ]),
            bgcolor=self.COLOR_ITEM_CARRITO,
            padding=10,
            border_radius=10,
            margin=ft.margin.only(bottom=5)
        )

    # --- CONSTRUCCIÓN DE LA VISTA ---
    def build(self):
        # 1. HEADER (Navegación principal)
        header = ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Text("Ventana Principal", color="white", weight=ft.FontWeight.BOLD), bgcolor=self.COLOR_MARINO, padding=10, border_radius=5),
                ft.Row([
                    ft.TextButton("Venta", icon=ft.Icons.SHOPPING_CART_SHARP, on_click=lambda _: self.navegar("/ventana_principal") , style=ft.ButtonStyle(color=ft.Colors.GREY)),
                    ft.TextButton("Producción", icon=ft.Icons.BAKERY_DINING,on_click=lambda _: self.navegar("/ventana_principal_produccion") , style=ft.ButtonStyle(color=ft.Colors.GREY)),
                    ft.TextButton("Consultas", icon=ft.Icons.SEARCH,style=ft.ButtonStyle(color=self.COLOR_MARINO)),
                ], spacing=20),
                self.btn_blanco("Cerrar Sesión",on_click=lambda _: self.navegar("/"))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
        )

        # 2. SECCIÓN DE ACCIONES DE VENTA
        acciones_venta = ft.Container(
            content=ft.Row([
                ft.Text("Venta", size=28, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO, expand=True),
                self.btn_oscuro("Consultar Ventas",on_click=lambda _: self.navegar("/consulta_ventas")),
                self.btn_oscuro("Pagos"),
                self.btn_blanco("Modificar Caja"),
                self.btn_oscuro("Realizar Corte")
            ]),
            padding=ft.padding.symmetric(horizontal=15, vertical=10)
        )

        # 3. MÉTODOS DE PAGO Y BOTONES FINALES
        metodos_pago = ft.Container(
            content=ft.Row([
                self.btn_oscuro("Efectivo", expand=1),
                self.btn_oscuro("Tarjeta", expand=1),
                self.btn_oscuro("Transferencia", expand=1),
                self.btn_blanco("Crear como apartado", expand=1, icon=ft.Icons.STAR_BORDER),
                self.btn_blanco("Imprimir Ticket", expand=1, icon=ft.Icons.PRINT),
                self.btn_blanco("Finalizar Venta", expand=1, icon=ft.Icons.CHECK)
            ], spacing=10),
            padding=ft.padding.symmetric(horizontal=15, vertical=5)
        )

        # 4. PANEL IZQUIERDO (Categorías y Productos)
        panel_izquierdo = ft.Container(
            content=ft.Column([
                # Categorías
                ft.Row([
                    self.categoria_pill("Salados"),
                    self.categoria_pill("Salados"),
                    self.categoria_pill("Salados"),
                    self.categoria_pill("Salados"),
                    self.categoria_pill("Salados"),
                ], scroll=ft.ScrollMode.AUTO),
                ft.Divider(color=self.COLOR_MARINO),
                # Grid de Panes
                ft.GridView(
                    expand=True,
                    runs_count=5,
                    max_extent=160,
                    child_aspect_ratio=0.8,
                    spacing=15,
                    run_spacing=15,
                    controls=[
                        self.tarjeta_producto("Concha", 25.00),
                        self.tarjeta_producto("Concha", 25.00),
                        self.tarjeta_producto("Concha", 25.00),
                        self.tarjeta_producto("Concha", 25.00),
                        self.tarjeta_producto("Concha", 25.00),
                        self.tarjeta_producto("Concha", 25.00),
                    ]
                )
            ]),
            expand=7, # Ocupa el 70% del ancho
            padding=15
        )

        # 5. PANEL DERECHO (Detalle de Venta)
        panel_derecho = ft.Container(
            content=ft.Column([
                # Lista de items en el carrito
                ft.Container(
                    content=ft.Column([
                        self.item_carrito("Concha", 25.00, 2),
                        self.item_carrito("Concha", 25.00, 2),
                        self.item_carrito("Concha", 25.00, 2),
                        self.item_carrito("Concha", 25.00, 2),
                    ], scroll=ft.ScrollMode.AUTO),
                    expand=True,
                ),
                # Resumen (Subtotal, Impuestos, etc)
                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Text("Subtotal", weight=ft.FontWeight.BOLD), ft.Text("$25.00", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Impuestos I.V.A.", weight=ft.FontWeight.BOLD), ft.Text("$0.00", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Descuento", weight=ft.FontWeight.BOLD), ft.Text("$0.00", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ]),
                    bgcolor=self.COLOR_FONDO_CARRITO,
                    padding=15,
                    border_radius=10,
                    margin=ft.margin.only(top=10, bottom=10)
                ),
                # Total
                ft.Container(
                    content=ft.Row([
                        ft.Text("Total", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO), 
                        ft.Text("$25.00", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=self.COLOR_FONDO_CARRITO,
                    padding=15,
                    border_radius=10
                )
            ]),
            expand=3, # Ocupa el 30% del ancho
            padding=15,
            border=ft.Border.only(left=ft.BorderSide(2, self.COLOR_FONDO_CARRITO))
        )

        # ENSAMBLE FINAL
        return ft.View(
            route="/ventana_principal_consultas",
            bgcolor=ft.Colors.WHITE,
            padding=0,
            controls=[
                header,
                acciones_venta,
                metodos_pago,
                # Contenedor principal que divide pantalla en Izquierda y Derecha
                ft.Container(
                    content=ft.Row([
                        panel_izquierdo,
                        panel_derecho
                    ], vertical_alignment=ft.CrossAxisAlignment.START, expand=True),
                    expand=True
                )
            ]
        )