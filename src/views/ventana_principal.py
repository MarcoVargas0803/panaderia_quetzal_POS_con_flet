import flet as ft
#Fetch para la Base de Datos.
from Backend.fetch import Fetch_Panes_Dulces, Fetch_Panes_Especiales, Fetch_Panes_Salados

import datetime

class PrincipalView:
    def __init__(self, navegar_callback):
        self.navegar = navegar_callback
        
        # Paleta de Colores
        self.COLOR_MARINO = "#2C3545"
        self.COLOR_GRIS_CLARO = "#9BA4B5"
        self.COLOR_FONDO_CARRITO = "#E0E5EC"
        self.COLOR_ITEM_CARRITO = "#768296"

        #Listas vacias para los fetch: 4. PANEL IZQUIERDO (Categorías y Productos)
        self.Lista_categorias = []
        self.Lista_tarjetas = []
        self.Lista_items_carrito = []

        #Lista vacia para los fetch: 5. PANEL DERECHO (Detalle de Venta)
        self.Lista_panes_dulces = []
        self.Lista_panes_salados = []
        self.Lista_panes_especiales = []

        # ESTADO: ¿Qué categoría está activa?
        self.categoria_actual = "Salados" 

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
        
        self.row_categorias = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)

        # REFERENCIAS del los items del carrito
        self.columna_items_carrito = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=5)




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
        # ¿Este botón es el seleccionado?
        es_activo = self.categoria_actual == texto
        
        return ft.Container(
            content=ft.Text(
                texto, 
                weight=ft.FontWeight.BOLD, 
                color=ft.Colors.WHITE if es_activo else self.COLOR_MARINO
            ),
            bgcolor=self.COLOR_MARINO if es_activo else self.COLOR_GRIS_CLARO,
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            border_radius=15,
            on_click=self.click_categoria,
            data=texto # Guardamos el nombre aquí para saber cuál se presionó
        )


    def tarjetas_productos(self, lista_datos, url_imagen="../assets/Concha.png"):
        #Lista para guardar tarjetas
        lista_tarjetas_fetch = []
        for pan in lista_datos:
            tarjeta_pan = ft.Container(
                content=ft.Column([
                    # Placeholder de imagen
                    ft.Image(src=url_imagen, width=150, height=100, fit=1, border_radius=ft.BorderRadius.only(top_left=10, top_right=10)),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(pan["nombre"], weight=ft.FontWeight.BOLD, size=16, color=self.COLOR_MARINO),
                            ft.Text(f"${pan["precio"]:.2f}", size=14, color=self.COLOR_MARINO)
                        ], spacing=2),
                       
                        padding=10
                    )
                ], spacing=0),
                bgcolor=self.COLOR_FONDO_CARRITO,
                border_radius=10,
                width=150,
                #Función para agregar al carrito.
                on_click=lambda e, p=pan: self.agregar_al_carrito(p),
            )
        # 4. Agregamos esta tarjeta ya diseñada a nuestra lista de controles
            lista_tarjetas_fetch.append(tarjeta_pan)
        
        return lista_tarjetas_fetch
    
    # Operaciones CRUD del carrito.
    def agregar_al_carrito(self, pan):
        nombre = pan["nombre"]
        # Si ya existe, subimos cantidad. Si no, lo creamos.
        if nombre in self.carrito:
            self.carrito[nombre]["cantidad"] += 1
        else:
            self.carrito[nombre] = {"precio": pan["precio"], "cantidad": 1}
        
        self.actualizar_vista_carrito()

    def modificar_cantidad(self, nombre, delta):
        if nombre in self.carrito:
            self.carrito[nombre]["cantidad"] += delta
            # Si llega a cero, lo borramos
            if self.carrito[nombre]["cantidad"] <= 0:
                self.carrito.pop(nombre)
        
        self.actualizar_vista_carrito()

    def borrar_del_carrito(self, nombre):
        if nombre in self.carrito:
            self.carrito.pop(nombre)
        self.actualizar_vista_carrito()

   
    #Container secundario del texto y el monto.
    def container_monto(self, texto: str, variable: ft.Text):
        return ft.Container(
            #Configuración
            padding=20,
            bgcolor=self.COLOR_GRIS_CLARO,
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
    

    def item_carrito(self, nombre, datos):
        return ft.Container(
            content=ft.Row([

                #Imagen 
                ft.Column([
                    ft.Image(src="../assets/Concha.png", fit=1, border_radius=ft.BorderRadius.only(top_left=10, top_right=10)),
                ], expand=True, spacing=0),
                
                
                ft.Column([
                    ft.Text(nombre, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=14),
                    ft.Text(f"${datos['precio']:.2f}", color=ft.Colors.WHITE70, size=12)
                ], expand=True, spacing=0),
                
                # Controles de cantidad
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                        icon_color=ft.Colors.WHITE_70,
                        icon_size=20,
                        on_click=lambda _: self.modificar_cantidad(nombre, -1)
                    ),
                    ft.Text(str(datos["cantidad"]), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                        icon_color=ft.Colors.WHITE_70,
                        icon_size=20,
                        on_click=lambda _: self.modificar_cantidad(nombre, 1)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_300,
                        icon_size=20,
                        on_click=lambda _: self.borrar_del_carrito(nombre)
                    ),
                ], spacing=0)
            ]),
            bgcolor=self.COLOR_ITEM_CARRITO,
            padding=10,
            border_radius=10,
        )
    
    #Actualizar la lista del carrito
    def actualizar_vista_carrito(self):
        # 1. Limpiar lista visual
        self.columna_items_carrito.controls.clear()
        
        total = 0
        
        # 2. Re-dibujar items desde el diccionario 'self.carrito'
        for nombre, datos in self.carrito.items():
            total += datos["precio"] * datos["cantidad"]
            self.columna_items_carrito.controls.append(self.item_carrito(nombre, datos))
        
        # 3. Actualizar los textos de Total en la interfaz
        # (Para esto, necesitas que los textos de subtotal/total también sean self.text_total)
        self.text_subtotal.value = f"${total:.2f}"
        self.text_total.value = f"${total:.2f}"
        
        # 4. Refrescar Flet
        self.columna_items_carrito.update()
        self.text_subtotal.update()
        self.text_total.update()

    # -- Funciones para responsividad -- 

    def click_categoria(self, e):
        # 1. Cambiamos la categoría actual
        self.categoria_actual = e.control.data
            
        # 2. Elegimos qué función de Fetch usar
        if self.categoria_actual == "Salados":
                datos = Fetch_Panes_Salados()
        elif self.categoria_actual == "Dulces":
                datos = Fetch_Panes_Dulces()
        else:
                datos = Fetch_Panes_Especiales()
            
        # 3. Actualizamos el Grid (el asterisco desempaqueta la lista de tarjetas)
        self.grid_productos.controls = [*self.tarjetas_productos(datos)]
            
        # 4. Actualizamos visualmente los botones de categoría
        self.renderizar_categorias()
            
        # 5. Refrescamos los cambios en la pantalla
        self.grid_productos.update()
        self.row_categorias.update()

    def renderizar_categorias(self):
        # Esta función dibuja o redibuja los botones para que cambien de color
        categorias = ["Dulces", "Salados", "Especial"]
        self.row_categorias.controls = [self.categoria_pill(c) for c in categorias]

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
            selected_date, set_selected_date = ft.use_state(datetime.datetime.now())
        
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
                    #on_click=lambda _: date_picker.pick_date(),
                ),
                self.texto_fecha_display,
                date_picker # Importante: debe estar en el árbol
            ]
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
                    spacing=15,
                    controls=[

                        ft.Container(
                            content=ft.Column([
                                ft.Text("Caja 1 (fetch)", weight=ft.FontWeight.BOLD, size= 18, color="black"),
                                ft.Text("Caja a Cargo de: Marco A. Vargas Valle (fetch)", size=16, color="black"),
                            ], spacing=2, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),
                        ft.Text("Monto a Pagar", weight=ft.FontWeight.BOLD, color="black"),
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
                            #Confirmar Monto a Pagar 
                            ft.TextButton(
                            "Confirmar monto a pagar", 
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),
                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Imprimir Ticket", 
                            on_click=lambda _: self.modal_mensaje("Ticket impreso!")
                        )

                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.CENTER,
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
                                ft.TextButton("¿No está registrado? Registrar Cliente."),
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
                            label="Material",
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
                        )

                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
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
                    ft.TextButton("Venta", icon=ft.Icons.SHOPPING_CART_SHARP, style=ft.ButtonStyle(color=self.COLOR_MARINO)),
                    ft.TextButton("Producción", icon=ft.Icons.BAKERY_DINING,on_click=lambda _: self.navegar("/ventana_principal_produccion") , style=ft.ButtonStyle(color=ft.Colors.GREY)),
                    ft.TextButton("Consultas", icon=ft.Icons.SEARCH, on_click=lambda _: self.navegar("/ventana_principal_consultas"), style=ft.ButtonStyle(color=ft.Colors.GREY)),
                ], spacing=20),
                self.btn_blanco("Cerrar Sesión", on_click=lambda _: self.navegar("/"))
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
            padding=ft.Padding.symmetric(horizontal=15, vertical=10)
        )

        # 3. MÉTODOS DE PAGO Y BOTONES FINALES
        metodos_pago = ft.Container(
            content=ft.Row([
                self.btn_oscuro("Efectivo", expand=1),
                self.btn_oscuro("Tarjeta", expand=1),
                self.btn_oscuro("Transferencia", expand=1),
                self.btn_blanco("Crear como apartado", expand=1, icon=ft.Icons.STAR_BORDER, on_click=self.modal_realizar_apartado),
                # Botón que dispara el modal
                self.btn_blanco(
                    "Imprimir Ticket", 
                    expand=1, 
                    icon=ft.Icons.PRINT, 
                    on_click=self.modal_imprimir_ticket
                ),
                self.btn_blanco("Finalizar Venta", expand=1, icon=ft.Icons.CHECK)
            ], spacing=10),
            padding=ft.Padding.symmetric(horizontal=15, vertical=5)
        )

        # 4. PANEL IZQUIERDO (Categorías y Productos)
        # Inicializamos los datos por primera vez
        self.renderizar_categorias()
        self.grid_productos.controls = [*self.tarjetas_productos(Fetch_Panes_Salados())]


        panel_izquierdo = ft.Container(
            content=ft.Column([
                # Categorías (referencia a la fila de categorias)
                self.row_categorias,
                ft.Divider(color=self.COLOR_MARINO),
                # Grid de Panes (referencia al grid de productos)
               self.grid_productos
            ]),
            expand=7, # Ocupa el 70% del ancho
            padding=15
        )

        # 5. PANEL DERECHO (Detalle de Venta)
        panel_derecho = ft.Container(
            content=ft.Column([
                # Lista de items en el carrito
                ft.Container(content=self.columna_items_carrito, expand=True),
                # Resumen (Subtotal, Impuestos, etc)
                

                self.container_monto("Subtotal", self.text_subtotal),
                # Resumen (Subtotal, Impuestos, etc)
                self.container_monto("Total", self.text_total),
            
    
            ]),
            expand=3, # Ocupa el 30% del ancho
            padding=30,
            border=ft.Border.only(left=ft.BorderSide(2, ft.Colors.BLACK)),
            border_radius=15,
           
        )

        # ENSAMBLE FINAL
        return ft.View(
            route="/ventana_principal",
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