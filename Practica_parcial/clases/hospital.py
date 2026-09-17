class Hospital:
    def __init__(self, razonSocial):
        self.razonSocial = razonSocial
        self.consultas = []

    @property
    def razonSocial(self):
        return self._razonSocial
    
    @razonSocial.setter
    def razonSocial(self, valor):
        self._razonSocial = str(valor)

# Solo getter para consulta; no lleva setter para no reemplazar la lista completa
    @property
    def consultas(self):
        return self.consultas

    def addAtencion(self, atencion):
        self._atencion.append(atencion)
    
    