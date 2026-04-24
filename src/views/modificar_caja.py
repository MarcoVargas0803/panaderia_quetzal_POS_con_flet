import flet as ft
#Fetch para la Base de Datos.
from Backend.fetch import Fetch_Panes_Dulces, Fetch_Panes_Especiales, Fetch_Panes_Salados

import datetime

class ModificarCajaView:
    def __init__(self, navegar_callback):
        self.navegar = navegar_callback
        

        # Paleta de Colores
        self.COLOR_MARINO = "#2C3545"
        self.COLOR_GRIS_CLARO = "#9BA4B5"
        self.COLOR_FONDO_CARRITO = "#E0E5EC"
        self.COLOR_ITEM_CARRITO = "#768296"

        # ESTADO: ¿Qué categoría está activa?
        self.categoria_actual = "Salados" 

        # ESTADO: ¿Qué categoría está activa?
        self.categoria_actual = "Salados" 

        # ESTADO: ¿Qué tipo de pago está activo?
        self.pago_actual = "Efectivo"

        #ESTADO del carrito
        self.carrito = {}
        
        # REFERENCIAS del grid de productos
        self.grid_productos = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=160,
            child_aspect_ratio=0.8,
            spacing=15,
            run_spacing=15,
        )
        
        #Definir fila de categorias para selección
        self.row_categorias = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)
        
        #Definir fila de categorias para selección
        self.row_tipo_pagos = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)

        # REFERENCIAS del los items del carrito
        self.columna_items_carrito = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=5)




    # --- COMPONENTES REUTILIZABLES ---
    def btn_oscuro(self, texto, expand=0, on_click=None, icon=None):
        return ft.Button(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            icon=icon, 
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
   
    #Container secundario del texto y el monto.
    def container_monto(self, texto: str, variable: ft.Text):
        return ft.Container(
            #Configuración
            padding=20,
            border_radius=15,

            content=
                ft.Row([
                    #Ejemplo: Subtotal.
                    ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, size=20,expand=True),
                    #Ejemplo: $50.00
                    #Realizamos un container para poder agregar el ft.Text "Variable".
                    ft.Container(
                        padding= 0,
                        content=variable
                    )
                ])

        )

   #Barra de busqueda general
    #Habria que buscar como se realiza un fetch para rellenar los datos de clientes.
    def Barra_busqueda(self) -> ft.Column:
        async def close_anchor(e):
            text = f"Color {e.control.data}"
            print(f"closing view from {text}")
            await anchor.close_view(text)

        async def open_anchor(e):
            await anchor.open_view()

        def handle_change(e):
            print(f"handle_change e.data: {e.data}")

        def handle_submit(e):
            print(f"handle_submit e.data: {e.data}")

        anchor = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search colors...",
            view_hint_text="Choose a color from the suggestions...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=open_anchor,
            controls=[
                #Reemplazar para agregar el fetch a la lista de clientes
                #Fetch debería de volver lista con solo el nombre, aunque podría verse para incluir otras datos.
                #Checar si tiene autocompletado para poder manejarlo
                ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
                for i in range(10)
            ],
        )

        return ft.Column(
            controls=[
                anchor,
            ],
        )

   # -- Logica Mensaje Señal General -- #
    def modal_mensaje(self, mensaje: str):
        ft.context.page.show_dialog(
            
            ft.AlertDialog(
                modal=False,
                title=ft.Text(mensaje), on_dismiss=lambda e: print("Ticket impreso..")
        )
        )

    #Agarrador de Fecha
    def agarrarFecha(self):

        # 1. Definimos una referencia para el texto que mostrará la fecha
        self.texto_fecha_display = ft.Text(
            value=f"Selected date: {datetime.datetime.now().strftime('%Y-%m-%d')}",
            size=16
        )

        # 2. Función que se ejecuta cuando el usuario elige una fecha
        def on_date_change(e):
            if e.control.value:
                # Actualizamos el valor del texto con la nueva fecha
                self.texto_fecha_display.value = f"Selected date: {e.control.value.strftime('%Y-%m-%d')}"
                self.texto_fecha_display.update()
                print(f"Fecha guardada: {e.control.value}") # Para tu debug
        
        # 3. Creamos el DatePicker
        date_picker = ft.DatePicker(
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2026, 12, 1),
            on_change=on_date_change,
        )

        return ft.Column(
            controls=[
                ft.Button(
                    "Pick date",
                    icon=ft.Icons.CALENDAR_MONTH,
                    # En Flet moderno, usamos pick_date() para abrirlo
                    on_click=lambda _: date_picker.pick_date(),
                ),
                self.texto_fecha_display,
                date_picker # Importante: debe estar en el árbol
            ]
        )
    def detalle_saldo(self, mensaje: str, variable = None):
        return ft.Container(
            content=ft.Column([
                ft.Text(mensaje, weight=ft.FontWeight.BOLD, size= 18, color="black"),
                ft.Text(self.text_subtotal.value, size=16, color="black"),
            ]), bgcolor=self.COLOR_GRIS_CLARO, padding=10, border_radius=15
        )
        
   # --- Modal para imprimir ticket --- 
    def modal_imprimir_ticket(self, e):
        # Usamos ft.context.page para mostrar el diálogo directamente
        ft.context.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                expand=True,
                title=ft.Text("Venta (fetch)", weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
                content=ft.Column(
                    tight=True,
                    spacing=5,
                    controls=[

                        ft.Container(
                            content=ft.Column([
                                ft.Text("Caja 1", weight=ft.FontWeight.BOLD, size= 18, color="black"),
                                ft.Text("Caja a Cargo de: Marco A. Vargas Valle (fetch)", size=16, color="black"),
                            ], spacing=2, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),

                        ft.Container(
                            content=ft.Row([
                                self.detalle_saldo("Saldo de Apertura"),
                                self.detalle_saldo("Saldo de Cierre"),
                                self.detalle_saldo("Fecha de Apertura"),
                                self.detalle_saldo("Monto Total de Caja"),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=20,
                            border_radius=15,

                        ),

                        ft.Text("Faltante", weight=ft.FontWeight.BOLD, color="black"),
                        ft.Container(
                            content=ft.Row([
                                ft.Text(self.text_total.value, size=24, weight=ft.FontWeight.BOLD, color="black"),
                                ft.Text("calculado automáticamente", size=16, color="black54"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),
                    ],
                ),
                actions=
                    ft.Column(
                        controls=[
                            #Provisional
                            ft.Button(content="Confirmar Corte de Día"+" - "+self.text_total.value,expand=True, icon=ft.Icons.MONEY, on_click= lambda _: ft.context.page.pop_dialog()), 
                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.Button(content="Imprimir Ticket", icon=ft.Icons.PRINT ,on_click=lambda _: self.modal_mensaje("Ticket impreso!"),expand=True)
                           
                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    #Modal para "Registrar Cliente"
    def modal_registrar_cliente(self):
        # Usamos ft.context.page para mostrar el diálogo directamente
        ft.context.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                expand=True,
                title=ft.Text("Registrar Cliente", weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
                content=ft.Column(
                    tight=True,
                    spacing=15,
                    controls=[

                        #Anticipo
                        ft.TextField(
                            label="Nombre del Cliente",
                        ),

                        ft.TextField(
                            label="Teléfono del Cliente",
                        ),

                    ],
                ),
                actions=
                    ft.Column(
                        controls=[

                            #Confirmar Registrar Cliente 
                            ft.TextButton(
                            "Registrar Cliente", 
                            #Realizar inserción para el cliente.
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),

                        #Cancelar
                            ft.TextButton(
                            "Cancelar", 
                            #Realizar inserción de apartado.
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),

                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.START,
            )
        )
    
    
    #Modal para "Realizar apartado"
    def modal_realizar_apartado(self, e):
        # Usamos ft.context.page para mostrar el diálogo directamente
        ft.context.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                expand=True,
                title=ft.Text("Realizar Apartado", weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),
                content=ft.Column(
                    tight=True,
                    spacing=15,
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                #Va a la ventana "Registrar Cliente"
                                ft.TextButton("¿No está registrado? Registrar Cliente.", on_click=lambda _: self.modal_registrar_cliente()),
                            ], alignment=ft.MainAxisAlignment.START, spacing=50, expand=True),
                        ),

                        self.Barra_busqueda(),

                        ft.Container(
                            content=ft.Row([
                                ft.Text("monto total del apartado", size=16, color="black54"),
                                ft.Text(self.text_total.value, size=24, weight=ft.FontWeight.BOLD, color="black"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),

                        ft.Container(
                            content=ft.Row([
                                ft.Text("pago minimo para apartar(20%)", size=16, color="black54"),
                                #Realizar otra variable que calcule el 20% del valor total.
                                ft.Text(self.text_total.value, size=24, weight=ft.FontWeight.BOLD, color="black"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),

                        #Fecha
                        self.agarrarFecha(),
                        #Anticipo
                        ft.TextField(
                            label="Monto del apartado",
                        ),

                         ft.Container(
                            content=ft.Row([
                                ft.Text("Monto restante para finiquitar apartado", size=16, color="black54"),
                                #Realizar otra variable que calcule el restante a pagar de #self.text_total.value).
                                ft.Text(self.text_total.value, size=24, weight=ft.FontWeight.BOLD, color="black"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),

                    ],
                ),
                actions=
                    ft.Column(
                        controls=[

                            #Confirmar Monto a Pagar 
                            ft.TextButton(
                            "Confirmar Apartado", 
                            #Realizar inserción de apartado.
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),
                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Imprimir Ticket", 
                            on_click=lambda _: self.modal_mensaje("Ticket impreso!")
                        ),

                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    def text_box_container(self, texto):
                return ft.Container(
                content=ft.Column([
                    ft.TextField(label=texto),
                    self.btn_oscuro("Confirmar",expand=True)
                ]),
                border=ft.Border.all(width=2,color=self.COLOR_MARINO),
                border_radius=5,
                padding=20,
            )


    # --- CONSTRUCCIÓN DE LA VISTA ---
    def build(self):

        #Variables de actualización para subtotal y total de carrito.
        self.text_subtotal = ft.Text("$0.00", weight=ft.FontWeight.BOLD, expand=True, size=18)
        self.text_total = ft.Text("$0.00", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO, expand=True)

        # 1. HEADER (Navegación principal)
        header = ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Text("Ventana Principal", color="white", weight=ft.FontWeight.BOLD), bgcolor=self.COLOR_MARINO, padding=10, border_radius=5),
                
                ft.Row([
                    ft.TextButton("Venta", icon=ft.Icons.SHOPPING_CART_SHARP, style=ft.ButtonStyle(color=self.COLOR_MARINO), disabled=False),
                    ft.TextButton("Producción", icon=ft.Icons.BAKERY_DINING , style=ft.ButtonStyle(color=ft.Colors.GREY),disabled=False),
                    ft.TextButton("Consultas", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=ft.Colors.GREY),disabled=False),
                ], spacing=20),

                ft.Row([
                    self.btn_oscuro("Volver a Venta", on_click=lambda _: self.navegar("/ventana_principal"),icon=ft.Icons.ARROW_BACK_IOS),
                self.btn_blanco("Cerrar Sesión", on_click=lambda _: self.navegar("/"))
                ],alignment= ft.MainAxisAlignment.END),
                
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO))
        )

        # 2. SECCIÓN DE ACCIONES DE VENTA
        acciones_caja = ft.Container(
            content=ft.Row([
                ft.Text("Caja", size=28, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO, expand=True),
                
                ft.Row([
                    self.Barra_busqueda(),
                    # Botón que dispara el modal
                    self.btn_blanco("Imprimir Ticket",  expand=True, icon=ft.Icons.PRINT, on_click=self.modal_imprimir_ticket )
                ],alignment= ft.MainAxisAlignment.END),

                ft.Row([
                    #El botón de modificar caja es un botón que se puede desactivar o activar, con el fin de permitir la modificación o no.
                    self.btn_oscuro("Modificar Caja"),
                    self.btn_oscuro("Realizar Corte",on_click=self.modal_imprimir_ticket)
                ],alignment= ft.MainAxisAlignment.END),

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.Border.only(bottom=ft.BorderSide(2, self.COLOR_MARINO)),
            padding=ft.Padding.symmetric(horizontal=15, vertical=10)
        )



        # 3. MÉTODOS DE PAGO Y BOTONES FINALES}

        # 4. PANEL IZQUIERDO (Categorías y Productos)


        text_box_saldos = ft.Container(
            #Contenedor principal (Fila)
            content=ft.Row([

                self.text_box_container("Saldo de Apertura"),
                self.text_box_container("Saldo de Cierre"),
                self.text_box_container("Fecha de Apertura"),
                self.text_box_container("Fecha de Cierre"),
            ],alignment=ft.MainAxisAlignment.CENTER),
            padding=15,
        )

        # 5. PANEL DERECHO (Detalle de Venta)
        detalle_caja = ft.Container(
            content=ft.Column([
                ft.Text("Detalle de Caja", size=28, weight=ft.FontWeight.BOLD, color=self.COLOR_MARINO),

                ft.Container(
                    content=ft.Column([
                        #De manera provisional estan self.text_subtotal y self.text_total.
                        self.container_monto("Saldo de Apertura Confirmado", self.text_subtotal),
                        self.container_monto("Saldo de Cierre Confirmado", self.text_total),
                        self.container_monto("Ingresos Totales del sistema", self.text_total),
                        self.container_monto("Monto Total de la Caja (Saldo de Apertura + Ingresos Totales)", self.text_total),
                    ]), bgcolor=self.COLOR_GRIS_CLARO, border_radius=15
                ),

                ft.Container(
                    content=ft.Column([
                        #De manera provisional esta self.text_total.
                       self.container_monto("Faltante de Caja", self.text_total)

                    ]), bgcolor=self.COLOR_GRIS_CLARO, border_radius=15
                ),
            ]),
            padding=15,
            border_radius=15,
           
        )

        # ENSAMBLE FINAL
        return ft.View(
            route="/caja",
            bgcolor=ft.Colors.WHITE,
            padding=0,
            controls=[
                header,
                acciones_caja,
                text_box_saldos,
                detalle_caja
                    
               
            ]
        )