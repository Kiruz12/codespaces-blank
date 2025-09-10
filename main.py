import csv
import os
from datetime import datetime

# Clases para lista enlazada
class NodoVenta:
    def __init__(self, datos):
        self.datos = datos  # [id, producto, cantidad, precio_unitario, fecha]
        self.siguiente = None

class ListaEnlazadaVentas:
    def __init__(self):
        self.cabeza = None
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def agregar_venta(self, datos):
        nuevo_nodo = NodoVenta(datos)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def obtener_todas_ventas(self):
        ventas = []
        actual = self.cabeza
        while actual is not None:
            ventas.append(actual.datos)
            actual = actual.siguiente
        return ventas
    
    def buscar_por_id(self, id_buscar):
        actual = self.cabeza
        while actual is not None:
            if actual.datos[0] == id_buscar:
                return actual.datos
            actual = actual.siguiente
        return None
    
    def modificar_venta(self, id_modificar, nuevo_producto, nueva_cantidad, nuevo_precio):
        actual = self.cabeza
        while actual is not None:
            if actual.datos[0] == id_modificar:
                if nuevo_producto:
                    actual.datos[1] = nuevo_producto
                if nueva_cantidad is not None:
                    actual.datos[2] = nueva_cantidad
                if nuevo_precio is not None:
                    actual.datos[3] = nuevo_precio
                return True
            actual = actual.siguiente
        return False
    
    def eliminar_venta(self, id_eliminar):
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
    
    def obtener_max_id(self):
        if self.esta_vacia():
            return 0
        max_id = 0
        actual = self.cabeza
        while actual is not None:
            try:
                id_actual = int(actual.datos[0])
                if id_actual > max_id:
                    max_id = id_actual
            except ValueError:
                continue
            actual = actual.siguiente
        return max_id
    
    def calcular_totales(self):
        total_ingresos = 0
        total_ventas = 0
        actual = self.cabeza
        
        while actual is not None:
            try:
                cantidad = int(actual.datos[2])
                precio = float(actual.datos[3])
                total_venta = cantidad * precio
                total_ingresos += total_venta
                total_ventas += 1
            except ValueError:
                continue
            actual = actual.siguiente
        
        return total_ingresos, total_ventas

