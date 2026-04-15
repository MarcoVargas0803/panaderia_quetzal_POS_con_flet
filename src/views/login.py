import flet as ft

class LoginView:
    def __init__(self, navegar_callback):
        self.navegar = navegar_callback
        self.COLOR_MARINO = "#2C3545"

    def build(self):
        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Text("Inicio de Sesión", color="white", weight=ft.FontWeight.BOLD), bgcolor=self.COLOR_MARINO, padding=10, border_radius=5),
                        ft.ElevatedButton("Retroceder >", on_click=lambda _: self.navegar("/"), style=ft.ButtonStyle(bgcolor=self.COLOR_MARINO, color="white"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20,
                    border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Usuario", weight=ft.FontWeight.BOLD, size=16, color=self.COLOR_MARINO),
                        ft.TextField(hint_text="Ingrese su usuario", border_color=self.COLOR_MARINO, width=400),
                        ft.Text("Contraseña", weight=ft.FontWeight.BOLD, size=16, color=self.COLOR_MARINO),
                        ft.TextField(hint_text="Ingrese su contraseña", border_color=self.COLOR_MARINO, width=400, password=True, can_reveal_password=True),
                        ft.Container(height=20),
                        ft.ElevatedButton("Iniciar Sesión", on_click=lambda _: self.navegar("/ventana_principal"), width=200, height=45, style=ft.ButtonStyle(bgcolor=self.COLOR_MARINO, color="white", ))
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    alignment=ft.Alignment(0, 0)
                )
            ],
            bgcolor="white"
        )