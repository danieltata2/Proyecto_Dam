import flet as ft
from bbdd import verificar_usuario
from datetime import datetime
from Registro import registro_view
from Resultado import resultado_view  # Importar la vista resultado

def main(page: ft.Page):
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def mostrar_login():
        correo = ft.TextField(label="Correo", width=300)
        contrasena = ft.TextField(label="Contrasena", password=True, can_reveal_password=True, width=300)
        mensaje = ft.Text("", color="red")

        def iniciar_sesion(e):
            if not correo.value or not contrasena.value:
                mensaje.value = "Debe completar ambos campos."
                page.update()
                return

            if verificar_usuario(correo.value, contrasena.value):
                page.clean()
                page.add(resultado_view())  # Mostrar pantalla éxito
            else:
                mensaje.value = "Correo o contraseña incorrectos."
                page.update()

            conn = verificar_usuario()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE correo=%s AND contrasena=%s AND estado=TRUE",
                        (correo.value, contrasena.value))
            usuario = cur.fetchone()

            if usuario:
                cur.execute("UPDATE users SET Ultimo_Login = %s WHERE id = %s", (datetime.now(), usuario[0]))
                conn.commit()
                conn.close()
                page.clean()
                page.add(resultado_view())  # Mostrar vista resultado
            else:
                mensaje.value = "Correo o contraseña incorrectos."
                conn.close()
                page.update()

        page.clean()
        page.add(ft.Column([
            correo,
            contrasena,
            mensaje,
            ft.ElevatedButton("Iniciar sesión", on_click=iniciar_sesion),
            ft.TextButton("¿No tienes cuenta? Regístrate",
                          on_click=lambda _: mostrar_registro()),
        ]))

    def mostrar_registro():
        page.clean()
        page.add(registro_view(page, volver_a_login=mostrar_login))

    # Mostrar la vista de login al iniciar
    mostrar_login()

ft.app(target=main, view=ft.WEB_BROWSER, port=30039)
