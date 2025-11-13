class Node:
    def __init__(self, id, name, lat=None, lon=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.next = None
        self.sub_list = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, id, name, lat=None, lon=None):
        new_node = Node(id, name, lat, lon)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        return new_node

    def find(self, id):
        current = self.head
        while current:
            if current.id == id:
                return current
            current = current.next
        return None

    def to_dict(self):
        result = []
        current = self.head
        while current:
            d = {"id": current.id, "name": current.name}
            if current.lat and current.lon:
                d["lat"] = current.lat
                d["lon"] = current.lon
            if current.sub_list:
                d["children"] = current.sub_list.to_dict()
            result.append(d)
            current = current.next
        return result
