import json
import os
from typing import List, Optional, Dict, Any

import requests

COUNTRY = "PAN"
INDICATOR = "SH.IMM.MEAS"
WB_URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}?format=json&per_page=20000"
CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "local_cache.json")

class WorldBankService:
    def __init__(self) -> None:
        self._data = self._load_data()

    # ---------- Public API ----------
    def all(self) -> List[Dict[str, Any]]:
        return self._data

    def by_year(self, year: int) -> Optional[Dict[str, Any]]:
        for row in self._data:
            if row["year"] == year:
                return row
        return None

    def latest_year(self) -> Optional[int]:
        years = [r["year"] for r in self._data if r.get("value") is not None]
        return max(years) if years else None

    # ---------- Internal ----------
    def _load_data(self) -> List[Dict[str, Any]]:
        refresh = os.getenv("WB_REFRESH") == "1"
        if refresh:
            try:
                data = self._fetch_remote()
                if os.getenv("WB_WRITE_CACHE") == "1":
                    self._write_cache(data)
                return data
            except Exception:
                # Si falla el fetch, caemos al cache local
                pass
        # cache local
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        # última opción: intentar remoto una vez
        try:
            return self._fetch_remote()
        except Exception:
            # sin datos
            return []

    def _fetch_remote(self) -> List[Dict[str, Any]]:
        resp = requests.get(WB_URL, timeout=20)
        resp.raise_for_status()
        payload = resp.json()
        if not isinstance(payload, list) or len(payload) < 2:
            raise RuntimeError("Respuesta inesperada del Banco Mundial")
        rows = payload[1]
        data = []
        for r in rows:
            # 'date' es string con el año
            try:
                year = int(r.get("date"))
            except Exception:
                continue
            val = r.get("value")  # puede ser None
            if val is not None:
                try:
                    val = float(val)
                except Exception:
                    val = None
            data.append({
                "country": COUNTRY,
                "indicator": INDICATOR,
                "year": year,
                "value": val,
            })
        # ordenar por año asc
        data.sort(key=lambda x: x["year"])
        return data

    def _write_cache(self, data: List[Dict[str, Any]]) -> None:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
