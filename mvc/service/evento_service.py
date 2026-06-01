from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from model.evento import Evento
from repo.evento_repository import EventoRepository


class EventoService:
    """Logica de programacion y mantenimiento de shows."""

    CAPACIDAD_TOTAL = 40
    DISTRIBUCION_ZONAS = {
        "VIP": 10,
        "Preferencial": 15,
        "General": 15}
    PRECIO_MINIMO_GENERAL = 2500.0
    ZONAS_ORDEN = ("VIP", "Preferencial", "General")

    def __init__(self, repositorio: Optional[EventoRepository] = None) -> None:
        self.repositorio = repositorio or EventoRepository()

    # ------------------------------------------------------------------
    def _parse_fecha(self, fecha: str) -> datetime:
        return datetime.strptime(fecha.strip(), "%Y-%m-%d")

    # ------------------------------------------------------------------
    def _parse_hora(self, hora: str) -> datetime:
        hora_limpia = hora.strip()
        if ":" not in hora_limpia:
            hora_limpia = f"{int(hora_limpia):02d}:00"
        return datetime.strptime(hora_limpia, "%H:%M")

    # ------------------------------------------------------------------
    def _validar_entrada_evento(
        self,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int) -> Tuple[bool, str]:

        if not nombre.strip():
            return False, "El nombre del show es obligatorio."
        if not categoria.strip():
            return False, "La categoria del show es obligatoria."
        if duracion_minutos < 30:
            return False, "La duracion minima es de 30 minutos."

        try:
            self._parse_fecha(fecha)
        except ValueError:
            return False, "La fecha debe usar formato YYYY-MM-DD."

        try:
            self._parse_hora(hora_inicio)
        except ValueError:
            return False, "La hora debe usar formato HH:MM en 24 horas."

        return True, "OK"

    # ------------------------------------------------------------------
    def _hay_conflicto_horario(
        self,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        evento_excluir_id: Optional[int] = None) -> bool:

        nuevo_inicio = self._parse_hora(hora_inicio)
        nuevo_fin = nuevo_inicio + timedelta(minutes=duracion_minutos)

        for evento_existente in self.repositorio.obtener_por_fecha(fecha):
            if evento_excluir_id is not None and evento_existente.identificador == evento_excluir_id:
                continue

            inicio_actual = self._parse_hora(evento_existente.hora_inicio)
            fin_actual = inicio_actual + timedelta(minutes=evento_existente.duracion_minutos)

            ventana_nueva = (nuevo_inicio, nuevo_fin)
            ventana_actual = (inicio_actual, fin_actual)
            if ventana_nueva[0] < ventana_actual[1] and ventana_actual[0] < ventana_nueva[1]:
                return True

        return False

    # ------------------------------------------------------------------
    def _normalizar_precios(self, precios_por_zona: Optional[Dict[str, float]]) -> Dict[str, float]:
        base = {
            "General": self.PRECIO_MINIMO_GENERAL,
            "Preferencial": self.PRECIO_MINIMO_GENERAL * 1.4,
            "VIP": self.PRECIO_MINIMO_GENERAL * 2}

        if not precios_por_zona:
            return base

        normalizados: Dict[str, float] = {}
        for zona in self.ZONAS_ORDEN:
            precio = float(precios_por_zona.get(zona, base[zona]))
            if precio < self.PRECIO_MINIMO_GENERAL:
                precio = self.PRECIO_MINIMO_GENERAL
            normalizados[zona] = precio

        if normalizados["VIP"] < normalizados["Preferencial"]:
            normalizados["VIP"] = normalizados["Preferencial"]
        if normalizados["Preferencial"] < normalizados["General"]:
            normalizados["Preferencial"] = normalizados["General"]

        return normalizados

    # ------------------------------------------------------------------
    def programar_evento(
        self,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        descripcion: str,
        precios_por_zona: Optional[Dict[str, float]] = None) -> Tuple[bool, str, Optional[Evento]]:

        valido, mensaje = self._validar_entrada_evento(nombre, categoria, fecha, hora_inicio, duracion_minutos)
        if not valido:
            return False, mensaje, None

        if self._hay_conflicto_horario(fecha, hora_inicio, duracion_minutos):
            return False, "Existe choque de horarios con otro show en la misma fecha.", None

        nuevo_id = self.repositorio.obtener_ultimo_id() + 1
        evento = Evento(
            identificador=nuevo_id,
            nombre=nombre.strip(),
            categoria=categoria.strip(),
            fecha=fecha.strip(),
            hora_inicio=hora_inicio.strip(),
            duracion_minutos=duracion_minutos,
            descripcion=descripcion.strip(),
            precios_por_zona=self._normalizar_precios(precios_por_zona),
            capacidad_por_zona=self.DISTRIBUCION_ZONAS.copy())

        self.repositorio.agregar(evento)
        return True, "Show programado correctamente.", evento

    # ------------------------------------------------------------------
    def actualizar_precios(
        self,
        evento_id: int,
        precio_general: float,
        precio_preferencial: float,
        precio_vip: float) -> Tuple[bool, str]:

        evento = self.repositorio.obtener_por_id(evento_id)
        if evento is None:
            return False, "No existe el show seleccionado."

        precios_nuevos = {
            "General": precio_general,
            "Preferencial": precio_preferencial,
            "VIP": precio_vip}

        evento.precios_por_zona = self._normalizar_precios(precios_nuevos)
        self.repositorio.actualizar(evento)
        return True, "Precios actualizados correctamente."

    # ------------------------------------------------------------------
    def actualizar_evento(
        self,
        evento_id: int,
        nombre: str,
        categoria: str,
        fecha: str,
        hora_inicio: str,
        duracion_minutos: int,
        descripcion: str) -> Tuple[bool, str]:

        evento = self.repositorio.obtener_por_id(evento_id)
        if evento is None:
            return False, "No existe el show seleccionado."

        valido, mensaje = self._validar_entrada_evento(nombre, categoria, fecha, hora_inicio, duracion_minutos)

        if not valido:
            return False, mensaje

        if self._hay_conflicto_horario(
            fecha=fecha,
            hora_inicio=hora_inicio,
            duracion_minutos=duracion_minutos,
            evento_excluir_id=evento_id):
            return False, "Existe choque de horarios con otro show en la misma fecha."

        evento.nombre = nombre.strip()
        evento.categoria = categoria.strip()
        evento.fecha = fecha.strip()
        evento.hora_inicio = hora_inicio.strip()
        evento.duracion_minutos = duracion_minutos
        evento.descripcion = descripcion.strip()

        self.repositorio.actualizar(evento)
        return True, "Show actualizado correctamente."

    # ------------------------------------------------------------------
    def aumentar_capacidad(
        self,
        evento_id: int,
        agregar_general: int,
        agregar_preferencial: int,
        agregar_vip: int) -> Tuple[bool, str]:

        evento = self.repositorio.obtener_por_id(evento_id)
        if evento is None:
            return False, "No existe el show seleccionado."

        if agregar_general < 0 or agregar_preferencial < 0 or agregar_vip < 0:
            return False, "Los asientos a agregar no pueden ser negativos."
        if agregar_general == 0 and agregar_preferencial == 0 and agregar_vip == 0:
            return False, "Debes agregar asientos en al menos una zona."

        evento.capacidad_por_zona["General"] = evento.capacidad_por_zona.get("General", 0) + agregar_general
        evento.capacidad_por_zona["Preferencial"] = (
            evento.capacidad_por_zona.get("Preferencial", 0) + agregar_preferencial)

        evento.capacidad_por_zona["VIP"] = evento.capacidad_por_zona.get("VIP", 0) + agregar_vip

        self.repositorio.actualizar(evento)
        return True, "Capacidad actualizada correctamente."

    # ------------------------------------------------------------------
    def eliminar_evento(self, evento_id: int, tiene_tickets: bool) -> Tuple[bool, str]:
        if tiene_tickets:
            return False, "No se puede eliminar el show porque ya tiene ventas registradas."
        eliminado = self.repositorio.eliminar(evento_id)

        if not eliminado:
            return False, "No se encontro el show a eliminar."
        return True, "Show eliminado correctamente."

    # ------------------------------------------------------------------
    def _clave_evento_por_id(self, evento: Evento) -> int:
        return evento.identificador

    # ------------------------------------------------------------------
    def _clave_evento_por_hora(self, evento: Evento) -> str:
        return evento.hora_inicio

    # ------------------------------------------------------------------
    def listar_eventos(self) -> List[Evento]:
        eventos = self.repositorio.obtener_todos()
        eventos_ordenados = list(eventos)
        eventos_ordenados.sort(key=self._clave_evento_por_id)
        return eventos_ordenados

    # ------------------------------------------------------------------
    def listar_eventos_por_fecha(self, fecha: str) -> List[Evento]:
        eventos_por_fecha = self.repositorio.obtener_por_fecha(fecha)
        eventos_ordenados = list(eventos_por_fecha)
        eventos_ordenados.sort(key=self._clave_evento_por_hora)
        return eventos_ordenados

    # ------------------------------------------------------------------
    def obtener_evento(self, evento_id: int) -> Optional[Evento]:
        return self.repositorio.obtener_por_id(evento_id)

    # ------------------------------------------------------------------
    def obtener_eventos_por_categoria(self, categoria: str) -> List[Evento]:
        categoria_buscada = categoria.strip().lower()
        eventos_filtrados = []
        for evento in self.listar_eventos():
            if evento.categoria.lower() == categoria_buscada:
                eventos_filtrados.append(evento)
        return eventos_filtrados

    # ------------------------------------------------------------------
    def cargar_shows_demo(self) -> int:
        shows_demo = [
            {
                "nombre": "Aereo Estelar",
                "categoria": "Acrobacia",
                "fecha": "2026-06-02",
                "hora_inicio": "17:00",
                "duracion_minutos": 90,
                "descripcion": "Show de telas y trapecio con acrobacias aereas."},
            {
                "nombre": "Risas Sin Red",
                "categoria": "Comedia",
                "fecha": "2026-06-02",
                "hora_inicio": "20:00",
                "duracion_minutos": 70,
                "descripcion": "Rutinas de payasos y humor para toda la familia."
            },
            {
                "nombre": "Noche de Fuego",
                "categoria": "Fuego",
                "fecha": "2026-06-03",
                "hora_inicio": "19:30",
                "duracion_minutos": 80,
                "descripcion": "Malabares de fuego y efectos de luz sincronizados."
            },
            {
                "nombre": "Ilusion Total",
                "categoria": "Magia",
                "fecha": "2026-06-04",
                "hora_inicio": "18:30",
                "duracion_minutos": 75,
                "descripcion": "Grandes actos de magia e ilusionismo en escena."
            }]

        existentes = set()
        for evento in self.listar_eventos():
            llave_evento = (evento.nombre.lower(), evento.fecha, evento.hora_inicio)
            existentes.add(llave_evento)

        agregados = 0
        
        for show in shows_demo:
            llave = (show["nombre"].lower(), show["fecha"], show["hora_inicio"])
            if llave in existentes:
                continue
            resultado_programacion = self.programar_evento(
                nombre=show["nombre"],
                categoria=show["categoria"],
                fecha=show["fecha"],
                hora_inicio=show["hora_inicio"],
                duracion_minutos=show["duracion_minutos"],
                descripcion=show["descripcion"])
            exito = resultado_programacion[0]
            if exito:
                agregados += 1

        return agregados

