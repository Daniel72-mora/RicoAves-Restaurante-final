import mysql.connector

# --- FUNCIÓN BASE PARA LA CONEXIÓN ---
def ejecutar_query(sql, valores=None, es_consulta=False):
    try:
        # Configuración de conexión para XAMPP (sin contraseña por defecto)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rico_aves"
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        
        if es_consulta:
            resultado = cursor.fetchall()
            return resultado
        
        conn.commit()
        return True
    except Exception as e:
        print(f"\n❌ Error de base de datos: {e}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- MENÚS DE LA INTERFAZ ---
def menu_principal():
    print("\n" + "="*40)
    print("   SISTEMA ADMINISTRATIVO RICO AVES")
    print("="*40)
    print("1. GESTIÓN DE PRODUCTOS")
    print("2. GESTIÓN DE CLIENTES")
    print("3. REGISTRAR VENTA (PEDIDO)")
    print("4. VER HISTORIAL DE VENTAS")
    print("5. SALIR")
    return input("Seleccione una opción: ")

# --- LÓGICA PRINCIPAL DEL PROGRAMA ---
while True:
    opcion = menu_principal()

    # 1. GESTIÓN DE PRODUCTOS (CRUD)
    if opcion == "1":
        print("\n--- SUBMENÚ PRODUCTOS ---")
        print("a. Agregar Producto/Combo")
        print("b. Ver Catálogo")
        print("c. Actualizar Precio")
        print("d. Eliminar Producto")
        sub = input("Seleccione: ").lower()

        if sub == "a":
            nom = input("Nombre del plato: ")
            desc = input("Descripción: ")
            pre = float(input("Precio: "))
            cat = input("Categoría (Individual/Combo/Bebida): ")
            sql = "INSERT INTO productos (nombre, descripcion, precio, categoria) VALUES (%s, %s, %s, %s)"
            ejecutar_query(sql, (nom, desc, pre, cat))
            print("✅ Producto guardado.")

        elif sub == "b":
            res = ejecutar_query("SELECT * FROM productos", es_consulta=True)
            print("\nID | NOMBRE | PRECIO | CATEGORÍA")
            for p in res:
                print(f"{p[0]} | {p[1]} | ${p[3]} | {p[4]}")

        elif sub == "c":
            id_p = int(input("ID del producto a cambiar: "))
            nuevo_p = float(input("Nuevo precio: "))
            ejecutar_query("UPDATE productos SET precio = %s WHERE id_producto = %s", (nuevo_p, id_p))
            print("✅ Precio actualizado.")

        elif sub == "d":
            id_p = int(input("ID del producto a borrar: "))
            ejecutar_query("DELETE FROM productos WHERE id_producto = %s", (id_p,))
            print("✅ Producto eliminado.")

    # 2. GESTIÓN DE CLIENTES
    elif opcion == "2":
        print("\n--- REGISTRO DE CLIENTES ---")
        nom = input("Nombre completo: ")
        tel = input("Teléfono: ")
        dir = input("Dirección: ")
        mail = input("Correo: ")
        sql = "INSERT INTO clientes (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)"
        ejecutar_query(sql, (nom, tel, dir, mail))
        print("✅ Cliente registrado.")

    # 3. REGISTRAR VENTA (PEDIDO)
    elif opcion == "3":
        print("\n--- NUEVA VENTA ---")
        # Mostrar datos rápidos para facilitar la venta
        print("Clientes disponibles:")
        clis = ejecutar_query("SELECT id_cliente, nombre FROM clientes", es_consulta=True)
        for c in clis: print(f"ID: {c[0]} - {c[1]}")
        
        id_c = int(input("\nID del Cliente: "))
        id_p = int(input("ID del Producto: "))
        cant = int(input("Cantidad: "))
        
        sql = "INSERT INTO pedidos (id_cliente, id_producto, cantidad) VALUES (%s, %s, %s)"
        ejecutar_query(sql, (id_c, id_p, cant))
        print("✅ ¡Venta registrada exitosamente!")

    # 4. VER HISTORIAL DE VENTAS (JOIN)
    elif opcion == "4":
        print("\n" + "-"*50)
        print("HISTORIAL COMPLETO DE VENTAS")
        print("-"*50)
        # Consulta avanzada con JOIN para ver nombres en lugar de puros números
        sql = """
            SELECT p.id_pedido, c.nombre, pr.nombre, p.cantidad, (pr.precio * p.cantidad)
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            JOIN productos pr ON p.id_producto = pr.id_producto
        """
        ventas = ejecutar_query(sql, es_consulta=True)
        if ventas:
            for v in ventas:
                print(f"Ticket #{v[0]} | {v[1]} compró {v[3]}x {v[2]} | Total: ${v[4]}")
        else:
            print("No hay ventas registradas.")

    # 5. SALIR
    elif opcion == "5":
        print("Cerrando sistema de Rico Aves. ¡Hasta pronto!")
        break
    
    else:
        print("⚠️ Opción no válida.")