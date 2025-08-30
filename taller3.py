import csv
import os
from datetime import datetime

class sistem:
    def __init__(self):
        self.cliente_file = "clientes.csv"
        self.pedido_file = "pedidos.csv"
        self.venta_file = "ventas.csv"
        self.inicializar_archivos()
    
    def inicializar_archivos(self):
        if not os.path.exists(self.cliente_file):
            with open(self.cliente_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id_cliente', 'nombre', 'apellido', 'telefono', 'activo'])
        
        if not os.path.exists(self.pedido_file):
            with open(self.pedido_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id_pedido', 'id_cliente', 'producto', 'precio', 'cantidad', 'activo'])
        
        if not os.path.exists(self.venta_file):
            with open(self.venta_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id_venta', 'id_cliente', 'producto', 'precio', 'cantidad', 'fecha'])

    def obtener_proximo_id(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                ids = []
                for row in reader:
                    if row:
                        ids.append(int(row[0]))
                return max(ids) + 1 if ids else 1
        except FileNotFoundError:
            return 1

    def registrar_cliente(self):
        print("\n--- REGISTRAR NUEVO CLIENTE ---")
        cliente_nombre = input("Nombre: ")
        cliente_apellido = input("Apellido: ")
        cliente_telefono = input("Teléfono: ")
        
        cliente_id = self.obtener_proximo_id(self.cliente_file)
        
        with open(self.cliente_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([cliente_id, cliente_nombre, cliente_apellido, cliente_telefono, 1])
        
        print(f"Cliente registrado exitosamente con ID: {cliente_id}")

    def listar_clientes(self):
        print("\nLISTADO DE CLIENTES")
        try:
            with open(self.cliente_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                
                cliente_lista = []
                for row in reader:
                    if row:
                        cliente_estado = "Activo" if row[4] == "1" else "Inactivo"
                        cliente_lista.append({
                            'id': row[0],
                            'nombre': row[1],
                            'apellido': row[2],
                            'telefono': row[3],
                            'estado': cliente_estado
                        })
                
                if not cliente_lista:
                    print("No hay clientes registrados.")
                    return
                
                print(f"{'ID':<5} {'Nombre':<15} {'Apellido':<15} {'Teléfono':<12} {'Estado':<8}")
                print("-" * 60)
                for cliente in cliente_lista:
                    print(f"{cliente['id']:<5} {cliente['nombre']:<15} {cliente['apellido']:<15} {cliente['telefono']:<12} {cliente['estado']:<8}")
        
        except FileNotFoundError:
            print("No hay clientes registrados.")

    def eliminar_cliente(self):
        print("\nELIMINAR CLIENTE")
        self.listar_clientes()
        
        try:
            cliente_id = int(input("\nID del cliente a eliminar: "))
            
            cliente_todos = []
            with open(self.cliente_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if row:
                        cliente_todos.append(row)
            
            cliente_encontrado = False
            for cliente in cliente_todos:
                if int(cliente[0]) == cliente_id:
                    cliente[4] = '0'  
                    cliente_encontrado = True
                    break
            
            if cliente_encontrado:
                with open(self.cliente_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(cliente_todos)
                print("Cliente marcado como inactivo exitosamente.")
            else:
                print("Cliente no encontrado.")
                
        except ValueError:
            print("ID debe ser un número válido.")

    def registrar_pedido(self):
        print("\n--- REGISTRAR NUEVO PEDIDO ---")
        self.listar_clientes()
        
        try:
            cliente_id = int(input("\nID del cliente: "))
            
            cliente_existe = False
            with open(self.cliente_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and int(row[0]) == cliente_id and row[4] == '1':
                        cliente_existe = True
                        break
            
            if not cliente_existe:
                print("Cliente no encontrado o inactivo.")
                return
            
            pedido_producto = input("Producto: ")
            try:
                pedido_precio = float(input("Precio (0 si no aplica): "))
            except ValueError:
                pedido_precio = 0.0
            
            try:
                pedido_cantidad = int(input("Cantidad (1 si no aplica): "))
            except ValueError:
                pedido_cantidad = 1
            
            pedido_id = self.obtener_proximo_id(self.pedido_file)
            
            with open(self.pedido_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([pedido_id, cliente_id, pedido_producto, pedido_precio, pedido_cantidad, 1])
            
            print(f"Pedido registrado exitosamente con ID: {pedido_id}")
            
        except ValueError:
            print("Datos inválidos")

    def listar_pedidos_cliente(self):
        print("\nLISTAR PEDIDOS POR CLIENTE")
        self.listar_clientes()
        
        try:
            cliente_id = int(input("\nID del cliente: "))
            
            cliente_nombre = ""
            with open(self.cliente_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and int(row[0]) == cliente_id:
                        cliente_nombre = f"{row[1]} {row[2]}"
                        break
            
            if not cliente_nombre:
                print("Cliente no encontrado")
                return
            
            print(f"\nPedidos de {cliente_nombre}:")
            print(f"{'ID':<5} {'Producto':<20} {'Precio':<10} {'Cantidad':<8} {'Estado':<8}")
            print("-" * 55)
            
            pedido_encontrados = False
            with open(self.pedido_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and int(row[1]) == cliente_id:
                        pedido_estado = "Activo" if row[5] == "1" else "Inactivo"
                        print(f"{row[0]:<5} {row[2]:<20} {float(row[3]):<10.2f} {row[4]:<8} {pedido_estado:<8}")
                        pedido_encontrados = True
            
            if not pedido_encontrados:
                print("No se encontraron pedidos para este cliente")
                
        except ValueError:
            print("ID debe ser un número válido")

    def guardar_venta(self):
        print("\n--- GUARDAR VENTA ---")
        self.listar_clientes()
        
        try:
            cliente_id = int(input("\nID del cliente: "))
            
            cliente_existe = False
            cliente_nombre = ""
            with open(self.cliente_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and int(row[0]) == cliente_id and row[4] == '1':
                        cliente_existe = True
                        cliente_nombre = f"{row[1]} {row[2]}"
                        break
            
            if not cliente_existe:
                print("Cliente no encontrado o inactivo.")
                return
            
            print(f"\nRegistrando venta para: {cliente_nombre}")
            venta_producto = input("Producto: ")
            
            try:
                venta_precio = float(input("Precio: "))
                venta_cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Precio y cantidad deben ser números válidos.")
                return
            
            venta_id = self.obtener_proximo_id(self.venta_file)
            venta_fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.venta_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([venta_id, cliente_id, venta_producto, venta_precio, venta_cantidad, venta_fecha])
            
            venta_total = venta_precio * venta_cantidad
            print(f"Venta registrada exitosamente. Total: ${venta_total:.2f}")
            
        except ValueError:
            print("ID debe ser un número valido")

    def listar_ventas_cliente(self):
        print("\nLISTAR VENTAS POR CLIENTE")
        
        cliente_nombre_buscar = input("Nombre del cliente: ").lower()
        
        cliente_coincidentes = []
        with open(self.cliente_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row and row[4] == '1':
                    cliente_nombre_completo = f"{row[1]} {row[2]}".lower()
                    if cliente_nombre_buscar in cliente_nombre_completo:
                        cliente_coincidentes.append({
                            'id': int(row[0]),
                            'nombre': f"{row[1]} {row[2]}"
                        })
        
        if not cliente_coincidentes:
            print("No se encontraron clientes con ese nombre")
            return
        
        if len(cliente_coincidentes) > 1:
            print("\nClientes encontrados:")
            for i, cliente in enumerate(cliente_coincidentes, 1):
                print(f"{i}. {cliente['nombre']}")
            
            try:
                seleccion = int(input("\nSeleccione el cliente: ")) - 1
                if seleccion < 0 or seleccion >= len(cliente_coincidentes):
                    print("Selección invalida")
                    return
                cliente_seleccionado = cliente_coincidentes[seleccion]
            except ValueError:
                print("Selección invalida.")
                return
        else:
            cliente_seleccionado = cliente_coincidentes[0]
        
        venta_lista = []
        with open(self.venta_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row and int(row[1]) == cliente_seleccionado['id']:
                    venta_lista.append({
                        'producto': row[2],
                        'precio': float(row[3]),
                        'cantidad': int(row[4]),
                        'fecha': row[5]
                    })
        
        if not venta_lista:
            print(f"No se encontraron ventas para {cliente_seleccionado['nombre']}")
            return
        
        print(f"\nVentas de {cliente_seleccionado['nombre']}:")
        print(f"{'Producto':<20} {'Precio':<10} {'Cantidad':<8} {'Subtotal':<10} {'Fecha':<20}")
        print("-" * 70)
        
        venta_total_general = 0
        for venta in venta_lista:
            venta_subtotal = venta['precio'] * venta['cantidad']
            venta_total_general += venta_subtotal
            print(f"{venta['producto']:<20} {venta['precio']:<10.2f} {venta['cantidad']:<8} {venta_subtotal:<10.2f} {venta['fecha']:<20}")
        
        print("-" * 70)
        print(f"{'TOTAL GENERAL:':<48} {venta_total_general:.2f}")

    def mostrar_menu(self):
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE GESTIÓN DE CLIENTES Y PEDIDOS")
            print("="*50)
            print("1. Registrar cliente")
            print("2. Listar clientes")
            print("3. Eliminar cliente")
            print("4. Registrar pedido")
            print("5. Listar pedidos de un cliente")
            print("6. Guardar venta")
            print("7. Listar ventas por cliente")
            print("8. Salir")
            print("="*50)
            
            try:
                opcion = int(input("Seleccione una opción: "))
                
                if opcion == 1:
                    self.registrar_cliente()
                elif opcion == 2:
                    self.listar_clientes()
                elif opcion == 3:
                    self.eliminar_cliente()
                elif opcion == 4:
                    self.registrar_pedido()
                elif opcion == 5:
                    self.listar_pedidos_cliente()
                elif opcion == 6:
                    self.guardar_venta()
                elif opcion == 7:
                    self.listar_ventas_cliente()
                elif opcion == 8:
                    print("¡Gracias por usar el sistema!")
                    break
                else:
                    print("Intente nuevamente")
                    
            except ValueError:
                print("Por favor, ingrese un número valido")

if __name__ == "__main__":
    sistema = sistem()
    sistema.mostrar_menu()