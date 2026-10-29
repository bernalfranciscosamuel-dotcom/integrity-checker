import hashlib
import json
from pathlib import Path


def hash_file(path):
    """Calcula el hash SHA-256 de un archivo y lo devuelve como texto."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        # Leemos en bloques de 64 KB para no cargar archivos grandes en memoria
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()


def hash_directory(directory):
    """Devuelve un diccionario {ruta_relativa: hash} con todos los archivos de una carpeta."""
    directory = Path(directory)
    hashes = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            hashes[relative] = hash_file(path)
    return hashes


def save_baseline(directory, output="baseline.json"):
    """Guarda la línea base (los hashes actuales) en un archivo JSON."""
    hashes = hash_directory(directory)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, sort_keys=True)
    return hashes


def compare_baseline(directory, baseline_path="baseline.json"):
    """Compara la carpeta actual con la línea base y devuelve los cambios."""
    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    current = hash_directory(directory)

    removed = sorted(set(baseline) - set(current))
    added = sorted(set(current) - set(baseline))
    modified = sorted(
        name
        for name in (set(baseline) & set(current))
        if baseline[name] != current[name]
    )

    return {"modified": modified, "removed": removed, "added": added}