class Tienda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = {}  # Un diccionario para almacenar productos (nombre -> precio)
        self.clientes = []   # Una lista para almacenar los clientes

    def agregar_producto(self, nombre, precio):
        self.productos[nombre] = precio

    def listar_productos(self):
        print(f"Productos en la tienda {self.nombre}:")
        for nombre, precio in self.productos.items():
            print(f"{nombre}: ${precio}")

    def agregar_cliente(self, nombre):
        self.clientes.append(nombre)

    def listar_clientes(self):
        print(f"Clientes de la tienda {self.nombre}:")
        for cliente in self.clientes:
            print(cliente)

# Crear una instancia de la clase Tienda
mi_tienda = Tienda("Mi Tienda")

# Agregar productos
mi_tienda.agregar_producto("Camiseta", 15)
mi_tienda.agregar_producto("Pantalón", 30)
mi_tienda.agregar_producto("Zapatos", 50)

# Listar productos
mi_tienda.listar_productos()

# Agregar clientes
mi_tienda.agregar_cliente("Juan")
mi_tienda.agregar_cliente("Ana")
mi_tienda.agregar_cliente("Carlos")

# Listar clientes
mi_tienda.listar_clientes()
