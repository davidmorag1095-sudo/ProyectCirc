from typing import Optional


class Ticket:
    def __init__(
        self,
        identificador: int,
        evento_id: int,
        usuario_id: Optional[int],
        zona: str,
        numero_asiento: int,
        precio: float,
        fecha_compra: str,
        metodo_pago: str) -> None:

        self.identificador = identificador
        self.evento_id = evento_id
        self.usuario_id = usuario_id
        self.zona = zona
        self.numero_asiento = numero_asiento
        self.precio = precio
        self.fecha_compra = fecha_compra
        self.metodo_pago = metodo_pago

    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "identificador": self.identificador,
            "evento_id": self.evento_id,
            "usuario_id": self.usuario_id,
            "zona": self.zona,
            "numero_asiento": self.numero_asiento,
            "precio": self.precio,
            "fecha_compra": self.fecha_compra,
            "metodo_pago": self.metodo_pago}

    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        usuario_id = None
        if data.get("usuario_id") is not None:
            usuario_id = int(data["usuario_id"])

        return cls(
            identificador=int(data.get("identificador", 0)),
            evento_id=int(data.get("evento_id", 0)),
            usuario_id=usuario_id,
            zona=data.get("zona", "General"),
            numero_asiento=int(data.get("numero_asiento", 0)),
            precio=float(data.get("precio", 0.0)),
            fecha_compra=data.get("fecha_compra", ""),
            metodo_pago=data.get("metodo_pago", "Sin especificar"))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Ticket(identificador={self.identificador!r}, evento_id={self.evento_id!r}, "
            f"zona={self.zona!r}, numero_asiento={self.numero_asiento!r}, precio={self.precio!r})")
