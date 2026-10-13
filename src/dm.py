import os


class DataManager:
    def __init__(self, filename="otchet.txt"):
        self.filename = filename

    def _get_path(self):
        papka = os.getenv("FLET_APP_STORAGE_DATA")
        if papka:
            return os.path.join(papka, self.filename)
        return self.filename

    def sohranit_otchet(self, sessions):
        put = self._get_path()
        with open(put, "w", encoding="utf-8") as f:
            f.write("+  |  login  |  time_in  |  time_out  |\n")
            f.write("|---|---|---|---|\n")
            for s in sessions:
                t_out = s.time_out if s.time_out is not None else "---"
                f.write("| " + s.name + " | " + s.time_in + " | " + t_out + " |\n")
            f.write("+\n")