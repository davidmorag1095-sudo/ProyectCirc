from typing import Optional


class Usuario:
    def __init__(
        self,
        identificador: int,
        nombre_completo: str,
        correo_electronico: str,
        contrasena: str,
        rol: str,
        direccion: Optional[str] = None) -> None:

        self.identificador = identificador
        self.nombre_completo = nombre_completo
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
        self.rol = rol
        self.direccion = direccion

    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "identificador": self.identificador,
            "nombre_completo": self.nombre_completo,
            "correo_electronico": self.correo_electronico,
            "contrasena": self.contrasena,
            "rol": self.rol,
            "direccion": self.direccion}

    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(
            identificador=int(data.get("identificador", 0)),
            nombre_completo=data.get("nombre_completo", "").strip(),
            correo_electronico=data.get("correo_electronico", "").strip(),
            contrasena=data.get("contrasena", ""),
            rol=data.get("rol", "Cliente"),
            direccion=data.get("direccion"))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Usuario(identificador={self.identificador!r}, "
            f"nombre_completo={self.nombre_completo!r}, "
            f"correo_electronico={self.correo_electronico!r}, "
            f"rol={self.rol!r})")
