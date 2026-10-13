import atexit
import flet as ft

from ui import Main


def main(page: ft.Page):
    app = Main(page)

    def on_exit():
        app.session.close()
        app.dm.sohranit_otchet([app.session])

    atexit.register(on_exit)


if __name__ == "__main__":
    ft.run(main)