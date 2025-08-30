class P:
    def read(self,filename):
        with open(filename, "r", encoding="utf-8") as p:
            for linea in p:
                print (linea.strip())
    def write(self,filename, dictionary):
        enable = 1
        id = 1
        with open(filename, "w", encoding="utf-8") as p:
            labels = list(dictionary[0].keys())
            p.write("id,")
            for label in labels:
                p.write(label + ",")
            p.write("status"+"\n")
            for a in dictionary:
                count = 0
                p.write(str(id)+",")
                for d in a.values():
                    p.write(str(id)+",")
                    for d in a.values():
                        p.write(d )
                        count+=1
                        p.write(",")
                    id+=1
                    p.write(str(enable)+"\n")
def delete (self,filname,id):
    list = []
    with open(filename,"r",encoding="utf-8") as p:
        list = P.readlines()
    newList = []
    for l in list:
        arr = l.split(',')
        if str(arr[0]) == str(id):
            print (id)
            arr[len(arr)-1] = "0"
            ll = ""
            count = 1
            for a in arr:
                ll = ll + str(a)
                if count <len(arr):
                    ll = ll + ","
                count +=1
            l = ll + "\n"
        newList.append(l)
    self.write_array(filename, newList)
def write_array(self, filename, list):
    with open(filename,"r",encoding="utf-8") as p:
        for l in list:
            p.write(l)
        



people = [{"name":"Juan","lastname":"lopez"},
{"name":"Juan","lastname":"lopez"},
{"name":"Juan","lastname":"lopez"}]

def sequential_search_file(filename, value,param):
    index_param = -1
    with open(filename, "r") as file:
       for i, line in enumerate(file):
           arr = line.split(",")
           if (i == 0):
               try:
                   index_param = arr.index(param)
               except Exception:
                   return " no encontré la columna"+ param
           elif arr [index_param]== value:
               return arr
    return -1

p = P()
p.write("datos.txt", people)