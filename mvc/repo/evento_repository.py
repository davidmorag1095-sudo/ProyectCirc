from pathlib import Path
from typing import List, Optional

from model.evento import Evento
from repo.base_repository import BaseRepository


class EventoRepository(BaseRepository[Evento]):
    def __init__(self, archivo_json: Optional[Path] = None) -> None:
        ruta = archivo_json or (Path(__file__).resolve().parent.parent / "data" / "eventos.json")
        super().__init__(ruta, Evento)

    # ------------------------------------------------------------------
    def obtener_por_fecha(self, fecha: str) -> List[Evento]:
        eventos_filtrados = []
        for evento in self.get_all():
            if evento.fecha == fecha:
                eventos_filtrados.append(evento)
        return eventos_filtrados

    # ------------------------------------------------------------------
    def obtener_por_nombre(self, nombre: str) -> Optional[Evento]:
        nombre_buscado = nombre.strip().lower()
        for evento in self.get_all():
            if evento.nombre.lower() == nombre_buscado:
                return evento
        return None

    # ------------------------------------------------------------------
    def obtener_ultimo_id(self) -> int:
        ultimo_id = 0
        for evento in self.get_all():
            if evento.identificador > ultimo_id:
                ultimo_id = evento.identificador
        return ultimo_id

