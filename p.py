class P:
    def read(self,filename):
        with open(filename, "r", encoding="utf-8") as p:
            for linea in p:
                print (linea.strip())
    def write(self,filename):
        with open(filename, "w", encoding="utf-8") as p:
            p.write("encabezado\n")
            p.writelines(["linea 1", "linea 2", "linea 3", "linea 4"])
p = P()
p.write("datos.txt")
p.read("datos.txt")