from atencionMedica import AtencionMedica

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
        return self._consultas

    # Métodos

    def addAtencion(self, atencion):
        self._atencion.append(atencion)

    def es_atencion_Medica(self):
        es_Medica = [a for a in self.consultas if isinstance(a, AtencionMedica)]
        return es_Medica

    
    def importe_total_atencion_consulta(self):
        importe_total = 0
        for i in range(len(self._atencion)):
            if isinstance(self._atencion[i], AtencionMedica):
                importe_total += self._atencion[i].importe

        return importe_total


    def importe_promedio_atenciones(self):
        atenciones_medicas = list(filter(self.es_atencion_Medica, self._atencion))
        sup = int(input("Ingrese el monto máximo: "))
        inf = int(input("Ingrese el monto mínimo: "))
        for i in range(len(atenciones_medicas)):
            if   sup > atenciones_medicas[i].im > inf : 
                total += atenciones_medicas[i].importeACobrar()
                cont += 1

        if cont > 0:
            return total/cont
        
        return 0

    def codigo_primera_atencino_habitual(self):
        atenciones_medicas = list(filter(self.es_atencion_Medica, self._atencion))
        primero = next(x for x in atenciones_medicas if x.paciente.habitual == True)
        return primero.codigo