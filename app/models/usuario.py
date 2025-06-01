class Usuario:
    def __init__(self, id=None, nombre=None, apellido=None, cedula=None, email=None, username=None, password_hash=None, rol=None, created_at=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.created_at = created_at