class SistemaVentas:
    def __init__(self):
        self.archivo_csv = "info.csv"
        self.lista_ventas = ListaEnlazadaVentas()
        self.inicializar_archivo()
        self.cargar_datos()
    
    def inicializar_archivo(self):
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'producto', 'cantidad', 'precio_unitario', 'fecha'])
    
    def cargar_datos(self):
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Saltar cabecera si existe
                try:
                    header = next(reader)
                except StopIteration:
                    # Archivo vacío
                    return
                
                for row in reader:
                    if row and len(row) >= 4:
                        # Asegurar que tenemos 5 columnas
                        if len(row) == 4:
                            row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        self.lista_ventas.agregar_venta(row)
        except FileNotFoundError:
            print("Archivo no encontrado, se creará uno nuevo.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def guardar_datos(self):
        try:
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'producto', 'cantidad', 'precio_unitario', 'fecha'])
                
                ventas = self.lista_ventas.obtener_todas_ventas()
                for venta in ventas:
                    writer.writerow(venta)
        except Exception as e:
            print(f"Error al guardar datos: {e}")
    
    def crear_venta(self):
        print("\n--- CREAR NUEVA VENTA ---")
        
        # Generar ID automático
        nuevo_id = self.lista_ventas.obtener_max_id() + 1
        
        producto = input("Producto: ").strip()
        if not producto:
            print("Error: El producto no puede estar vacío.")
            return
        
        try:
            cantidad = int(input("Cantidad: "))
            precio_unitario = float(input("Precio unitario: "))
            
            if cantidad <= 0 or precio_unitario <= 0:
                print("Error: La cantidad y el precio deben ser mayores a 0.")
                return
                
        except ValueError:
            print("Error: La cantidad y el precio deben ser números válidos.")
            return
        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        nueva_venta = [
            str(nuevo_id), producto, str(cantidad), str(precio_unitario), fecha
        ]
        
        self.lista_ventas.agregar_venta(nueva_venta)
        self.guardar_datos()
        
        total_venta = cantidad * precio_unitario
        print(f"✓ Venta creada exitosamente (ID: {nuevo_id})")
        print(f"  Total: ${total_venta:.2f}")
    
    def listar_ventas(self):
        print("\n--- LISTA DE VENTAS ---")
        
        ventas = self.lista_ventas.obtener_todas_ventas()
        
        if not ventas:
            print("No hay ventas registradas.")
            return
        
        print(f"{'ID':<5} {'Producto':<20} {'Cantidad':<10} {'Precio Unit.':<12} {'Total':<12} {'Fecha':<16}")
        print("-" * 80)
        
        for venta in ventas:
            try:
                cantidad = int(venta[2])
                precio = float(venta[3])
                total = cantidad * precio
                fecha_corta = venta[4].split(' ')[0] if len(venta) > 4 else "N/A"
                print(f"{venta[0]:<5} {venta[1]:<20} {cantidad:<10} ${precio:<11.2f} ${total:<11.2f} {fecha_corta:<16}")
            except ValueError:
                print(f"{venta[0]:<5} {venta[1]:<20} Error en datos")
    
    def buscar_por_id(self):
        print("\n--- BUSCAR VENTA POR ID ---")
        
        if self.lista_ventas.esta_vacia():
            print("No hay ventas registradas.")
            return
        
        try:
            id_buscar = input("Ingrese el ID a buscar: ").strip()
            
            venta = self.lista_ventas.buscar_por_id(id_buscar)
            if not venta:
                print(f"No se encontró ninguna venta con ID: {id_buscar}")
                return
            
            try:
                cantidad = int(venta[2])
                precio = float(venta[3])
                total = cantidad * precio
                fecha = venta[4] if len(venta) > 4 else "N/A"
                
                print("\n✓ Venta encontrada:")
                print(f"ID: {venta[0]}")
                print(f"Producto: {venta[1]}")
                print(f"Cantidad: {cantidad}")
                print(f"Precio unitario: ${precio:.2f}")
                print(f"Total: ${total:.2f}")
                print(f"Fecha: {fecha}")
            except ValueError:
                print("Error: Datos de venta corruptos.")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def modificar_venta(self):
        print("\n--- MODIFICAR VENTA ---")
        
        if self.lista_ventas.esta_vacia():
            print("No hay ventas registradas.")
            return
        
        self.listar_ventas()
        
        try:
            id_modificar = input("\nIngrese el ID de la venta a modificar: ").strip()
            
            venta = self.lista_ventas.buscar_por_id(id_modificar)
            if not venta:
                print(f"No se encontró ninguna venta con ID: {id_modificar}")
                return
            
            try:
                cantidad_actual = int(venta[2])
                precio_actual = float(venta[3])
                total_actual = cantidad_actual * precio_actual
                
                print(f"\nVenta actual: {venta[1]} - Cantidad: {cantidad_actual} - Precio: ${precio_actual:.2f} - Total: ${total_actual:.2f}")
                
                nuevo_producto = input("Nuevo producto (Enter para mantener actual): ").strip()
                nueva_cantidad = None
                nuevo_precio = None
                
                input_cantidad = input("Nueva cantidad (Enter para mantener actual): ").strip()
                if input_cantidad:
                    nueva_cantidad = int(input_cantidad)
                    if nueva_cantidad <= 0:
                        print("La cantidad debe ser mayor a 0")
                        return
                
                input_precio = input("Nuevo precio unitario (Enter para mantener actual): ").strip()
                if input_precio:
                    nuevo_precio = float(input_precio)
                    if nuevo_precio <= 0:
                        print("El precio debe ser mayor a 0")
                        return
                
                if self.lista_ventas.modificar_venta(id_modificar, nuevo_producto, nueva_cantidad, nuevo_precio):
                    self.guardar_datos()
                    print("✓ Venta modificada exitosamente")
                else:
                    print("Error al modificar la venta")
                    
            except ValueError:
                print("Error: Ingrese valores numéricos válidos")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def eliminar_venta(self):
        print("\n--- ELIMINAR VENTA ---")
        
        if self.lista_ventas.esta_vacia():
            print("No hay ventas registradas.")
            return
        
        self.listar_ventas()
        
        try:
            id_eliminar = input("\nIngrese el ID de la venta a eliminar: ").strip()
            
            venta = self.lista_ventas.buscar_por_id(id_eliminar)
            if not venta:
                print(f"No se encontró ninguna venta con ID: {id_eliminar}")
                return
            
            try:
                cantidad = int(venta[2])
                precio = float(venta[3])
                total = cantidad * precio
                
                print(f"\nVenta a eliminar: {venta[1]} - Cantidad: {cantidad} - Precio: ${precio:.2f} - Total: ${total:.2f}")
                
                confirmacion = input("¿Está seguro de eliminar esta venta? (s/n): ").strip().lower()
                if confirmacion == 's':
                    if self.lista_ventas.eliminar_venta(id_eliminar):
                        self.guardar_datos()
                        print("✓ Venta eliminada exitosamente")
                    else:
                        print("Error al eliminar la venta")
                else:
                    print("Eliminación cancelada")
                    
            except ValueError:
                print("Error: Datos de venta corruptos")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def calcular_totales(self):
        print("\n--- TOTALES ---")
        
        if self.lista_ventas.esta_vacia():
            print("No hay ventas registradas.")
            return
        
        total_ingresos, total_ventas = self.lista_ventas.calcular_totales()
        
        print(f"Total de ventas realizadas: {total_ventas}")
        print(f"Ingreso total: ${total_ingresos:.2f}")
        
        # Mostrar promedio por venta
        if total_ventas > 0:
            promedio = total_ingresos / total_ventas
            print(f"Promedio por venta: ${promedio:.2f}")
    
    def mostrar_menu(self):
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE GESTIÓN DE VENTAS")
            print("="*50)
            print("1. Crear nueva venta")
            print("2. Listar ventas")
            print("3. Buscar por ID")
            print("4. Modificar venta")
            print("5. Eliminar venta")
            print("6. Calcular totales")
            print("7. Salir")
            print("="*50)
            
            try:
                opcion = input("Seleccione una opción (1-7): ").strip()
                
                if opcion == "1":
                    self.crear_venta()
                elif opcion == "2":
                    self.listar_ventas()
                elif opcion == "3":
                    self.buscar_por_id()
                elif opcion == "4":
                    self.modificar_venta()
                elif opcion == "5":
                    self.eliminar_venta()
                elif opcion == "6":
                    self.calcular_totales()
                elif opcion == "7":
                    print("¡Gracias por usar el sistema!")
                    break
                else:
                    print("Opción no válida. Por favor, seleccione 1-7")
                    
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    sistema = SistemaVentas()
    sistema.mostrar_menu()