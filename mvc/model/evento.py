from typing import Dict


class Evento:
    def __init__(
        self,
        identificador: int,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        descripcion: str,
        precios_por_zona: Dict[str, float],
        capacidad_por_zona: Dict[str, int]) -> None:

        self.identificador = identificador
        self.nombre = nombre
        self.categoria = categoria
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.duracion_minutos = duracion_minutos
        self.descripcion = descripcion
        self.precios_por_zona = precios_por_zona
        self.capacidad_por_zona = capacidad_por_zona

    def to_dict(self) -> dict:
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "duracion_minutos": self.duracion_minutos,
            "descripcion": self.descripcion,
            "precios_por_zona": self.precios_por_zona,
            "capacidad_por_zona": self.capacidad_por_zona}
#------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "Evento":
        return cls(
            identificador=int(data.get("identificador", 0)),
            nombre=data.get("nombre", "").strip(),
            categoria=data.get("categoria", "General").strip() or "General",
            fecha=data.get("fecha", "").strip(),
            hora_inicio=data.get("hora_inicio", "").strip(),
            duracion_minutos=int(data.get("duracion_minutos", 0)),
            descripcion=data.get("descripcion", "").strip(),
            precios_por_zona=dict(data.get("precios_por_zona", {})),
            capacidad_por_zona=dict(data.get("capacidad_por_zona", {})))

    # --------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Evento(identificador={self.identificador!r}, nombre={self.nombre!r}, "
            f"fecha={self.fecha!r}, hora_inicio={self.hora_inicio!r})")
