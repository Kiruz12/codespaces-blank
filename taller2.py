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
        print("Error: El archivo 'datos.txt' no existe.")
    except ValueError:
        print("Error: Formato de saldo inválido en el archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")
search_name()