from pathlib import Path
from typing import List, Optional

from model.ticket import Ticket
from repo.base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, archivo_json: Optional[Path] = None) -> None:
        ruta = archivo_json or (Path(__file__).resolve().parent.parent / "data" / "tickets.json")
        super().__init__(ruta, Ticket)

    # ------------------------------------------------------------------
    def obtener_ultimo_id(self) -> int:
        ultimo_id = 0
        for ticket in self.get_all():
            if ticket.identificador > ultimo_id:
                ultimo_id = ticket.identificador
        return ultimo_id

    # ------------------------------------------------------------------
    def obtener_por_evento(self, evento_id: int) -> List[Ticket]:
        tickets_evento = []
        for ticket in self.get_all():
            if ticket.evento_id == evento_id:
                tickets_evento.append(ticket)
        return tickets_evento

    # ------------------------------------------------------------------
    def obtener_por_evento_y_zona(self, evento_id: int, zona: str) -> List[Ticket]:
        zona_buscada = zona.strip().lower()
        tickets_filtrados = []
        for ticket in self.get_all():
            if ticket.evento_id == evento_id and ticket.zona.lower() == zona_buscada:
                tickets_filtrados.append(ticket)
        return tickets_filtrados

    # ------------------------------------------------------------------
    def obtener_por_usuario(self, usuario_id: int) -> List[Ticket]:
        tickets_usuario = []
        for ticket in self.get_all():
            if ticket.usuario_id == usuario_id:
                tickets_usuario.append(ticket)
        return tickets_usuario

    # ------------------------------------------------------------------
    def obtener_por_zona(self, zona: str) -> List[Ticket]:
        zona_buscada = zona.strip().lower()
        tickets_zona = []
        for ticket in self.get_all():
            if ticket.zona.lower() == zona_buscada:
                tickets_zona.append(ticket)
        return tickets_zona

