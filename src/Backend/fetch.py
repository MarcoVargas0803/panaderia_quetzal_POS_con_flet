
import mysql.connector
#Realizar obtención de datos de producto_venta

#Image : Obtenido de un repositorio de fotos, URL.
#Nombre: Nombre del pan.
#Precio: Precio del pan.

#Realizar un fetch, para poder instanciar todos los componentes "producto_venta" para agregarlos al container.}

# Pan para panes dulces: select nombre, precio from productos WHERE categorias_id=2;
# Pan para panes especiales: select nombre, precio from productos WHERE categorias_id=3;


def Fetch_Panes_Salados() -> list:

    cnx = mysql.connector.connect(user='root', password='V4vm080305', database='panaderia', host="localhost")
    cursor = cnx.cursor()

    # Pan para panes salados: select nombre, precio from productos WHERE categorias_id=1;
    query = ("SELECT productos_id, nombre, precio from productos WHERE categorias_id=1")
    cursor.execute(query)
    resultados = cursor.fetchall()


    # 4. Definir tu lista (arrayList) para guardar los datos
    lista_panes_salados = []


    # Convertimos cada fila de la base de datos en un diccionario
    for (id_p, nombre, precio) in resultados:
        producto_dict = {
            "id": id_p,
            "nombre": nombre,
            "precio": precio
        }
        lista_panes_salados.append(producto_dict)
    
    cursor.close()
    cnx.close()

    return lista_panes_salados

    

def Fetch_Panes_Dulces() -> list:

    cnx = mysql.connector.connect(user='root',password='V4vm080305', database='panaderia', host="localhost")
    cursor = cnx.cursor()

    # Pan para panes salados: select nombre, precio from productos WHERE categorias_id=1;
    query = ("select productos_id, nombre, precio from productos WHERE categorias_id=2")
    cursor.execute(query)

    resultados = cursor.fetchall()

     # 4. Definir tu lista (arrayList) para guardar los datos
    lista_panes_dulces = []

     # Convertimos cada fila de la base de datos en un diccionario
    for (id_p, nombre, precio) in resultados:
        producto_dict = {
            "id": id_p,
            "nombre": nombre,
            "precio": precio
        }
        lista_panes_dulces.append(producto_dict)

    cursor.close()
    cnx.close()


    return lista_panes_dulces
    
    

def Fetch_Panes_Especiales():

    cnx = mysql.connector.connect(user='root', password="V4vm080305", database='panaderia', host="localhost")
    cursor = cnx.cursor()

    # Pan para panes salados: select nombre, precio from productos WHERE categorias_id=1;
    query = ("select productos_id, nombre, precio from productos WHERE categorias_id=3")

    cursor.execute(query)

    resultados = cursor.fetchall()

    lista_panes_especiales = []

     # Convertimos cada fila de la base de datos en un diccionario
    for (id_p, nombre, precio) in resultados:
        producto_dict = {
            "id": id_p,
            "nombre": nombre,
            "precio": precio
        }
        lista_panes_especiales.append(producto_dict)

    cursor.close()
    cnx.close()

    return lista_panes_especiales


# Llama a la función e imprime el resultado para probar
if __name__ == "__main__":
    print("Iniciando prueba de base de datos...")
    
    # Mandamos a llamar a la función y guardamos lo que nos devuelve
    panes_salados = Fetch_Panes_Salados()
    for pan in panes_salados:
        #Aqui puede entrar la lógica para agregar los campos necesarios para los componentes, instanciar
        print(pan["nombre"])    
    # Imprimimos la lista en la terminal

