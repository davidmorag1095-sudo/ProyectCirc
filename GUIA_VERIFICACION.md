# Guia breve de verificacion manual

Esta guia permite validar rapidamente que el sistema cumple con los escenarios principales del proyecto.

## 1) Acceso al sistema

1. Ejecutar el main.
2. Iniciar sesion con los usuarios demo de `Administrador`, `Cajero` y `Cliente`.
3. Confirmar que cada rol muestra su modulo correspondiente.

## 2) Flujo de administrador

1. Seleccionar un show existente.
2. Abrir `ConfigShows`, cargar el show y actualizar datos (hora o descripcion).
3. Actualizar precios por zona en el panel principal.
4. Agregar asientos por zona y validar que no haya errores de negocio.

## 3) Flujo de cliente y boleteria

1. Comprar ticket en zona `General`.
2. Comprar ticket en zona `VIP`.
3. Verificar que el asiento asignado no se repita y que cambie la disponibilidad.

## 4) Persistencia y reportes

1. Generar reporte general y por fecha.
2. Cerrar y volver a abrir la aplicacion.
3. Confirmar que los cambios se mantienen en `mvc/data/*.json`.
