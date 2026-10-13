from abc import ABC, abstractmethod
from datetime import datetime


class Predmet(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    def get_price(self):
        pass

    def __eq__(self, other):
        return self._price == other._price

    def __repr__(self):
        return "Predmet: " + self._name

    def __str__(self):
        return self._name


class Stavka(Predmet):
    def get_price(self):
        return self._price

    def __lt__(self, other):
        return self._price < other._price

    def __gt__(self, other):
        return self._price > other._price


class Session(ABC):
    def __init__(self, name):
        self._name = name
        self._time_in = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._time_out = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def get_info(self):
        pass

    def close(self):
        self._time_out = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def __eq__(self, other):
        return self._name == other._name

    def __repr__(self):
        return "Session: " + self._name

    def __str__(self):
        return self._name


class User(Session):
    def get_info(self):
        return self._name

    def __lt__(self, other):
        return self._name < other._name

    def __gt__(self, other):
        return self._name > other._name


class Mapper:
    def __init__(self):
        self.keys = []
        self.values = []

    def set(self, key, value):
        if key in self.keys:
            i = self.keys.index(key)
            self.values[i] = value
        else:
            self.keys.append(key)
            self.values.append(value)

    def get(self, key):
        if key in self.keys:
            i = self.keys.index(key)
            return self.values[i]
        return None

    def __eq__(self, other):
        return self.keys == other.keys

    def __repr__(self):
        return "Mapper"

    def __str__(self):
        return "Mapper"


class Upgrade:
    vsego = 0
    pobed = 0

    @staticmethod
    def shans(stavka, cel):
        if cel <= 0:
            return 0
        s = stavka / cel
        if s > 1:
            s = 1
        return s

    @staticmethod
    def poprobovat(stavka, cel):
        shans = Upgrade.shans(stavka, cel)
        nado = Upgrade.vsego * shans
        if Upgrade.pobed < nado:
            uspeh = True
        else:
            uspeh = False
        Upgrade.vsego = Upgrade.vsego + 1
        if uspeh:
            Upgrade.pobed = Upgrade.pobed + 1
        return uspeh