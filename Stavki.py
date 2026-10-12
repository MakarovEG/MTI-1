import flet as ft
import random
import time
import os
from datetime import datetime
from abc import ABC, abstractmethod
class Predmet(ABC):
    def __init__(self,name,price):
        self._name=name
        self._price=price
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name=value
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self,value):
        self._price=value
    def get_price(self):
        pass
    def __eq__(self,other):
        return self._price==other._price
    def __repr__(self):
        return "Predmet: "+self._name
    def __str__(self):
        return self._name
class Stavka(Predmet):
    def get_price(self):
        return self._price
    def __lt__(self,other):
        return self._price<other._price
    def __gt__(self,other):
        return self._price>other._price
class Session(ABC):
    def __init__(self,name):
        self._name=name
        self._time_in=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._time_out=None
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name=value
    @property
    def time_in(self):
        return self._time_in
    @time_in.setter
    def time_in(self,value):
        self._time_in=value
    @property
    def time_out(self):
        return self._time_out
    @time_out.setter
    def time_out(self,value):
        self._time_out=value
    def get_info(self):
        pass
    def close(self):
        self._time_out=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    def __eq__(self,other):
        return self._name==other._name
    def __repr__(self):
        return "Session: "+self._name
    def __str__(self):
        return self._name
class User(Session):
    def get_info(self):
        return self._name
    def __lt__(self,other):
        return self._name<other._name
    def __gt__(self,other):
        return self._name>other._name
class Mapper:
    def __init__(self):
        self.keys=[]
        self.values=[]
    def set(self,key,value):
        if key in self.keys:
            i=self.keys.index(key)
            self.values[i]=value
        else:
            self.keys.append(key)
            self.values.append(value)
    def get(self,key):
        if key in self.keys:
            i=self.keys.index(key)
            return self.values[i]
        else:
            return None
    def __eq__(self,other):
        return self.keys==other.keys
    def __repr__(self):
        return "Mapper"
    def __str__(self):
        return "Mapper"
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
class Upgrade:
    vsego=0
    pobed=0
    @staticmethod
    def shans(stavka,cel):
        if cel<=0:
            return 0
        s=stavka/cel
        if s>1:
            s=1
        return s
    @staticmethod
    def poprobovat(stavka,cel):
        shans=Upgrade.shans(stavka,cel)
        nado=Upgrade.vsego*shans
        if Upgrade.pobed<nado:
            uspeh=True
        else:
            uspeh=False
        Upgrade.vsego=Upgrade.vsego+1
        if uspeh==True:
            Upgrade.pobed=Upgrade.pobed+1
        return uspeh
cveta=Mapper()
cveta.set("win",ft.Colors.GREEN)
cveta.set("lose",ft.Colors.RED)
stavki=[Stavka("10",10),Stavka("50",50),Stavka("100",100),Stavka("200",200),Stavka("500",500),Stavka("1000",1000),Stavka("1500",1500),Stavka("2000",2000),Stavka("3000",3000),Stavka("5000",5000)]
def sohranit_otchet(sessions):
    put="otchet.txt"
    papka=os.getenv("FLET_APP_STORAGE_DATA")
    if papka:
        put=os.path.join(papka,"otchet.txt")
    f=open(put,"w",encoding="utf-8")
    f.write("+  |  login  |  time_in  |  time_out  |\n")
    f.write("|---|---|---|---|\n")
    for s in sessions:
        if s.time_out==None:
            t_out="---"
        else:
            t_out=s.time_out
        f.write("| "+s.name+" | "+s.time_in+" | "+t_out+" |\n")
    f.write("+\n")
    f.close()
