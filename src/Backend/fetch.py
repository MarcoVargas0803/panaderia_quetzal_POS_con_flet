
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
    query = ("select nombre, precio from productos WHERE categorias_id=1")
    cursor.execute(query)


    resultados = cursor.fetchall()


    # 4. Definir tu lista (arrayList) para guardar los datos
    lista_panes_salados = []


    # Convertimos cada fila de la base de datos en un diccionario
    for (nombre, precio) in resultados:
        producto_dict = {
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
    query = ("select nombre, precio from productos WHERE categorias_id=2")
    cursor.execute(query)

    resultados = cursor.fetchall()

     # 4. Definir tu lista (arrayList) para guardar los datos
    lista_panes_dulces = []

     # Convertimos cada fila de la base de datos en un diccionario
    for (nombre, precio) in resultados:
        producto_dict = {
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
    query = ("select nombre, precio from productos WHERE categorias_id=3")

    cursor.execute(query)

    resultados = cursor.fetchall()

    lista_panes_especiales = []

     # Convertimos cada fila de la base de datos en un diccionario
    for (nombre, precio) in resultados:
        producto_dict = {
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