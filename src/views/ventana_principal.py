import flet as ft
#Fetch para la Base de Datos.
from Backend.fetch import Fetch_Panes_Dulces, Fetch_Panes_Especiales, Fetch_Panes_Salados, fetch_clientes, registrar_cliente
from Backend.fetch import crear_apartado_detallado_db, registrar_venta_directa_db
from utils.Toasts import NotificationHelper
from Logic.logic import ApartadoLogic
from Logic.logic import VentaLogic
from Backend.fetch import crear_apartado_db
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

        # ESTADO: ¿Qué categoría está activa?
        self.categoria_actual = "Salados" 

        # ESTADO: ¿Qué tipo de pago está activo?
        self.pago_actual = "Efectivo"

        self.cliente_apartado_id = None

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

        self.fecha_entrega_apartado = datetime.datetime.now() # Estado inicial



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
                            ft.Text(pan["nombre"], weight=ft.FontWeight.BOLD, size=16, color=self.COLOR_GRIS_CLARO),
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
            self.carrito[nombre] = {"id": pan["id"], "precio": pan["precio"], "cantidad": 1}
        
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

    
    
    # Botones para seleccionar tipo de pago
    def tipo_pago_pill(self, texto):
        # ¿Este botón es el seleccionado?
        es_activo = self.pago_actual == texto
        
        return ft.Container(
            content=ft.Text(
                texto, 
                weight=ft.FontWeight.BOLD, 
                color=ft.Colors.BLACK if es_activo else ft.Colors.WHITE
            ),
            bgcolor=ft.Colors.GREEN_200 if es_activo else self.COLOR_MARINO,
            border_radius=5,
            padding=ft.Padding.symmetric(horizontal=30, vertical=8),
            expand=1,
            #Volvermos a llamar la función click_tipoPago
            on_click=self.click_tipo_pago,
            data=texto # Guardamos el nombre aquí para saber cuál se presionó
        )
     # -- Función para click a "Efectivo", "Transferencia", "Tarjeta"
    def click_tipo_pago(self, e):
            # 1. Cambiamos la categoría actual
            self.pago_actual = e.control.data
                
            # 2. Elegimos qué función de Fetch usar
            #None provisional: Aqui debe de haber un llamado para guardar la variable para el procedimiento de venta.
            if self.pago_actual== "Efectivo":
                    tipo_pago_seleccionado = None
            elif self.pago_actual == "Tarjeta":
                    tipo_pago_seleccionado = None
            elif self.pago_actual == "Transferencia":
                    tipo_pago_seleccionado = None

        #FUTURO: "tipo_pago_seleccionado" estará disponible para ser insertado para uno de los procedimientos almacenados para venta.

        # 4. Actualizamos visualmente los botones de categoría
            self.renderizar_tipo_pagos()
        # 5. Refrescamos los cambios en la pantalla
            self.row_tipo_pagos.update()

    def renderizar_tipo_pagos(self):
        # Esta función dibuja o redibuja los botones para que cambien de color
        tipos_pagos = ["Efectivo", "Tarjeta", "Transferencia"]
        self.row_tipo_pagos.controls = [self.tipo_pago_pill(pago) for pago in tipos_pagos]

    
    #Botón categoria con responsividad de si es seleccionada
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

    # -- Función para click a cierta categoría
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
        # 1. Cargamos todos los clientes una sola vez al inicio del componente
        self.todos_los_clientes = fetch_clientes() 

        async def close_anchor(e):
            cliente_seleccionado = e.control.data
            self.cliente_apartado_id = cliente_seleccionado['clientes_id']
            # Al seleccionar, el anchor se cierra con el nombre elegido
            await anchor.close_view(cliente_seleccionado['nombre'])

        async def open_anchor(e):
            await anchor.open_view()

        # --- 2. Lógica de Autocompletado (Filtrado) ---
        def handle_change(e):
            # Obtenemos lo que el usuario está escribiendo (en minúsculas para comparar mejor)
            texto_busqueda = e.data.lower()
            
            # Filtramos la lista original basándonos en el nombre
            clientes_filtrados = [
                c for c in self.todos_los_clientes 
                if texto_busqueda in c["nombre"].lower()
            ]

            # 3. Actualizamos los controles del SearchBar dinámicamente
            anchor.controls = [
                ft.ListTile(
                    title=ft.Text(cliente["nombre"]),
                    subtitle=ft.Text(f"Tel: {cliente['telefono']}"),
                    on_click=close_anchor,
                    data=cliente
                ) for cliente in clientes_filtrados
            ]
            
            # Refrescamos el componente para mostrar los nuevos resultados
            anchor.update()

        # --- 4. Definición del Componente ---
        anchor = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Buscar cliente...",
            view_hint_text="Sugerencias encontradas...",
            on_tap=open_anchor,
            on_change=handle_change, # <--- AQUÍ ACTIVAMOS EL AUTOCOMPLETADO
            controls=[
                # Iniciamos con todos los clientes visibles
                ft.ListTile(
                    title=ft.Text(cliente["nombre"]),
                    subtitle=ft.Text(f"Tel: {cliente['telefono']}"),
                    on_click=close_anchor,
                    data=cliente
                ) for cliente in self.todos_los_clientes
            ],
        )

        return ft.Column(controls=[anchor])

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
        # 1. El visualizador de la fecha (Referencia de clase)
        self.texto_fecha_display = ft.Text(
            value=self.fecha_entrega_apartado.strftime("%Y-%m-%d"),
            size=16,
            weight=ft.FontWeight.BOLD,
            color=self.COLOR_MARINO
        )

        # 2. El Handler: Qué pasa cuando el usuario elige la fecha
        def handle_cambio_fecha(e):
            if e.control.value:
                # Actualizamos el estado de la clase
                self.fecha_entrega_apartado = e.control.value
                # Actualizamos la interfaz
                self.texto_fecha_display.value = self.fecha_entrega_apartado.strftime("%Y-%m-%d")
                self.texto_fecha_display.update()
                print(f"Fecha de entrega seleccionada: {self.fecha_entrega_apartado}")

        # 3. El componente DatePicker (Invisible)
        self.selector_fecha = ft.DatePicker(
            first_date=datetime.datetime.now(), # No pueden apartar hacia el pasado
            last_date=datetime.datetime(2026, 12, 31),
            on_change=handle_cambio_fecha,
        )

        # Función interna para abrirlo manualmente
        def abrir_calendario(e):
            self.selector_fecha.open = True # <--- LA ALTERNATIVA
            self.selector_fecha.update()

        # 4. El Layout (Lo que el cajero ve)
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text("Fecha de Entrega:", size=12, color="black54"),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.CALENDAR_MONTH,
                        icon_color=self.COLOR_MARINO,
                        on_click=abrir_calendario, # Abre el calendario
                        tooltip="Seleccionar fecha"
                    ),
                    self.texto_fecha_display
                ]),
                self.selector_fecha # DEBE estar en el árbol de controles
            ]
    )

    def _notificar(self,page, mensaje: str, es_error: bool):
        """Atajo interno para disparar Toasts de forma asíncrona."""
        page.run_task(
            NotificationHelper.mostrar_toast, 
            page, 
            mensaje, 
            es_error # es_error
        )
    
    def _handle_imprimir_ticket(self, e):

        # 1. Ejecutamos la notificación (asíncrona)
        # Pasamos la función, luego los argumentos posicionales
        e.page.run_task(
            NotificationHelper.mostrar_toast, 
            e.page, 
            "¡Ticket impreso y venta registrada!", 
            False # es_error
        )

    def _handle_confirmar_apartado(self, e):
        # 1. Validación de seguridad "Senior"
        if self.cliente_apartado_id is None:
            self._notificar(e.page, "Error: Debes seleccionar un cliente en la barra de búsqueda", True)
            return # Detenemos la ejecución aquí

        try:
            # 1. Preparamos el detalle del carrito para el JSON de MySQL
            # Necesitas asegurarte de que cada pan en tu self.carrito tenga su 'id' real
            lista_productos_json = []
            for nombre, info in self.carrito.items():
                lista_productos_json.append({
                    "productos_id": info["id"], # Usa el ID real del pan
                    "cantidad": info["cantidad"]
                })

            # 2. Empaquetamos los datos generales
            datos_para_db = {
                "cliente_id": self.cliente_apartado_id,
                "usuario_id": 1, # ID de Marco Vargas
                "caja_id": 1,
                "total": float(self.text_total.value.replace("$", "").replace(",", "")),
                "anticipo": float(self.tf_anticipo.value),
                "fecha_entrega": self.fecha_entrega_apartado.strftime("%Y-%m-%d"),
                "metodo": self.pago_actual
            }

            # 3. Llamamos a la nueva función del backend
            exito, msj = crear_apartado_detallado_db(datos_para_db, lista_productos_json)
            
            if exito:
                e.page.pop_dialog()
                self._notificar(e.page, msj)
                self.carrito.clear()
                self.actualizar_vista_carrito()
            else:
                self._notificar(e.page, msj, True)

        except Exception as ex:
            self._notificar(e.page, f"Error de sistema: {str(ex)}", True)
    
    def _handle_imprimir_ticket_apartado(self,e):
        
        # 1. Ejecutamos la notificación (asíncrona)
        # Pasamos la función, luego los argumentos posicionales
        e.page.run_task(
            NotificationHelper.mostrar_toast, 
            e.page, 
            "¡Ticket impreso y apartado registrado!", 
            False # es_error
        )

    def _handle_cancelar_apartado(self,e):
        
        # 1. Cerramos el modal
        e.page.pop_dialog()
        # 1. Ejecutamos la notificación (asíncrona)
        # Pasamos la función, luego los argumentos posicionales
        e.page.run_task(
            NotificationHelper.mostrar_toast, 
            e.page, 
            "Apartado Cancelado.", 
            False # es_error
        )

    def _handle_finalizar_venta(self, e):
        # 1. Validaciones de Senior
        if not self.carrito:
            self._notificar(e.page, "El carrito está vacío", True)
            return
        
        # Aquí podrías agregar una validación de si se imprimió el ticket si fuera obligatorio
        
        try:
            # 2. Procesamos datos con la capa de Lógica
            total_limpio = VentaLogic.limpiar_monto(self.text_total.value)
            detalle_productos = VentaLogic.preparar_detalle_venta(self.carrito)

            # 3. Mandamos al Backend
            # Nota: Usamos IDs fijos (1) para usuario y caja por ahora
            exito, mensaje = registrar_venta_directa_db(
                usuario_id=1, 
                caja_id=1, 
                total=total_limpio, 
                detalles_lista=detalle_productos, 
                metodo=self.pago_actual
            )

            if exito:
                # 4. Éxito: Limpiamos carrito y notificamos
                self.carrito.clear()
                self.actualizar_vista_carrito() # Esto pone el total en $0.00
                self._notificar(e.page, mensaje, False)
            else:
                self._notificar(e.page, mensaje, True)

            e.page.pop_dialog()

        except Exception as ex:
            self._notificar(e.page, f"Error inesperado: {str(ex)}", True)
        
    # Aquí podrías agregar más lógica, como limpiar el carrito 
    # self.limpiar_carrito()
        
   # --- Modal para imprimir ticket --- 
    def modal_finalizar_venta(self, e):
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

                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Volver atrás", 
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),
                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Cancelar Venta", 
                            #PROVISIONAL: solo habra un pop
                            on_click=lambda _: ft.context.page.pop_dialog()
                        ),

                            #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Imprimir Ticket", 
                            on_click=self._handle_imprimir_ticket
                        ),
                            #Confirmar Monto a Pagar 
                            ft.TextButton(
                            "Confirmar y finalizar venta", 
                            on_click=self._handle_finalizar_venta
                        )
                        

                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
    # --- Handler para Registrar Cliente ---
    def _handle_registrar_cliente(self, e):
        nombre = self.tf_nombre_cliente.value.strip()
        telefono = self.tf_telefono_cliente.value.strip()

        # Validación básica de Senior antes de ir a la BD
        if not nombre or not telefono:
            self._notificar(e.page, "Por favor llena todos los campos", True)
            return

        # Llamada al Backend
        exito, mensaje = registrar_cliente(nombre, telefono)

        if exito:
            e.page.pop_dialog() # Cerramos el modal
            self._notificar(e.page, mensaje, False)
            
            # Tip Pro: Actualizamos la lista de clientes de la barra de búsqueda 
            # para que el nuevo cliente aparezca de inmediato sin reiniciar la app
            if hasattr(self, 'todos_los_clientes'):
                self.todos_los_clientes = fetch_clientes()
        else:
            self._notificar(e.page, mensaje, True)
    

    # --- Modal Actualizado ---
    def modal_registrar_cliente(self):
        # Definimos los campos como atributos de clase para leerlos en el Handler
        self.tf_nombre_cliente = ft.TextField(
            label="Nombre del Cliente",
            border_color=self.COLOR_MARINO,
            prefix_icon=ft.Icons.PERSON
        )
        self.tf_telefono_cliente = ft.TextField(
            label="Teléfono (10 dígitos)",
            border_color=self.COLOR_MARINO,
            prefix_icon=ft.Icons.PHONE,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=10 # Ayudamos al usuario a no pasarse
        )

        ft.context.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Nuevo Registro de Cliente", weight="bold"),
                content=ft.Column([
                    self.tf_nombre_cliente,
                    self.tf_telefono_cliente
                ], tight=True, spacing=20),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: ft.context.page.pop_dialog()),
                    self.btn_oscuro("Guardar Cliente", on_click=self._handle_registrar_cliente)
                ]
            )
        )
    
    def _handle_confirmar_apartado(self, e):
        # Recolección de datos para el Procedimiento Almacenado
        # Nota: usuario_id y caja_id deberían venir de tu login, aquí pondremos 1 por ahora.
        try:
            # Tomamos el primer producto del carrito para cumplir con tu sp_CrearApartado
            primer_producto_nombre = list(self.carrito.keys())[0]
            producto_id = 1 # Aquí deberías tener el ID real del producto
            cantidad = self.carrito[primer_producto_nombre]["cantidad"]

            datos_para_db = {
                "cliente_id": self.cliente_apartado_id,
                "usuario_id": 1, # ID del usuario Marco Vargas
                "caja_id": 1,
                "total": float(self.text_total.value.replace("$", "")),
                "anticipo": float(self.tf_anticipo.value),
                "producto_id": producto_id,
                "cantidad": cantidad,
                "fecha_entrega": self.fecha_entrega_apartado.strftime("%Y-%m-%d"),
                "metodo": self.pago_actual
            }

            exito, msj = crear_apartado_db(datos_para_db)
            
            if exito:
                e.page.pop_dialog()
                self._notificar(e.page, msj)
                self.carrito.clear() # Limpiamos después de la operación exitosa
                self.actualizar_vista_carrito()
            else:
                self._notificar(e.page, msj, True)

        except IndexError:
            self._notificar(e.page, "El carrito está vacío", True)
    
    
    #Modal para "Realizar apartado"
    def modal_realizar_apartado(self, e):

        def _on_anticipo_change(e):
            # Usamos nuestra lógica externa para calcular el restante
            nuevo_restante = ApartadoLogic.calcular_monto_restante(
                self.text_total.value, 
                self.tf_anticipo.value
            )
            self.txt_restante_display.value = f"${nuevo_restante:.2f}"
            self.txt_restante_display.update()

        # 1. Calculamos el anticipo mínimo sugerido (20%)
        anticipo_min = ApartadoLogic.calcular_anticipo_minimo(self.text_total.value)

        # 2. Creamos los campos con sus referencias
        self.tf_anticipo = ft.TextField(
            label="Monto del anticipo",
            value=str(anticipo_min),
            on_change=_on_anticipo_change, # Evento para calcular en tiempo real
            keyboard_type=ft.KeyboardType.NUMBER
        )

        self.txt_anticipo_minimo_display = ft.Text(
            value=f"${anticipo_min:.2f}",
            size=24, weight="bold"
        )

        self.txt_restante_display = ft.Text(
            value=f"${ApartadoLogic.calcular_monto_restante(self.text_total.value, str(anticipo_min)):.2f}",
            size=24, weight="bold"
        )

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
                                self.txt_anticipo_minimo_display
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50, expand=True),
                            bgcolor="#D1D9E6",
                            padding=20,
                            border_radius=15,
                        ),

                        #Fecha
                        self.agarrarFecha(),
                        #Anticipo
                        self.tf_anticipo,

                         ft.Container(
                            content=ft.Row([
                                ft.Text("Monto restante para finiquitar apartado", size=16, color="black54"),
                                #Realizar otra variable que calcule el restante a pagar de #self.text_total.value).
                                self.txt_restante_display
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

                        #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Cancelar Apartado", 
                            on_click=self._handle_cancelar_apartado
                        ),
                             
                             #Imprimir ticket, aquí falta agregar la funcionalidad de mandar a imprimir
                            ft.TextButton(
                            "Imprimir Ticket", 
                            on_click=self._handle_imprimir_ticket_apartado
                        ),

                            #Confirmar Monto a Pagar 
                            ft.TextButton(
                            "Confirmar Apartado", 
                            #Realizar inserción de apartado.
                            on_click=self._handle_confirmar_apartado
                        ),
                       

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
                self.btn_oscuro("Pagos", on_click=lambda _: self.navegar("/consulta_pagos")),
                self.btn_blanco("Modificar Caja",on_click=lambda _: self.navegar("/caja")),
                self.btn_oscuro("Realizar Corte")
            ]),
            padding=ft.Padding.symmetric(horizontal=15, vertical=10)
        )



        # 3. MÉTODOS DE PAGO Y BOTONES FINALES}

        # Inicializamos los datos por primera vez
        self.renderizar_tipo_pagos()
        metodos_pago = ft.Container(
            content=ft.Row([
                #self.btn_oscuro("Efectivo", expand=1),
                #self.btn_oscuro("Tarjeta", expand=1),
                #self.btn_oscuro("Transferencia", expand=1),

                self.row_tipo_pagos,
                self.btn_blanco("Crear como apartado", expand=1, icon=ft.Icons.STAR_BORDER, on_click=self.modal_realizar_apartado),
                # Botón que dispara el modal
                self.btn_blanco(
                    "Finalizar Venta", 
                    expand=1, 
                    icon=ft.Icons.CHECK, 
                    on_click=self.modal_finalizar_venta
                ),
                #Provisional, cambiar "modal mensaje" por función apropiada para eliminar lo que haya seleccionado y guardar en BD.
                # self.btn_blanco("Finalizar Venta", expand=1, icon=ft.Icons.CHECK,on_click=self._handle_finalizar_venta)
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