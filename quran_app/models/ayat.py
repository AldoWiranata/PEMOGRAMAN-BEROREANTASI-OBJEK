class Ayat:
    def __init__(self, nomor, teks_arab, teks_latin, terjemahan, surat_nomor, surat_nama):
        self._nomor = nomor
        self._teks_arab = teks_arab
        self._teks_latin = teks_latin
        self._terjemahan = terjemahan
        self._surat_nomor = surat_nomor
        self._surat_nama = surat_nama
    
    @property
    def nomor(self):
        return self._nomor
    
    @property
    def teks_arab(self):
        return self._teks_arab
    
    @property
    def teks_latin(self):
        return self._teks_latin
    
    @property
    def terjemahan(self):
        return self._terjemahan
    
    @property
    def surat_nomor(self):
        return self._surat_nomor
    
    @property
    def surat_nama(self):
        return self._surat_nama
    
    def to_dict(self):
        return {
            "nomor": self._nomor,
            "teks_arab": self._teks_arab,
            "teks_latin": self._teks_latin,
            "terjemahan": self._terjemahan,
            "surat_nomor": self._surat_nomor,
            "surat_nama": self._surat_nama
        }