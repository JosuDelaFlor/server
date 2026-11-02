class DomainError(Exception):
    """Clase base para todos los errores de dominio"""
    pass

class RconConnectionError(DomainError):
    def __init__(self, message: str = "No se pudo conectar al servidor RCON"):
        super().__init__(message)

class RconAuthenticationError(DomainError):
    def __init__(self, message: str = "Error de autenticación RCON"):
        super().__init__(message)