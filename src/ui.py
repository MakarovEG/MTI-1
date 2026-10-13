import flet as ft
import time

from models import Stavka, User, Mapper, Upgrade
from dm import DataManager


class MyText(ft.Text):
    pass


class MyButton(ft.Button):
    pass


class MyTextField(ft.TextField):
    pass


class MyColumn(ft.Column):
    pass


class MyRow(ft.Row):
    pass


class MyContainer(ft.Container):
    pass


class MyProgressBar(ft.ProgressBar):
    pass


class MyDivider(ft.Divider):
    pass


class MyIcon(ft.Icon):
    pass


class MyCard(ft.Card):
    pass


cveta = Mapper()
cveta.set("win", ft.Colors.GREEN)
cveta.set("lose", ft.Colors.RED)

stavki = [
    Stavka("10", 10), Stavka("50", 50), Stavka("100", 100),
    Stavka("200", 200), Stavka("500", 500), Stavka("1000", 1000),
    Stavka("1500", 1500), Stavka("2000", 2000), Stavka("3000", 3000),
    Stavka("5000", 5000),
]


class Main:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dm = DataManager()
        self.session = User("student")

        page.title = "Makarov Drop"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.bgcolor = ft.Colors.WHITE

        self.label_shans = MyText(value="Шанс: ---", size=16, text_align=ft.TextAlign.CENTER)
        self.label_result = MyText(value="", size=20, color=ft.Colors.GREEN, text_align=ft.TextAlign.CENTER)
        self.progress = MyProgressBar(width=300, value=0)
        self.pole_stavka = MyTextField(label="Твоя сумма (руб.)", width=300)
        self.pole_cel = MyTextField(label="Хочешь получить (руб.)", width=300)
        self.knopka = MyButton(content="ДРОПНУТЬ", on_click=self.apgreid, width=300)

        self.pole_stavka.on_change = self.pereschet
        self.pole_cel.on_change = self.pereschet

        ryad1, ryad2 = [], []
        for i, s in enumerate(stavki):
            kn = MyButton(
                content=s.name,
                on_click=self._make_knopka_stavki(s),
                width=80,
                height=32,
            )
            (ryad1 if i < 5 else ryad2).append(kn)

        page.add(
            MyContainer(
                content=MyColumn(
                    controls=[
                        MyText("MAKAROV DROP", size=30, text_align=ft.TextAlign.CENTER),
                        MyRow(controls=ryad1, alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                        MyRow(controls=ryad2, alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                        self.pole_stavka,
                        self.pole_cel,
                        self.label_shans,
                        self.progress,
                        self.knopka,
                        self.label_result,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
                alignment=ft.Alignment.CENTER,
            )
        )

        self.pereschet(None)
        page.on_close = self.on_close

    def _make_knopka_stavki(self, s):
        def vnutri(e):
            self.pole_stavka.value = str(s.price)
            self.pereschet(None)
        return vnutri

    def pereschet(self, e):
        try:
            st = float(self.pole_stavka.value) if self.pole_stavka.value else 0
        except ValueError:
            st = 0
        try:
            cel = float(self.pole_cel.value) if self.pole_cel.value else 0
        except ValueError:
            cel = 0

        if st <= 0 or cel <= 0:
            self.label_shans.value = "Шанс: ---"
            self.progress.value = 0
        elif cel <= st:
            self.label_shans.value = "Шанс: цель меньше ставки"
            self.progress.value = 0
        else:
            shans = Upgrade.shans(st, cel)
            self.label_shans.value = "Шанс: " + str(round(shans * 100, 1)) + "%"
            self.progress.value = shans
        self.page.update()

    def apgreid(self, e):
        try:
            st = float(self.pole_stavka.value)
        except (ValueError, TypeError):
            self.label_result.value = "Введи число"
            self.label_result.color = ft.Colors.RED
            self.page.update()
            return

        try:
            cel = float(self.pole_cel.value)
        except (ValueError, TypeError):
            self.label_result.value = "Введи число"
            self.label_result.color = ft.Colors.RED
            self.page.update()
            return

        if st <= 0:
            self.label_result.value = "Ставка должна быть больше 0"
            self.label_result.color = ft.Colors.RED
            self.page.update()
            return

        if cel <= st:
            self.label_result.value = "Цель должна быть больше ставки"
            self.label_result.color = ft.Colors.RED
            self.page.update()
            return

        shans = Upgrade.shans(st, cel)
        self.label_shans.value = "Шанс: " + str(round(shans * 100, 1)) + "%"
        self.progress.value = shans
        self.label_result.value = ""
        self.page.update()

        uspeh = Upgrade.poprobovat(st, cel)
        if uspeh:
            self.label_result.value = "ПОБЕДА"
            self.label_result.color = cveta.get("win")
            for _ in range(3):
                self.page.bgcolor = ft.Colors.GREEN_100
                self.page.update()
                time.sleep(0.15)
                self.page.bgcolor = ft.Colors.WHITE
                self.page.update()
                time.sleep(0.15)
            self.page.bgcolor = ft.Colors.GREEN_100
        else:
            self.label_result.value = "ПРОВАЛ"
            self.label_result.color = cveta.get("lose")
            for _ in range(3):
                self.page.bgcolor = ft.Colors.RED_100
                self.page.update()
                time.sleep(0.15)
                self.page.bgcolor = ft.Colors.WHITE
                self.page.update()
                time.sleep(0.15)
            self.page.bgcolor = ft.Colors.RED_100

        self.page.update()

        for _ in range(3):
            self.label_result.size = 30
            self.page.update()
            time.sleep(0.15)
            self.label_result.size = 20
            self.page.update()
            time.sleep(0.15)

        time.sleep(1)
        self.page.bgcolor = ft.Colors.WHITE
        self.page.update()

        self.pole_stavka.value = ""
        self.pole_cel.value = ""
        self.label_shans.value = "Шанс: ---"
        self.progress.value = 0
        self.page.update()

    def on_close(self, e):
        self.session.close()
        self.dm.sohranit_otchet([self.session])