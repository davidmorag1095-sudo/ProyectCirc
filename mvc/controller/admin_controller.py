from typing import Optional

from model.evento import Evento
from service.evento_service import EventoService
from service.ticket_service import TicketService


class AdminController:
    """Controlador principal del modulo de administrador."""

    def __init__(
        self,
        evento_service: Optional[EventoService] = None,
        ticket_service: Optional[TicketService] = None ) -> None:
        self.evento_service = evento_service or EventoService()
        self.ticket_service = ticket_service or TicketService()
#------------------------------------------------------------------
    def programar_evento(
        self,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        descripcion: str) -> tuple[bool, str, Optional[Evento]]:
        return self.evento_service.programar_evento(
            nombre=nombre,
            categoria=categoria,
            fecha=fecha,
            hora_inicio=hora_inicio,
            duracion_minutos=duracion_minutos,
            descripcion=descripcion
        )

# ------------------------------------------------------------------

    def actualizar_precios(
        self,
        evento_id: int,
        precio_general: float,
        precio_preferencial: float,
        precio_vip: float) -> tuple[bool, str]:
        return self.evento_service.actualizar_precios(
            evento_id,
            precio_general,
            precio_preferencial,
            precio_vip
        )

# ------------------------------------------------------------------

    def actualizar_evento(
        self,
        evento_id: int,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        descripcion: str) -> tuple[bool, str]:
        return self.evento_service.actualizar_evento(
            evento_id=evento_id,
            nombre=nombre,
            categoria=categoria,
            fecha=fecha,
            hora_inicio=hora_inicio,
            duracion_minutos=duracion_minutos,
            descripcion=descripcion
        )

# ------------------------------------------------------------------

    def aumentar_capacidad(
        self,
        evento_id: int,
        agregar_general: int,
        agregar_preferencial: int,
        agregar_vip: int) -> tuple[bool, str]:
        return self.evento_service.aumentar_capacidad(
            evento_id=evento_id,
            agregar_general=agregar_general,
            agregar_preferencial=agregar_preferencial,
            agregar_vip=agregar_vip
        )

# ------------------------------------------------------------------

    def eliminar_evento(self, evento_id: int) -> tuple[bool, str]:
        return self.evento_service.eliminar_evento(
            evento_id=evento_id,
            tiene_tickets=self.ticket_service.evento_tiene_tickets(evento_id)
        )

# ------------------------------------------------------------------

    def listar_eventos(self) -> list[Evento]:
        return self.evento_service.listar_eventos()

# ------------------------------------------------------------------

    def obtener_evento(self, evento_id: int) -> Optional[Evento]:
        return self.evento_service.obtener_evento(evento_id)

    def cargar_shows_demo(self) -> int:
        return self.evento_service.cargar_shows_demo()

    def generar_reporte_evento(self, evento_id: int) -> Optional[dict]:
        evento = self.evento_service.obtener_evento(evento_id)
        if evento is None:
            return None
        return self.ticket_service.reporte_evento(evento)

# ------------------------------------------------------------------

    def generar_reporte_general(self) -> dict:
        eventos = self.evento_service.listar_eventos()
        reporte = self.ticket_service.reporte_general(eventos)
        evento_top_id = reporte.get("evento_top_ocupacion_id")
        evento_top = None
        if evento_top_id:
            evento_top = self.evento_service.obtener_evento(evento_top_id)

        if evento_top is None:
            reporte["evento_top_nombre"] = "-"
        else:
            reporte["evento_top_nombre"] = evento_top.nombre
        return reporte

# ------------------------------------------------------------------

    def generar_reporte_por_fecha(self, fecha: str) -> dict:
        eventos = self.evento_service.listar_eventos()
        reporte = self.ticket_service.reporte_por_fecha(fecha, eventos)
        evento_top_id = reporte.get("evento_top_ocupacion_id")
        evento_top = None
        if evento_top_id:
            evento_top = self.evento_service.obtener_evento(evento_top_id)

        if evento_top is None:
            reporte["evento_top_nombre"] = "-"
        else:
            reporte["evento_top_nombre"] = evento_top.nombre
        return reporte

# ------------------------------------------------------------------

    def buscar_ticket(self, ticket_id: int):
        return self.ticket_service.obtener_ticket(ticket_id)

