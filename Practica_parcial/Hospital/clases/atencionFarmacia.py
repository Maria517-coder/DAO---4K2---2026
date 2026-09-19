from atencion import Atencion

class AtencionFarmacia(Atencion):
    def __init__(self, codigo, tipoDeCobro, importe, descuento):
        super().__init__(codigo, tipoDeCobro)
        self.importe = importe
        self.descuento = descuento

    # --- IMPORTE TOTAL ---
    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, valor):
        self._importe = float(valor)
        

    # --- DESCUENTO (CUPÓN) ---
    @property
    def descuento(self):
        return self._descuento

    # Acá agregamos la validación de si el cupon de descuento es mayor a cero
    
    @descuento.setter
    def descuento(self, valor):
        if valor > 0:
            self._descuento = float(valor)
        else:
            raise ValueError("El descuento debe ser mayor a cero.")

    def importeACobrar(self):
        monto = self.importe
        monto - self.descuento if self.descuento > 0 else 0 
        if self.tipoDeCobro == 1:
            monto = monto * 0.95
        if self.tipoDeCobro == 2:
            monto = monto * 1.3

        return monto

            