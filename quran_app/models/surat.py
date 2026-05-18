class Surat:
    def __init__(self, nomor, nama, nama_latin, nama_arab, arti, jumlah_ayat, tempat, juz):
        self._nomor = nomor
        self._nama = nama
        self._nama_latin = nama_latin
        self._nama_arab = nama_arab
        self._arti = arti
        self._jumlah_ayat = jumlah_ayat
        self._tempat = tempat
        self._juz = juz
    
    @property
    def nomor(self): 
        return self._nomor
    
    @property
    def nama(self): 
        return self._nama
    
    @property
    def nama_latin(self): 
        return self._nama_latin
    
    @property
    def nama_arab(self): 
        return self._nama_arab
    
    @property
    def arti(self): 
        return self._arti
    
    @property
    def jumlah_ayat(self): 
        return self._jumlah_ayat
    
    @property
    def tempat(self): 
        return self._tempat
    
    @property
    def juz(self): 
        return self._juz
    
    def to_dict(self):
        return {
            "nomor": self._nomor,
            "nama": self._nama,
            "nama_latin": self._nama_latin,
            "nama_arab": self._nama_arab,
            "arti": self._arti,
            "jumlah_ayat": self._jumlah_ayat,
            "tempat": self._tempat,
            "juz": self._juz
        }


class SuratDetail(Surat):
    def __init__(self, nomor, nama, nama_latin, nama_arab, arti, jumlah_ayat, tempat, juz, ayat_list=None):
        # Panggil constructor parent class
        super().__init__(nomor, nama, nama_latin, nama_arab, arti, jumlah_ayat, tempat, juz)
        self._ayat_list = ayat_list if ayat_list else []
    
    @property
    def ayat_list(self):
        return self._ayat_list
    
    def to_dict(self):
        data = super().to_dict()
        data["ayat"] = [a.to_dict() for a in self._ayat_list]
        return data