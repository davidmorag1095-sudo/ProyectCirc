import json
from pathlib import Path
from typing import Dict, Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Repositorio base con memoria en lista/diccionario y persistencia JSON."""

    def __init__(self, archivo_json: Path, modelo_cls: Type[T]) -> None:
        self.archivo_json = archivo_json
        self.modelo_cls = modelo_cls
        self.lista_elementos: List[T] = []
        self.diccionario_elementos: Dict[int, T] = {}

        self.archivo_json.parent.mkdir(parents=True, exist_ok=True)
        if not self.archivo_json.exists():
            self.archivo_json.write_text("[]", encoding="utf-8")

        self._cargar()

    # ------------------------------------------------------------------
    def _extraer_clave(self, objeto: T) -> Optional[int]:
        clave = getattr(objeto, "identificador", None)
        if clave is None:
            return None
        return int(clave)

    # ------------------------------------------------------------------
    def _agregar_en_memoria(self, objeto: T) -> None:
        clave = self._extraer_clave(objeto)
        if clave is None:
            return
        self.lista_elementos.append(objeto)
        self.diccionario_elementos[clave] = objeto

    # ------------------------------------------------------------------
    def _cargar(self) -> None:
        self.lista_elementos = []
        self.diccionario_elementos = {}

        try:
            contenido = self.archivo_json.read_text(encoding="utf-8-sig").strip()
            if not contenido:
                return
            data = json.loads(contenido)
            if not isinstance(data, list):
                return
        except (json.JSONDecodeError, OSError):
            return

        for item in data:
            if not isinstance(item, dict):
                continue
            objeto = self.modelo_cls.from_dict(item)
            self._agregar_en_memoria(objeto)

    # ------------------------------------------------------------------
    def _guardar(self) -> None:
        data = []
        for objeto in self.lista_elementos:
            data.append(objeto.to_dict())
        self.archivo_json.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8")

    # ------------------------------------------------------------------
    def _leer(self) -> List[T]:
        return list(self.lista_elementos)

    # ------------------------------------------------------------------
    def _escribir(self, objetos: List[T]) -> None:
        self.lista_elementos = []
        self.diccionario_elementos = {}
        for objeto in objetos:
            self._agregar_en_memoria(objeto)
        self._guardar()

    # ------------------------------------------------------------------
    def add(self, clave: int, objeto: T) -> None:
        if clave in self.diccionario_elementos:
            raise ValueError("Elemento ya existe")
        self.lista_elementos.append(objeto)
        self.diccionario_elementos[clave] = objeto
        self._guardar()

    # ------------------------------------------------------------------
    def get(self, clave: int) -> Optional[T]:
        return self.diccionario_elementos.get(clave)

    # ------------------------------------------------------------------
    def get_all(self) -> List[T]:
        return list(self.lista_elementos)

    # ------------------------------------------------------------------
    def update(self, clave: int, objeto: T) -> bool:
        if clave not in self.diccionario_elementos:
            return False

        for index, actual in enumerate(self.lista_elementos):
            actual_clave = self._extraer_clave(actual)
            if actual_clave == clave:
                self.lista_elementos[index] = objeto
                break

        self.diccionario_elementos[clave] = objeto
        self._guardar()
        return True

    # ------------------------------------------------------------------
    def delete(self, clave: int) -> bool:
        objeto = self.diccionario_elementos.pop(clave, None)
        if objeto is None:
            return False

        elementos_filtrados = []
        for item in self.lista_elementos:
            if self._extraer_clave(item) != clave:
                elementos_filtrados.append(item)
        self.lista_elementos = elementos_filtrados
        self._guardar()
        return True

    # ------------------------------------------------------------------
    def obtener_todos(self) -> List[T]:
        return self.get_all()

    # ------------------------------------------------------------------
    def obtener_por_id(self, identificador: int) -> Optional[T]:
        return self.get(identificador)

    # ------------------------------------------------------------------
    def agregar(self, objeto: T) -> T:
        clave = self._extraer_clave(objeto)
        if clave is None:
            raise ValueError("El objeto no tiene identificador")
        self.add(clave, objeto)
        return objeto

    # ------------------------------------------------------------------
    def actualizar(self, objeto: T) -> bool:
        clave = self._extraer_clave(objeto)
        if clave is None:
            return False
        return self.update(clave, objeto)

    # ------------------------------------------------------------------
    def eliminar(self, identificador: int) -> bool:
        return self.delete(identificador)
