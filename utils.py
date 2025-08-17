import hashlib
from typing import Optional

PROVINCES = [
    "Bocas del Toro",
    "Coclé",
    "Colón",
    "Chiriquí",
    "Darién",
    "Herrera",
    "Los Santos",
    "Panamá",
    "Panamá Oeste",
    "Veraguas",
    "Guna Yala",
    "Emberá",
    "Ngäbe-Buglé",
]

def clamp(v: Optional[float], minv: float = 0.0, maxv: float = 100.0) -> Optional[float]:
    if v is None:
        return None
    return max(minv, min(maxv, v))

def deterministic_offset(province: str, year: int, spread: float = 0.07) -> float:
    """
    Retorna un delta determinístico en el rango [-spread, +spread] para una provincia y año.
    spread=0.07 => ±7 puntos porcentuales como máximo.
    """
    seed = f"{province}|{year}".encode("utf-8")
    h = hashlib.sha256(seed).hexdigest()
    # map hex -> [0,1)
    r = int(h[:12], 16) / float(16**12)
    # shift to [-1,1] then scale
    return (r * 2 - 1) * spread
