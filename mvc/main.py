"""Punto de entrada del sistema de boleteria del circo."""

import tkinter as tk

from view.admin_menu import AdminMenu
from view.boleteria_menu import BoleteriaMenu
from view.cliente_menu import ClienteMenu
from view.login_view import LoginView

class CircoApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("1180x680")
        self.root.minsize(1080, 640)

    def _limpiar_ventana(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def _cargar_login(self) -> None:
        self._limpiar_ventana()
        LoginView(self.root, on_login=self._cargar_menu_por_rol)

    def _cargar_menu_por_rol(self, rol: str, usuario_id: int) -> None:
        self._limpiar_ventana()
        if rol == "Administrador":
            AdminMenu(self.root, logout_callback=self._cargar_login)
        elif rol == "Cajero":
            BoleteriaMenu(self.root, logout_callback=self._cargar_login)
        else:
            ClienteMenu(self.root, usuario_id=usuario_id, logout_callback=self._cargar_login)

    def run(self) -> None:
        self._cargar_login()
        self.root.mainloop()


if __name__ == "__main__":
    CircoApp().run()

