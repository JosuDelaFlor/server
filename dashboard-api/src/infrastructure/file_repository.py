import os

from typing import Dict

from src.core.interfaces import IServerConfigRepository

class FileServerConfigRepositoryImpl(IServerConfigRepository):
    """Implementación real para leer y editar el archivo server.properties"""
    
    def __init__(self, file_path: str):
        # Inyectamos la ruta del archivo. Normalmente será "/server-data/server.properties"
        self.file_path = file_path

    def get_properties(self) -> Dict[str, str]:
        """Lee el archivo y devuelve un diccionario con las propiedades clave-valor."""
        properties = {}
        
        if not os.path.exists(self.file_path):
            return properties

        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar comentarios y líneas vacías
                if not line or line.startswith('#'):
                    continue
                
                # Separar por el primer '=' encontrado
                if '=' in line:
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()
                    
        return properties

    def update_property(self, key: str, value: str) -> bool:
        """
        Modifica una propiedad en el archivo. 
        Mantiene los comentarios y el orden original. Si la clave no existe, la añade al final.
        """
        if not os.path.exists(self.file_path):
            return False

        updated = False
        new_lines = []

        try:
            # 1. Leer el contenido actual
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 2. Procesar línea por línea
            for line in lines:
                stripped_line = line.strip()
                # Si la línea es nuestra clave, la reemplazamos
                if not stripped_line.startswith('#') and stripped_line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    new_lines.append(line)

            # 3. Si la clave no existía en el archivo, la añadimos al final
            if not updated:
                # Asegurarnos de que el archivo termina con un salto de línea antes de añadir
                if new_lines and not new_lines[-1].endswith('\n'):
                    new_lines[-1] += '\n'
                new_lines.append(f"{key}={value}\n")

            # 4. Sobrescribir el archivo con los nuevos datos
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
            return True

        except IOError:
            # Capturar errores de permisos o bloqueos de sistema operativo
            return False