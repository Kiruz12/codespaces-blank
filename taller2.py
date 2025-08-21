def search_name():
    name_search = input("Ingrese el nombre del cliente: ").strip().title()
    try:
        with open('datos.txt','r',encoding='utf-8') as archivo:
            lineas = archivo.readlines()

            encontrado = False  
            for linea in lineas:
                if not linea.strip() or linea.startswith('Cedula'):
                    continue  

                datos = linea.strip().split(',')

                if len(datos)>=3:
                    cedula = datos[0].strip()
                    nombre = datos[1].strip().title()
                    saldo = datos[2].strip()

                    if nombre == name_search:
                        print(f"\n=== INFORMACIÓN DEL CLIENTE ===")
                        print(f"Nombre: {nombre}")
                        print(f"Cédula: {cedula}")
                        print(f"Saldo: ${float(saldo):.2f}")
                        encontrado = True
                        break  
            
            if not encontrado:
                print(f"\nNo se encontró ningún cliente con el nombre '{name_search}'")
                
    except FileNotFoundError:
        print("Error: El archivo 'datos.txt' no existe")
    except ValueError:
        print("Error: Formato de saldo inválido en el archivo")
    except Exception as e:
        print(f"Error inesperado: {e}")

def saldos50():
    try:
        with open('datos.txt', 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            
            contador = 0
            
            
            for linea in lineas:
                if not linea.strip() or linea.startswith('Cedula'):
                    continue
                
                datos = linea.strip().split(',')
                
                if len(datos) >= 3:
                    try:
                        saldo = float(datos[2].strip())
                        if saldo > 50:
                            contador += 1
                    except ValueError:
                        continue 
            
            print(f"\nCLIENTES CON SALDO MAYOR A 50")
            print(f"Total de clientes: {contador}")
    except FileNotFoundError:
        print("Error: El archivo 'datos.txt' no existe.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def ordensaldo():
    try:
        with open('datos.txt', 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            
            clientes = []
            
            for linea in lineas:
                try:
                    if not linea.strip() or linea.startswith(('Cedula', 'Cédula')):
                        continue
                    
                    datos = linea.strip().split(',')
                    if len(datos) >= 3:
                        nombre = datos[1].strip().title()
                        saldo = float(datos[2].strip())
                        clientes.append((nombre, saldo))
                        
                except (ValueError, IndexError):
                    continue
            
            def obtener_saldo(cliente):
                return cliente[1]
            
            clientes_ordenados = sorted(clientes, key=obtener_saldo)
            
            print(f"\nNOMBRES ORDENADOS POR SALDO")
            
            for nombre, saldo in clientes_ordenados:
                print(f"{nombre} {saldo:.2f}")
                
    except FileNotFoundError:
        print("El archivo 'datos.txt' no existe.")
    except Exception as e:
        print(f"Error: {e}")

def menu():
 print("\nOpciones:")
 print("1. Buscar cliente por nombre")
 print("2. Contar clientes con saldo mayor a 50")
 print("3. Mostrar clientes ordenados por saldo")

 try:
    n = int(input("\nSeleccione una opción (1-3): ").strip())
    
    if n == 1:
        search_name()
    elif n == 2:
        saldos50()
    elif n == 3:
        ordensaldo()
    else:
        print("Opción inválida")
        
 except ValueError:
    print("Error: Debe ingresar un número")
 except Exception as e:
    print(f"Error: {e}")

menu()
