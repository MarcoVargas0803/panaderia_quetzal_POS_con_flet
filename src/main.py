import flet as ft
from views.inicio import InicioView
from views.login import LoginView
from views.registro import RegistroView
from views.ventana_principal import PrincipalView
from views.consulta_ventas import ConsultaVentasView
from views.ventana_principal_produccion import PrincipalProduccionView
from views.ventana_principal_consultas import PrincipalConsultasView
class App:
    def __init__(self, page: ft.Page):
        self.page = page

        # Configurar la página
        self.page.title = "Punto de Venta - Panadería Quetzal"
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0

        # Instancias de vistas
        self.inicio_view = InicioView(self.navegar)
        self.login_view = LoginView(self.navegar)
        self.registro_view = RegistroView(self.navegar)
        self.principal_view = PrincipalView(self.navegar)
        self.consulta_ventas_view = ConsultaVentasView(self.navegar)
        self.ventana_principal_produccion = PrincipalProduccionView(self.navegar)
        self.ventana_principal_consultas = PrincipalConsultasView(self.navegar)

        # Configurar eventos
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        # Iniciar en /
        self.page.route = "/"
        self.route_change(None)

    def navegar(self, ruta):
        self.page.route = ruta
        self.route_change(None)
        self.page.update()

    def route_change(self, e):
        self.page.views.clear()

        if self.page.route == "/":
            self.page.views.append(self.inicio_view.build())
        elif self.page.route == "/login":
            self.page.views.append(self.login_view.build())
        elif self.page.route == "/register":
            self.page.views.append(self.registro_view.build())
        elif self.page.route == "/ventana_principal":
            self.page.views.append(self.principal_view.build())
        elif self.page.route == "/consulta_ventas":
            self.page.views.append(self.consulta_ventas_view.build())
        elif self.page.route == "/ventana_principal_produccion":
            self.page.views.append(self.ventana_principal_produccion.build())
        elif self.page.route == "/ventana_principal_consultas":
            self.page.views.append(self.ventana_principal_consultas.build())
        
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.navegar(top_view.route)

def main(page: ft.Page):
    app = App(page)

if __name__ == '__main__':
    ft.run(main)
