from .usuario import Usuario

class Estudiante:
    def __init__(self, id=None, matricula=None, usuario: Usuario = None, created_at=None):
        self.id = id
        self.matricula = matricula
        self.usuario = usuario  # Instancia de Usuario
        self.created_at = created_at
