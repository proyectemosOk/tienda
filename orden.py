class Orden:
    def __init__(self, nombre, telefono, correo, tipo, marca, modelo,
                 estado_entrada, servicios, perifericos, observaciones):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.estado_entrada = estado_entrada
        self.servicios = servicios
        self.perifericos = perifericos
        self.observaciones = observaciones

    def a_dict(self):
        return self.__dict__
