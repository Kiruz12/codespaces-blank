import csv
import os
from datetime import datetime

# Clases para listas enlazadas
class Nodo:
    def __init__(self, datos):
        self.datos = datos  # [id, tipo, id_referencia, nombre, precio, cantidad, estado, fecha]
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def agregar(self, datos):
        nuevo_nodo = Nodo(datos)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def obtener_todos(self):
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(actual.datos)
            actual = actual.siguiente
        return elementos
    
    def buscar_por_id(self, id_buscar, tipo=None):
        actual = self.cabeza
        while actual is not None:
            if actual.datos[0] == id_buscar and (tipo is None or actual.datos[1] == tipo):
                return actual.datos
            actual = actual.siguiente
        return None
    
    def buscar_por_tipo(self, tipo):
        resultados = []
        actual = self.cabeza
        while actual is not None:
            if actual.datos[1] == tipo:
                resultados.append(actual.datos)
            actual = actual.siguiente
        return resultados
    
    def buscar_por_nombre(self, nombre_buscar, tipo=None):
        resultados = []
        actual = self.cabeza
        while actual is not None:
            if nombre_buscar.lower() in actual.datos[3].lower() and (tipo is None or actual.datos[1] == tipo):
                resultados.append(actual.datos)
            actual = actual.siguiente
        return resultados
    
    def modificar_estado(self, id_modificar, nuevo_estado):
        actual = self.cabeza
        while actual is not None:
            if actual.datos[0] == id_modificar:
                actual.datos[6] = nuevo_estado
                return True
            actual = actual.siguiente
        return False
    
    def eliminar_por_id(self, id_eliminar):
        if self.esta_vacia():
            return False
        
        # Caso especial: eliminar la cabeza
        if self.cabeza.datos[0] == id_eliminar:
            self.cabeza = self.cabeza.siguiente
            return True
        
        # Buscar el nodo a eliminar
        actual = self.cabeza
        anterior = None
        
        while actual is not None:
            if actual.datos[0] == id_eliminar:
                anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        
        return False
    
    def obtener_max_id_por_tipo(self, tipo):
        max_id = 0
        actual = self.cabeza
        while actual is not None:
            if actual.datos[1] == tipo:
                id_actual = int(actual.datos[0])
                if id_actual > max_id:
                    max_id = id_actual
            actual = actual.siguiente
        return max_id