def main(page:ft.Page):
    page.title="Makarov Drop"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.bgcolor=ft.Colors.WHITE
    session=User("student")
    label_shans=MyText(value="Шанс: ---",size=16,text_align=ft.TextAlign.CENTER)
    label_result=MyText(value="",size=20,color=ft.Colors.GREEN,text_align=ft.TextAlign.CENTER)
    progress=MyProgressBar(width=300,value=0)
    pole_stavka=MyTextField(label="Твоя сумма (руб.)",width=300)
    pole_cel=MyTextField(label="Хочешь получить (руб.)",width=300)
    def knopka_stavki(s):
        def vnutri(e):
            pole_stavka.value=str(s.price)
            pereschet(None)
        return vnutri
    ryad1=[]
    ryad2=[]
    for i in range(len(stavki)):
        s=stavki[i]
        kn=MyButton(content=s.name,on_click=knopka_stavki(s),width=80,height=32)
        if i<5:
            ryad1.append(kn)
        else:
            ryad2.append(kn)
    def pereschet(e):
        if pole_stavka.value=="":
            st=0
        else:
            try:
                st=float(pole_stavka.value)
            except:
                st=0
        if pole_cel.value=="":
            cel=0
        else:
            try:
                cel=float(pole_cel.value)
            except:
                cel=0
        if st<=0 or cel<=0:
            label_shans.value="Шанс: ---"
            progress.value=0
        elif cel<=st:
            label_shans.value="Шанс: цель меньше ставки"
            progress.value=0
        else:
            shans=Upgrade.shans(st,cel)
            label_shans.value="Шанс: "+str(round(shans*100,1))+"%"
            progress.value=shans
        page.update()
    pole_stavka.on_change=pereschet
    pole_cel.on_change=pereschet
    def apgreid(e):
        try:
            st=float(pole_stavka.value)
        except:
            label_result.value="Введи число"
            label_result.color=ft.Colors.RED
            page.update()
            return
        try:
            cel=float(pole_cel.value)
        except:
            label_result.value="Введи число"
            label_result.color=ft.Colors.RED
            page.update()
            return
        if st<=0:
            label_result.value="Ставка должна быть больше 0"
            label_result.color=ft.Colors.RED
            page.update()
            return
        if cel<=st:
            label_result.value="Цель должна быть больше ставки"
            label_result.color=ft.Colors.RED
            page.update()
            return
        shans=Upgrade.shans(st,cel)
        label_shans.value="Шанс: "+str(round(shans*100,1))+"%"
        progress.value=shans
        label_result.value=""
        page.update()
        uspeh=Upgrade.poprobovat(st,cel)
        if uspeh==True:
            label_result.value="ПОБЕДА"
            label_result.color=cveta.get("win")
            for i in range(3):
                page.bgcolor=ft.Colors.GREEN_100
                page.update()
                time.sleep(0.15)
                page.bgcolor=ft.Colors.WHITE
                page.update()
                time.sleep(0.15)
            page.bgcolor=ft.Colors.GREEN_100
        else:
            label_result.value="ПРОВАЛ"
            label_result.color=cveta.get("lose")
            for i in range(3):
                page.bgcolor=ft.Colors.RED_100
                page.update()
                time.sleep(0.15)
                page.bgcolor=ft.Colors.WHITE
                page.update()
                time.sleep(0.15)
            page.bgcolor=ft.Colors.RED_100
        page.update()
        for i in range(3):
            label_result.size=30
            page.update()
            time.sleep(0.15)
            label_result.size=20
            page.update()
            time.sleep(0.15)
        time.sleep(1)
        page.bgcolor=ft.Colors.WHITE
        page.update()
        pole_stavka.value=""
        pole_cel.value=""
        label_shans.value="Шанс: ---"
        progress.value=0
        page.update()
    knopka=MyButton(content="ДРОПНУТЬ",on_click=apgreid,width=300)
    pereschet(None)
    page.add(
        MyContainer(
            content=MyColumn(
                controls=[
                    MyText("MAKAROV DROP",size=30,text_align=ft.TextAlign.CENTER),
                    MyRow(controls=ryad1,alignment=ft.MainAxisAlignment.CENTER,spacing=4),
                    MyRow(controls=ryad2,alignment=ft.MainAxisAlignment.CENTER,spacing=4),
                    pole_stavka,
                    pole_cel,
                    label_shans,
                    progress,
                    knopka,
                    label_result
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=30,
            alignment=ft.Alignment.CENTER
        )
    )
    def on_close(e):
        session.close()
        sohranit_otchet([session])
    page.on_close=on_close
ft.run(main)