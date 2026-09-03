class Producto:
    def __init__(self, codigo, descripcion, precio, stock):
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"Código del producto: {self.codigo} - Descripción: {self.descripcion} - Precio: {self.precio} - Stock: {self.stock}"
    

    def hay_stock(self):
        if self.stock > 0:
            return True
        
    def valor_stock(self):
        total = self.stock * self.precio
        return total
    

def principal():
    prod_1 = Producto(123, "Shampoo", 5000, 12)
    prod_2 = Producto(1234, "Jabón Dove", 3000, 30)

    print(prod_1)
    print(prod_2)

    print(prod_1.hay_stock())
    print(prod_2.valor_stock())

if "__main__" == __name__:
    principal()

