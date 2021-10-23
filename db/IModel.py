class IModel:
    """ Modelo para los metodos de las consutlas """

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        pass

    def create(self, params) -> int:
        """Crear un registro"""
        pass

    def edit(self, params) -> int:
        """Editar los registros"""
        pass

    def delete(self, id) -> int:
        """Eliminar un registro"""
        pass
