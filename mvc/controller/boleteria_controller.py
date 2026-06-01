from typing import Optional

from model.ticket import Ticket
from service.evento_service import EventoService
from service.ticket_service import TicketService


class BoleteriaController:
    """Controlador del modulo de cajero/boleteria."""

    def __init__(
        self,
        evento_service: Optional[EventoService] = None,
        ticket_service: Optional[TicketService] = None) -> None:
        self.evento_service = evento_service or EventoService()
        self.ticket_service = ticket_service or TicketService()

# ------------------------------------------------------------------

    def listar_eventos(self):
        return self.evento_service.listar_eventos()

# ------------------------------------------------------------------

    def detalle_evento(self, evento_id: int):
        return self.evento_service.obtener_evento(evento_id)

# ------------------------------------------------------------------

    def asientos_disponibles(self, evento_id: int):
        return self.ticket_service.asientos_disponibles(evento_id)

# ------------------------------------------------------------------

    def vender_ticket(
        self,
        evento_id: int,
        zona: str,
        metodo_pago: str) -> tuple[bool, str, Optional[Ticket]]:
        return self.ticket_service.vender_ticket(
            evento_id=evento_id,
            zona=zona,
            metodo_pago=metodo_pago,
            usuario_id=None
        )

