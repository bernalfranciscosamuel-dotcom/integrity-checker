import hashlib
from pathlib import Path


def hash_file(path):
    """Calcula el hash SHA-256 de un archivo y lo devuelve como texto."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        # Leemos en bloques de 64 KB para no cargar archivos grandes en memoria
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()