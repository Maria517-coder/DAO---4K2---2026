class Libro:
    def __init__(self, titulo, autor, cant_pag, estado_prestamo):
        self.titulo = titulo
        self.autor = autor
        self.cant_pag = cant_pag
        self.estado_prestamo = estado_prestamo

    def __str__(self):
        return f"Titulo: {self.titulo} Autor: {self.autor} Cantidad de páginas: {self.cant_pag} Estado del prestamo: {self.estado_prestamo }"
    
    def prestar(self):
        if self.estado_prestamo == True:
            print("Este libro ya se encuentra prestado")
        else:
            self.estado_prestamo = True
            print("Prestamo aplicado correctamente!!")


def principal():
    libro_1 = Libro("Caperucita Roja", "H Grimm", 50, False)
    print(libro_1)
    libro_1.prestar()
    print(libro_1)

if "__main__" == __name__:
    principal()