def fetch_clientes() -> list:
        try:
            cnx = mysql.connector.connect(
                user='root', 
                password='V4vm080305', 
                database='panaderia', 
                host="localhost"
            )
            cursor = cnx.cursor()

            # Usamos los nombres exactos: clientes_id, nombre, telefono
            query = ("SELECT clientes_id, nombre, telefono FROM clientes")
            cursor.execute(query)

            resultados = cursor.fetchall()
            
            lista_clientes = []
            for (c_id, nom, tel) in resultados:
                lista_clientes.append({
                    "clientes_id": c_id,
                    "nombre": nom,
                    "telefono": tel
                })

            return lista_clientes

        except mysql.connector.Error as err:
            print(f"Error en MySQL: {err}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'cnx' in locals(): cnx.close()

def registrar_cliente(nombre: str, telefono: str) -> tuple[bool, str]:
    """Llama al procedimiento sp_RegistrarCliente en MySQL."""
    try:
        cnx = mysql.connector.connect(
            user='root', password='V4vm080305', database='panaderia', host="localhost"
        )
        cursor = cnx.cursor()

        # 1. Llamamos al procedimiento almacenado
        # Los parámetros deben ir en una lista o tupla
        cursor.callproc('sp_RegistrarCliente', [nombre, telefono])
        
        # IMPORTANTE: Al ser un INSERT dentro de un procedimiento, hay que hacer commit
        cnx.commit()
        
        return True, "Cliente registrado con éxito"

    except mysql.connector.Error as err:
        # 2. Capturamos el error personalizado de tu SIGNAL SQLSTATE '45000'
        mensaje_error = f"Error en BD: {err.msg}"
        return False, mensaje_error
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'cnx' in locals(): cnx.close()

# Backend/fetch.py

def crear_apartado_db(datos: dict) -> tuple[bool, str]:
    """Llama al procedimiento sp_CrearApartado con los parámetros requeridos."""
    try:
        cnx = mysql.connector.connect(
            user='root', password='V4vm080305', database='panaderia', host="localhost"
        )
        cursor = cnx.cursor()

        # Los parámetros deben seguir el orden exacto de tu PROCEDURE
        params = [
            datos['cliente_id'],
            datos['usuario_id'],
            datos['caja_id'],
            datos['total'],
            datos['anticipo'],
            datos['producto_id'],
            datos['cantidad'],
            datos['fecha_entrega'],
            datos['metodo']
        ]

        cursor.callproc('sp_CrearApartado', params)
        cnx.commit()
        return True, "Apartado registrado exitosamente"

    except mysql.connector.Error as err:
        return False, f"Error en BD: {err.msg}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'cnx' in locals(): cnx.close()

import json # Necesario para procesar el carrito

def crear_apartado_detallado_db(datos: dict, items_carrito: list) -> tuple[bool, str]:
    """Llama al procedimiento detallado pasando el carrito completo como JSON."""
    try:
        cnx = mysql.connector.connect(
            user='root', password='V4vm080305', database='panaderia', host="localhost"
        )
        cursor = cnx.cursor()

        # Convertimos la lista de productos de Python a un string JSON para MySQL
        # El formato debe ser: [{"productos_id": 1, "cantidad": 4}, ...]
        carrito_json = json.dumps(items_carrito)

        params = [
            datos['cliente_id'],
            datos['usuario_id'],
            datos['caja_id'],
            datos['total'],
            datos['anticipo'],
            carrito_json, # Enviamos TODO el detalle aquí
            datos['fecha_entrega'],
            datos['metodo']
        ]

        # Llamamos directamente al procedimiento detallado
        cursor.callproc('sp_CrearApartadoDetallado', params)
        cnx.commit()
        return True, "¡Apartado registrado con éxito!"

    except mysql.connector.Error as err:
        return False, f"Error en BD: {err.msg}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'cnx' in locals(): cnx.close()


def registrar_venta_directa_db(usuario_id, caja_id, total, detalles_lista, metodo) -> tuple[bool, str]:
    try:
        cnx = mysql.connector.connect(
            user='root', password='V4vm080305', database='panaderia', host="localhost"
        )
        cursor = cnx.cursor()

        # Convertimos la lista de Python a JSON string
        detalles_json = json.dumps(detalles_lista)

        # Parámetros según tu SP: usuario, caja, total, detalles(JSON), metodo
        params = [usuario_id, caja_id, total, detalles_json, metodo]
        
        cursor.callproc('sp_RegistrarVentaDirectaDetallada', params)
        cnx.commit()
        
        return True, "Venta finalizada con éxito"
    except mysql.connector.Error as err:
        return False, f"Error en BD: {err.msg}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'cnx' in locals(): cnx.close()