class SistemaGestion:
    def __init__(self):
        self.archivo_csv = "info.csv"
        self.lista_datos = ListaEnlazada()
        self.inicializar_archivo()
        self.cargar_datos()
    
    def inicializar_archivo(self):
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'tipo', 'id_referencia', 'nombre', 'precio', 'cantidad', 'estado', 'fecha'])
    
    def cargar_datos(self):
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar cabecera
                for row in reader:
                    if row and len(row) == 8:
                        # Convertir tipos de datos adecuados
                        row[4] = float(row[4]) if row[4] else 0.0
                        row[5] = int(row[5]) if row[5] else 1
                        self.lista_datos.agregar(row)
        except FileNotFoundError:
            pass
    
    def guardar_datos(self):
        with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'tipo', 'id_referencia', 'nombre', 'precio', 'cantidad', 'estado', 'fecha'])
            
            datos = self.lista_datos.obtener_todos()
            for dato in datos:
                writer.writerow(dato)
    
    def obtener_proximo_id(self, tipo):
        return self.lista_datos.obtener_max_id_por_tipo(tipo) + 1
    
    def registrar_cliente(self):
        print("\n--- REGISTRAR NUEVO CLIENTE ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        telefono = input("Teléfono: ")
        
        cliente_id = self.obtener_proximo_id("cliente")
        nombre_completo = f"{nombre} {apellido}"
        
        datos_cliente = [
            cliente_id, "cliente", "", nombre_completo, 0, 1, "activo", datetime.now().strftime("%Y-%m-%d")
        ]
        
        self.lista_datos.agregar(datos_cliente)
        self.guardar_datos()
        print(f"Cliente registrado exitosamente con ID: {cliente_id}")
    
    def listar_clientes(self):
        print("\nLISTADO DE CLIENTES")
        clientes = self.lista_datos.buscar_por_tipo("cliente")
        
        if not clientes:
            print("No hay clientes registrados.")
            return
        
        print(f"{'ID':<5} {'Nombre':<20} {'Teléfono':<12} {'Estado':<8}")
        print("-" * 50)
        
        for cliente in clientes:
            # Extraer teléfono si está en el nombre (formato: "Nombre Apellido - Teléfono")
            partes = cliente[3].split(' - ')
            nombre = partes[0]
            telefono = partes[1] if len(partes) > 1 else "N/A"
            
            print(f"{cliente[0]:<5} {nombre:<20} {telefono:<12} {cliente[6]:<8}")
    
    def eliminar_cliente(self):
        print("\nELIMINAR CLIENTE")
        self.listar_clientes()
        
        try:
            cliente_id = input("\nID del cliente a eliminar: ")
            
            cliente = self.lista_datos.buscar_por_id(cliente_id, "cliente")
            if not cliente:
                print("Cliente no encontrado.")
                return
            
            if self.lista_datos.modificar_estado(cliente_id, "inactivo"):
                self.guardar_datos()
                print("Cliente marcado como inactivo exitosamente.")
            else:
                print("Error al eliminar el cliente.")
                
        except ValueError:
            print("ID debe ser un número válido.")
    
    def registrar_pedido(self):
        print("\n--- REGISTRAR NUEVO PEDIDO ---")
        self.listar_clientes()
        
        try:
            cliente_id = input("\nID del cliente: ")
            
            cliente = self.lista_datos.buscar_por_id(cliente_id, "cliente")
            if not cliente or cliente[6] != "activo":
                print("Cliente no encontrado o inactivo.")
                return
            
            producto = input("Producto: ")
            try:
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Precio y cantidad deben ser números válidos.")
                return
            
            pedido_id = self.obtener_proximo_id("pedido")
            
            datos_pedido = [
                pedido_id, "pedido", cliente_id, producto, precio, cantidad, "activo", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
            
            self.lista_datos.agregar(datos_pedido)
            self.guardar_datos()
            print(f"Pedido registrado exitosamente con ID: {pedido_id}")
            
        except ValueError:
            print("Datos inválidos")
    
    def listar_pedidos_cliente(self):
        print("\nLISTAR PEDIDOS POR CLIENTE")
        self.listar_clientes()
        
        try:
            cliente_id = input("\nID del cliente: ")
            
            cliente = self.lista_datos.buscar_por_id(cliente_id, "cliente")
            if not cliente:
                print("Cliente no encontrado")
                return
            
            pedidos = self.lista_datos.buscar_por_tipo("pedido")
            pedidos_cliente = [p for p in pedidos if p[2] == cliente_id]
            
            print(f"\nPedidos de {cliente[3]}:")
            print(f"{'ID':<5} {'Producto':<20} {'Precio':<10} {'Cantidad':<8} {'Estado':<8}")
            print("-" * 55)
            
            if not pedidos_cliente:
                print("No se encontraron pedidos para este cliente")
                return
            
            for pedido in pedidos_cliente:
                print(f"{pedido[0]:<5} {pedido[3]:<20} {pedido[4]:<10.2f} {pedido[5]:<8} {pedido[6]:<8}")
                
        except ValueError:
            print("ID debe ser un número válido")
    
    def registrar_venta(self):
        print("\n--- REGISTRAR VENTA ---")
        self.listar_clientes()
        
        try:
            cliente_id = input("\nID del cliente: ")
            
            cliente = self.lista_datos.buscar_por_id(cliente_id, "cliente")
            if not cliente or cliente[6] != "activo":
                print("Cliente no encontrado o inactivo.")
                return
            
            producto = input("Producto: ")
            try:
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Precio y cantidad deben ser números válidos.")
                return
            
            venta_id = self.obtener_proximo_id("venta")
            
            datos_venta = [
                venta_id, "venta", cliente_id, producto, precio, cantidad, "completada", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
            
            self.lista_datos.agregar(datos_venta)
            self.guardar_datos()
            
            total = precio * cantidad
            print(f"Venta registrada exitosamente. ID: {venta_id}, Total: ${total:.2f}")
            
        except ValueError:
            print("ID debe ser un número válido")
    
    def listar_ventas_cliente(self):
        print("\nLISTAR VENTAS POR CLIENTE")
        
        nombre_buscar = input("Nombre del cliente: ")
        
        clientes = self.lista_datos.buscar_por_nombre(nombre_buscar, "cliente")
        
        if not clientes:
            print("No se encontraron clientes con ese nombre")
            return
        
        if len(clientes) > 1:
            print("\nClientes encontrados:")
            for i, cliente in enumerate(clientes, 1):
                print(f"{i}. {cliente[3]}")
            
            try:
                seleccion = int(input("\nSeleccione el cliente: ")) - 1
                if seleccion < 0 or seleccion >= len(clientes):
                    print("Selección inválida")
                    return
                cliente_seleccionado = clientes[seleccion]
            except ValueError:
                print("Selección inválida.")
                return
        else:
            cliente_seleccionado = clientes[0]
        
        ventas = self.lista_datos.buscar_por_tipo("venta")
        ventas_cliente = [v for v in ventas if v[2] == cliente_seleccionado[0]]
        
        if not ventas_cliente:
            print(f"No se encontraron ventas para {cliente_seleccionado[3]}")
            return
        
        print(f"\nVentas de {cliente_seleccionado[3]}:")
        print(f"{'ID':<5} {'Producto':<20} {'Precio':<10} {'Cantidad':<8} {'Total':<10} {'Fecha':<16}")
        print("-" * 75)
        
        total_general = 0
        for venta in ventas_cliente:
            total_venta = venta[4] * venta[5]
            total_general += total_venta
            fecha_corta = venta[7].split(' ')[0]  # Solo la fecha, no la hora
            print(f"{venta[0]:<5} {venta[3]:<20} {venta[4]:<10.2f} {venta[5]:<8} {total_venta:<10.2f} {fecha_corta:<16}")
        
        print("-" * 75)
        print(f"{'TOTAL GENERAL:':<43} {total_general:.2f}")
    
    def mostrar_estadisticas(self):
        print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
        
        # Contar elementos por tipo
        clientes = self.lista_datos.buscar_por_tipo("cliente")
        pedidos = self.lista_datos.buscar_por_tipo("pedido")
        ventas = self.lista_datos.buscar_por_tipo("venta")
        
        print(f"Total clientes: {len(clientes)}")
        print(f"Total pedidos: {len(pedidos)}")
        print(f"Total ventas: {len(ventas)}")
        
        # Calcular ingresos totales
        ingresos_totales = 0
        for venta in ventas:
            ingresos_totales += venta[4] * venta[5]
        
        print(f"Ingresos totales: ${ingresos_totales:.2f}")
    
    def mostrar_menu(self):
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE GESTIÓN INTEGRADO")
            print("="*50)
            print("1. Registrar cliente")
            print("2. Listar clientes")
            print("3. Eliminar cliente")
            print("4. Registrar pedido")
            print("5. Listar pedidos de cliente")
            print("6. Registrar venta")
            print("7. Listar ventas por cliente")
            print("8. Estadísticas del sistema")
            print("9. Salir")
            print("="*50)
            
            try:
                opcion = input("Seleccione una opción: ")
                
                if opcion == "1":
                    self.registrar_cliente()
                elif opcion == "2":
                    self.listar_clientes()
                elif opcion == "3":
                    self.eliminar_cliente()
                elif opcion == "4":
                    self.registrar_pedido()
                elif opcion == "5":
                    self.listar_pedidos_cliente()
                elif opcion == "6":
                    self.registrar_venta()
                elif opcion == "7":
                    self.listar_ventas_cliente()
                elif opcion == "8":
                    self.mostrar_estadisticas()
                elif opcion == "9":
                    print("¡Gracias por usar el sistema!")
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")
                    
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    sistema = SistemaGestion()
    sistema.mostrar_menu()
    