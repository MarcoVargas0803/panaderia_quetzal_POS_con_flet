import flet as ft

def main(page: ft.Page):
    # --- Configuración general de la ventana ---
    page.title = "Punto de Venta - Panadería Quetzal"
    page.window_width = 1000
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    COLOR_MARINO = "#2C3545"

    def navegar(ruta):
        page.route = ruta
        # Forzamos la ejecución de la lógica de enrutamiento
        route_change(None)
        page.update()

    def route_change(e):
        page.views.clear()

        # ---------------------------------------------------------
        # PANTALLA 1: INICIO (/)
        # ---------------------------------------------------------
        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Text("Panadería Quetzal POS V.1.0.", color="white", weight=ft.FontWeight.BOLD), bgcolor=COLOR_MARINO, padding=10, border_radius=5),
                                ft.Row([
                                    # Flet 0.80+: Se usa style=ft.ButtonStyle() en lugar de propiedades directas de color
                                    ft.OutlinedButton("Iniciar Sesión", on_click=lambda _: navegar("/login"), style=ft.ButtonStyle(color=COLOR_MARINO)),
                                    ft.ElevatedButton("Registrarse", on_click=lambda _: navegar("/register"), style=ft.ButtonStyle(bgcolor=COLOR_MARINO, color="white"))
                                ])
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=20,
                            # Flet 0.80+: ft.Border.only y ft.BorderSide
                            border=ft.Border.only(bottom=ft.BorderSide(2, COLOR_MARINO))
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Text("PANADERÍA QUETZAL", size=50, weight=ft.FontWeight.BOLD, color="black"),
                                # Flet 0.80+: Se usa el texto "contain" o ft.BoxFit.CONTAIN en lugar de ImageFit
                                ft.Image(src="assets/icon.png", width=300, height=300, fit="contain")
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=50),
                            expand=True,
                            alignment=ft.Alignment(0, 0)
                        ),
                        ft.Container(
                            content=ft.Text("Panadería Quetzal POS V. 1.0", weight=ft.FontWeight.BOLD, color="black"),
                            alignment=ft.Alignment(0, 0),
                            padding=20
                        )
                    ],
                    bgcolor="white"
                )
            )

        # ---------------------------------------------------------
        # PANTALLA 2: INICIO DE SESIÓN (/login)
        # ---------------------------------------------------------
        elif page.route == "/login":
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Text("Inicio de Sesión", color="white", weight=ft.FontWeight.BOLD), bgcolor=COLOR_MARINO, padding=10, border_radius=5),
                                ft.ElevatedButton("Retroceder >", on_click=lambda _: navegar("/"), style=ft.ButtonStyle(bgcolor=COLOR_MARINO, color="white"))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=20,
                            border=ft.Border.only(bottom=ft.BorderSide(2, COLOR_MARINO))
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Usuario", weight=ft.FontWeight.BOLD, size=16, color=COLOR_MARINO),
                                ft.TextField(hint_text="Ingrese su usuario", border_color=COLOR_MARINO, width=400),
                                ft.Text("Contraseña", weight=ft.FontWeight.BOLD, size=16, color=COLOR_MARINO),
                                ft.TextField(hint_text="Ingrese su contraseña", border_color=COLOR_MARINO, width=400, password=True, can_reveal_password=True),
                                ft.Container(height=20),
                                ft.ElevatedButton("Iniciar Sesión", width=200, height=45, style=ft.ButtonStyle(bgcolor=COLOR_MARINO, color="white"))
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            alignment=ft.Alignment(0, 0)
                        )
                    ],
                    bgcolor="white"
                )
            )

        # ---------------------------------------------------------
        # PANTALLA 3: REGISTRO (/register)
        # ---------------------------------------------------------
        elif page.route == "/register":
            page.views.append(
                ft.View(
                    route="/register",
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Text("Registrar Usuario", color="white", weight=ft.FontWeight.BOLD), bgcolor=COLOR_MARINO, padding=10, border_radius=5),
                                ft.ElevatedButton("Retroceder >", on_click=lambda _: navegar("/"), style=ft.ButtonStyle(bgcolor=COLOR_MARINO, color="white"))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=20,
                            border=ft.Border.only(bottom=ft.BorderSide(2, COLOR_MARINO))
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Nombre", weight=ft.FontWeight.BOLD, size=16, color=COLOR_MARINO),
                                ft.TextField(hint_text="Ingrese su nombre", border_color=COLOR_MARINO, width=400),
                                ft.Text("Contraseña", weight=ft.FontWeight.BOLD, size=16, color=COLOR_MARINO),
                                ft.TextField(hint_text="Ingrese su contraseña", border_color=COLOR_MARINO, width=400, password=True, can_reveal_password=True),
                                ft.Text("Mínimo al menos 8 caracteres, una mayúscula y un carácter especial (#,@, %...).", size=11, color="black"),
                                ft.Text("Rol", weight=ft.FontWeight.BOLD, size=16, color=COLOR_MARINO),
                                ft.Dropdown(
                                    hint_text="Seleccionar rol...",
                                    border_color=COLOR_MARINO,
                                    width=400,
                                    options=[
                                        ft.dropdown.Option("Administrador"),
                                        ft.dropdown.Option("Cajero"),
                                        ft.dropdown.Option("Panadero"),
                                    ]
                                ),
                                ft.Container(height=20),
                                ft.ElevatedButton("Registrar Usuario", width=200, height=45, style=ft.ButtonStyle(bgcolor=COLOR_MARINO, color="white"))
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
                            expand=True,
                            alignment=ft.Alignment(0, 0)
                        )
                    ],
                    bgcolor="white"
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        navegar(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.route = "/"
    route_change(None)

if __name__ == '__main__':
    ft.run(main)
