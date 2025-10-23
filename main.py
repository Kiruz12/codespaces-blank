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


class LinkedList:
    def __init__(self):
        self.head = None
        self._next_id = 1

    def add(self, name, surname):
        new_client = Client(self._next_id, name, surname)
        self._next_id += 1
        new_node = Node(new_client)
        new_node.next = self.head
        self.head = new_node
        return new_client

    def traverse(self):
        clients = []
        current = self.head
        while current:
            clients.append(current.data)
            current = current.next
        return clients

    def find_by_name_surname(self, name, surname):
        current = self.head
        while current:
            c = current.data
            if c.name == name and c.surname == surname:
                return current.data
            current = current.next
        return None

    def find_by_id(self, cid):
        current = self.head
        


def main_menu():
    client_list = LinkedList()

    while True:
        print("\nMenú:")
        print("1. Registrar Cliente")
        print("2. Lista Clientes")
        print("3. Eliminar Cliente")

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


        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main_menu()
