class Client:
    def __init__(self, id, name, surname):
        self.id = id
        self.name = name
        self.surname = surname
        self.active = True

    def display_info(self):
        status = "Active" if self.active else "Inactive"
        return f"ID: {self.id} | {self.name} {self.surname} | estado: {status}"


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._next_id = 1

    def add(self, name, surname):
        new_client = Client(self._next_id, name, surname)
        self._next_id += 1
        new_node = Node(new_client)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return new_client

    def traverse(self):
        clients = []
        current = self.head
        while current:
            clients.append(current.data)
            current = current.next
        return clients

    def find_by_id(self, cid):



def main_menu():
    client_list = DoublyLinkedList()
    while True:
        print("\nMenú:")
        print("1. Registrar Cliente")
        print("2. Lista Clientes")
        print("3. Eliminar Cliente")
        print("4. Salir")
        choice = input("Elige una opción: ")
        if choice == '1':
            name = input("Ingresa nombre del cliente: ")
            surname = input("Ingresa el apellido del cliente: ")
            client = client_list.add(name, surname)
            print(f"Cliente registrado. ID asignado: {client.id}")
        elif choice == '2':
            print("Clientes:")
            for client in client_list.traverse():
                print(client.display_info())
        elif choice == '3':
            cid = int(input("Ingresa el ID del cliente que quieres eliminar: "))
            client = client_list.find_by_id(cid)
            client.active = False
            print(f"Cliente {client.name} {client.surname} (ID {client.id}) fue eliminado.")
        elif choice == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main_menu()
