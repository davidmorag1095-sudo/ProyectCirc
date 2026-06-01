from typing import Optional

from model.usuario import Usuario
from repo.usuario_repository import UsuarioRepository


class UsuarioService:
    """Logica de usuarios y autenticacion."""

    ROLES_VALIDOS = ("Administrador", "Cajero", "Cliente")

    # ------------------------------------------------------------------
    def __init__(self, repositorio: Optional[UsuarioRepository] = None) -> None:
        self.repositorio = repositorio or UsuarioRepository()
        self._asegurar_usuarios_base()

    # ------------------------------------------------------------------
    def _asegurar_usuarios_base(self) -> None:
        usuarios_base = [
            ("Admin Principal", "admin@circo.com", "admin123", "Administrador"),
            ("Cajero Principal", "cajero@circo.com", "cajero123", "Cajero"),
            ("Cliente Demo", "cliente@circo.com", "cliente123", "Cliente")]

        for nombre, correo, clave, rol in usuarios_base:
            if self.repositorio.obtener_por_correo(correo) is None:
                self.registrar_usuario(nombre, correo, clave, rol)

    # ------------------------------------------------------------------
    def _correo_valido(self, correo: str) -> bool:
        correo_limpio = correo.strip()
        return "@" in correo_limpio and "." in correo_limpio.split("@")[-1]

    # ------------------------------------------------------------------
    def registrar_usuario(
        self,
        nombre_completo: str,
        correo_electronico: str,
        contrasena: str,
        rol: str = "Cliente",
        direccion: Optional[str] = None) -> Optional[Usuario]:

        nombre = nombre_completo.strip()
        correo = correo_electronico.strip().lower()
        clave = contrasena.strip()
        rol_limpio = rol.strip() or "Cliente"

        if not nombre or not correo or not clave:
            return None
        if rol_limpio not in self.ROLES_VALIDOS:
            return None
        if len(clave) < 4:
            return None
        if not self._correo_valido(correo):
            return None
        if self.repositorio.obtener_por_correo(correo) is not None:
            return None

        nuevo_id = self.repositorio.obtener_ultimo_id() + 1
        usuario = Usuario(
            identificador=nuevo_id,
            nombre_completo=nombre,
            correo_electronico=correo,
            contrasena=clave,
            rol=rol_limpio,
            direccion=direccion)
        self.repositorio.agregar(usuario)
        return usuario

    # ------------------------------------------------------------------
    def autenticar(self, correo_electronico: str, contrasena: str) -> Optional[Usuario]:
        correo = correo_electronico.strip().lower()
        clave = contrasena.strip()
        usuario = self.repositorio.obtener_por_correo(correo)

        if usuario and usuario.contrasena == clave:
            return usuario
        return None

    # ------------------------------------------------------------------
    def actualizar_contrasena(self, correo_electronico: str, nueva_contrasena: str) -> bool:
        correo = correo_electronico.strip().lower()
        clave_nueva = nueva_contrasena.strip()
        if len(clave_nueva) < 4:
            return False

        usuario = self.repositorio.obtener_por_correo(correo)
        if usuario is None:
            return False

        usuario.contrasena = clave_nueva
        return self.repositorio.actualizar(usuario)

    # ------------------------------------------------------------------
    def listar_usuarios(self) -> list[Usuario]:
        return self.repositorio.obtener_todos()

    # ------------------------------------------------------------------
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.repositorio.obtener_por_id(usuario_id)

