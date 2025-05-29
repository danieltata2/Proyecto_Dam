import flet as ft
from bbdd import insertar_usuario

def registro_view(page: ft.Page, volver_a_login):

    nombre = ft.TextField(label="Nombre", width=300)
    apellidos = ft.TextField(label="Apellidos", width=300)
    correo = ft.TextField(label="Correo", width=300)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    fecha_nacimiento = ft.DatePicker()
    fecha_nacimiento_btn = ft.ElevatedButton("Seleccionar Fecha de Nacimiento",
                                             on_click=lambda _: fecha_nacimiento.pick_date())
    mensaje = ft.Text("", color="red")

    def registrar_usuario(e):
        if not all([nombre.value, apellidos.value, correo.value, contrasena.value, fecha_nacimiento.value]):
            mensaje.value = "Todos los campos son obligatorios."
            page.update()
            return

        try:
            insertar_usuario(
                nombre.value,
                apellidos.value,
                correo.value,
                contrasena.value,
                fecha_nacimiento.value
            )
            mensaje.value = "Usuario registrado correctamente."
            page.update()
            # Continuar con redirección o limpieza
        except Exception as ex:
            mensaje.value = f"Error al registrar: {ex}"
            page.update()

    fecha_nacimiento = ft.DatePicker()
    fecha_nacimiento_btn = ft.ElevatedButton(
        "Seleccionar Fecha de Nacimiento",
        on_click=lambda _: abrir_datepicker()
    )

    def abrir_datepicker():
        fecha_nacimiento.open = True
        page.update()

    page.overlay.append(fecha_nacimiento)

    page.overlay.append(fecha_nacimiento)

    return ft.Column([
        nombre,
        apellidos,
        correo,
        contrasena,
        fecha_nacimiento_btn,
        mensaje,
        ft.ElevatedButton("Registrarse", on_click=registrar_usuario),
        ft.TextButton("Ya tengo cuenta. Ir a Login", on_click=lambda _: (page.clean(), volver_a_login())),
    ])
