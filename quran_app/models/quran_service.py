import requests
from .surat import SuratDetail
from .ayat import Ayat

class QuranService:
    def __init__(self):
        self._data = {}
        self._load()
    
    def _load(self):
        print("🔄 Mengambil data dari API...")
        try:
            r = requests.get("https://api.alquran.cloud/v1/surah", timeout=30)
            if r.status_code != 200: raise Exception("API error")
            
            for s in r.json()['data']:
                n = s['number']
                nama = self._nama(n, s['englishName'])
                arti = self._arti(n, s['englishNameTranslation'])
                tempat = "Makkiyah" if s['revelationType'] == 'Meccan' else "Madaniyah"
                
                # Ambil detail ayat
                d = requests.get(f"https://api.alquran.cloud/v1/surah/{n}/editions/quran-uthmani,id.indonesian", timeout=30).json()
                
                # Pisahkan Arab dan Indonesia
                arab = next((e['ayahs'] for e in d['data'] if e['edition']['identifier'] == 'quran-uthmani'), [])
                indo = next((e['ayahs'] for e in d['data'] if e['edition']['identifier'] == 'id.indonesian'), [])
                
                surat = SuratDetail(n, nama, s['englishName'], s['name'], arti, s['numberOfAyahs'], tempat, self._juz(n), [])
                
                for i in range(len(arab)):
                    surat.ayat_list.append(Ayat(arab[i]['numberInSurah'], arab[i]['text'], "", indo[i]['text'], n, nama))
                
                self._data[n] = surat
                print(f"✅ {nama}: {len(surat.ayat_list)} ayat")
            
            total = sum(len(s.ayat_list) for s in self._data.values())
            print(f"\n📊 TOTAL: {len(self._data)} surat, {total} ayat")
            
        except Exception as e:
            print(f"⚠️ Error: {e}, pakai data lokal")
            self._local()
    
    def _nama(self, n, default):
        nama = {1:"Al-Fatihah",2:"Al-Baqarah",3:"Ali 'Imran",4:"An-Nisa'",5:"Al-Ma'idah",6:"Al-An'am",7:"Al-A'raf",8:"Al-Anfal",9:"At-Taubah",10:"Yunus",11:"Hud",12:"Yusuf",13:"Ar-Ra'd",14:"Ibrahim",15:"Al-Hijr",16:"An-Nahl",17:"Al-Isra'",18:"Al-Kahf",19:"Maryam",20:"Thaha",21:"Al-Anbiya'",22:"Al-Hajj",23:"Al-Mu'minun",24:"An-Nur",25:"Al-Furqan",26:"Asy-Syu'ara'",27:"An-Naml",28:"Al-Qasas",29:"Al-'Ankabut",30:"Ar-Rum",31:"Luqman",32:"As-Sajdah",33:"Al-Ahzab",34:"Saba'",35:"Fatir",36:"Yasin",37:"As-Saffat",38:"Sad",39:"Az-Zumar",40:"Ghafir",41:"Fussilat",42:"Asy-Syura",43:"Az-Zukhruf",44:"Ad-Dukhan",45:"Al-Jasiyah",46:"Al-Ahqaf",47:"Muhammad",48:"Al-Fath",49:"Al-Hujurat",50:"Qaf",51:"Az-Zariyat",52:"At-Tur",53:"An-Najm",54:"Al-Qamar",55:"Ar-Rahman",56:"Al-Waqi'ah",57:"Al-Hadid",58:"Al-Mujadilah",59:"Al-Hasyr",60:"Al-Mumtahanah",61:"As-Saff",62:"Al-Jumu'ah",63:"Al-Munafiqun",64:"At-Tagabun",65:"At-Talaq",66:"At-Tahrim",67:"Al-Mulk",68:"Al-Qalam",69:"Al-Haqqah",70:"Al-Ma'arij",71:"Nuh",72:"Al-Jinn",73:"Al-Muzammil",74:"Al-Muddassir",75:"Al-Qiyamah",76:"Al-Insan",77:"Al-Mursalat",78:"An-Naba'",79:"An-Nazi'at",80:"'Abasa",81:"At-Takwir",82:"Al-Infitar",83:"Al-Mutaffifin",84:"Al-Insyiqaq",85:"Al-Buruj",86:"At-Tariq",87:"Al-A'la",88:"Al-Ghasyiyah",89:"Al-Fajr",90:"Al-Balad",91:"Asy-Syams",92:"Al-Lail",93:"Ad-Duha",94:"Al-Insyirah",95:"At-Tin",96:"Al-'Alaq",97:"Al-Qadr",98:"Al-Bayyinah",99:"Az-Zalzalah",100:"Al-'Adiyat",101:"Al-Qari'ah",102:"At-Takasur",103:"Al-'Asr",104:"Al-Humazah",105:"Al-Fil",106:"Quraisy",107:"Al-Ma'un",108:"Al-Kausar",109:"Al-Kafirun",110:"An-Nasr",111:"Al-Lahab",112:"Al-Ikhlas",113:"Al-Falaq",114:"An-Nas"}
        return nama.get(n, default)
    
    def _arti(self, n, default):
        arti = {1:"Pembukaan",2:"Sapi Betina",3:"Keluarga Imran",4:"Wanita",5:"Jamuan Hidangan",6:"Binatang Ternak",7:"Tempat Tertinggi",8:"Rampasan Perang",9:"Pengampunan",10:"Nabi Yunus",11:"Nabi Hud",12:"Nabi Yusuf",13:"Guruh",14:"Nabi Ibrahim",15:"Gunung Batu",16:"Lebah",17:"Perjalanan Malam",18:"Penghuni Gua",19:"Maryam",20:"Thaha",21:"Para Nabi",22:"Haji",23:"Orang Mukmin",24:"Cahaya",25:"Pembeda",26:"Para Penyair",27:"Semut",28:"Cerita",29:"Laba-Laba",30:"Bangsa Romawi",31:"Luqman",32:"Sujud",33:"Golongan Bersatu",34:"Kaum Saba'",35:"Pencipta",36:"Yasin",37:"Barisan",38:"Shad",39:"Rombongan",40:"Yang Mengampuni",41:"Dijelaskan",42:"Musyawarah",43:"Perhiasan",44:"Kabut",45:"Berlutut",46:"Bukit Pasir",47:"Nabi Muhammad",48:"Kemenangan",49:"Kamar",50:"Qaf",51:"Angin Menerbangkan",52:"Bukit",53:"Bintang",54:"Bulan",55:"Maha Pengasih",56:"Hari Kiamat",57:"Besi",58:"Gugatan",59:"Pengusiran",60:"Perempuan Diuji",61:"Barisan",62:"Hari Jumat",63:"Orang Munafik",64:"Ditampakkan",65:"Talak",66:"Mengharamkan",67:"Kerajaan",68:"Pena",69:"Hari Kiamat",70:"Tempat Naik",71:"Nabi Nuh",72:"Jin",73:"Berselimut",74:"Berkemul",75:"Kiamat",76:"Manusia",77:"Malaikat Diutus",78:"Berita Besar",79:"Malaikat Mencabut",80:"Bermuka Masam",81:"Digulung",82:"Terbelah",83:"Curang",84:"Terbelah",85:"Gugusan Bintang",86:"Datang Malam",87:"Paling Tinggi",88:"Pembalasan",89:"Fajar",90:"Negeri",91:"Matahari",92:"Malam",93:"Duha",94:"Melapangkan",95:"Buah Tin",96:"Segumpal Darah",97:"Kemuliaan",98:"Bukti Nyata",99:"Gempa",100:"Kuda Berlari",101:"Hari Kiamat",102:"Bermegah-megahan",103:"Waktu",104:"Pengumpat",105:"Gajah",106:"Quraisy",107:"Barang Berguna",108:"Nikmat Berlimpah",109:"Orang Kafir",110:"Pertolongan",111:"Gejolak Api",112:"Ikhlas",113:"Waktu Subuh",114:"Manusia"}
        return arti.get(n, default)
    
    def _juz(self, n):
        if n<=2: return 1
        if n<=3: return 3
        if n<=4: return 4
        if n<=5: return 6
        if n<=6: return 7
        if n<=7: return 8
        if n<=8: return 9
        if n<=9: return 10
        if n<=10: return 11
        if n<=11: return 12
        if n<=12: return 13
        if n<=14: return 14
        if n<=16: return 15
        if n<=18: return 16
        if n<=20: return 17
        if n<=22: return 18
        if n<=24: return 19
        if n<=27: return 20
        if n<=29: return 21
        if n<=32: return 22
        if n<=34: return 23
        if n<=37: return 24
        if n<=41: return 25
        if n<=45: return 26
        if n<=50: return 27
        if n<=66: return 28
        if n<=77: return 29
        return 30
    
    def _local(self):
        print("📖 Memuat data lokal...")
        for i in range(1, 115):
            if i==1: nama,arab,arti,jml,tempat = "Al-Fatihah","الفاتحة","Pembukaan",7,"Makkiyah"
            elif i==2: nama,arab,arti,jml,tempat = "Al-Baqarah","البقرة","Sapi Betina",286,"Madaniyah"
            elif i==112: nama,arab,arti,jml,tempat = "Al-Ikhlas","الإخلاص","Ikhlas",4,"Makkiyah"
            elif i==113: nama,arab,arti,jml,tempat = "Al-Falaq","الفلق","Waktu Subuh",5,"Makkiyah"
            elif i==114: nama,arab,arti,jml,tempat = "An-Nas","الناس","Manusia",6,"Makkiyah"
            else: nama,arab,arti,jml,tempat = f"Surat {i}","سورة",f"Arti {i}",10,"Makkiyah" if i<10 else "Madaniyah"
            
            surat = SuratDetail(i, nama, nama, arab, arti, jml, tempat, self._juz(i), [])
            for j in range(1, min(jml,5)+1):
                if i==1 and j==1: t,tr = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ","Dengan nama Allah"
                elif i==112 and j==1: t,tr = "قُلْ هُوَ اللَّهُ أَحَدٌ","Katakanlah Dialah Allah"
                else: t,tr = f"آية {j}", f"Terjemahan {j}"
                surat.ayat_list.append(Ayat(j, t, "", tr, i, nama))
            self._data[i] = surat
        print(f"📊 LOCAL: {len(self._data)} surat")
    
    # Public methods
    def get_all_surat(self): return [s.to_dict() for s in self._data.values()]
    def get_surat_by_nomor(self, n): return self._data[n].to_dict() if n in self._data else None
    def get_surat_by_juz(self, j): return [s.to_dict() for s in self._data.values() if s.juz == j]
    def search(self, k): k=k.lower(); return [s.to_dict() for s in self._data.values() if k in s.nama.lower() or k in s.arti.lower()]
    def get_total_surat(self): return len(self._data)
    def get_total_ayat(self): return sum(len(s.ayat_list) for s in self._data.values())