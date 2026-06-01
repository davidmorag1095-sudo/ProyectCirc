from typing import Optional

from model.usuario import Usuario
from service.usuario_service import UsuarioService


class AuthController:
    """Controlador para login, registro y cambio de clave."""

    def __init__(self, servicio_usuarios: Optional[UsuarioService] = None) -> None:
        self.servicio_usuarios = servicio_usuarios or UsuarioService()

    def iniciar_sesion(self, correo: str, contrasena: str) -> Optional[Usuario]:
        return self.servicio_usuarios.autenticar(correo, contrasena)

# ------------------------------------------------------------------

    def registrar(
        self,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str = "Cliente"    ) -> Optional[Usuario]:
        return self.servicio_usuarios.registrar_usuario(
            nombre_completo=nombre,
            correo_electronico=correo,
            contrasena=contrasena,
            rol=rol
        )

# ------------------------------------------------------------------

    def cambiar_contrasena(self, correo: str, nueva_contrasena: str) -> bool:
        return self.servicio_usuarios.actualizar_contrasena(correo, nueva_contrasena)

