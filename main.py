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
            if c.name.strip().lower() == name.strip().lower() and c.surname.strip().lower() == surname.strip().lower():
                return current.data
            current = current.next
        return None

    def find_by_id(self, cid):
        current = self.head
        while current:
            c = current.data
            if c.id == cid:
                return current.data
            current = current.next
        return None

def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ingrese un número entero válido.")


def main_menu():
    client_list = LinkedList()

    while True:
        print("\nMenú:")
        print("1. Registrar Cliente")
        print("2. Lista Clientes")
        print("3. eliminar cliente")

        choice = input("elige una opcion: ").strip()

        if choice == '1':
            name = input("ingresa nombre del cliente: ").strip()
            surname = input("ingresa el apellido del cliente: ").strip()
            client = client_list.add(name, surname)
            print(f"Cliente registrado. ID asignado: {client.id}")

        elif choice == '2':
            print("Clientes:")
            any_client = False
            for client in client_list.traverse():
                any_client = True
                print(client.display_info())
            if not any_client:
                print("No hay clientes aún.")

        elif choice == '3':
            cid = input_int("Ingresa el ID del cliente que quiere eliminar: ")
            client = client_list.find_by_id(cid)
            if client:
                client.active = False
                print(f"Client {client.name} {client.surname} (ID {client.id}) fue eliminado.")
            else:
                print("Cliente no encontrado.")

        else:
            print("invalido.")


if __name__ == "__main__":
    main_menu()