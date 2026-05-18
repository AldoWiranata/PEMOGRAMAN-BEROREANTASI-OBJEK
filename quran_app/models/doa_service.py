import random
import json
import os
from datetime import datetime

class DoaService:
    def __init__(self, data_file="doa_data.json"):
        self.data_file = data_file
        self.doa_list = self._load_data()
    
    def _load_data(self):
        
        doa_default = [
            {"id": 1, "nama": "Doa Sebelum Tidur", 
             "arab": "بِاسْمِكَ اللَّهُمَّ أَحْيَا وَأَمُوتُ",
             "latin": "Bismikallahumma ahya wa amut",
             "artinya": "Dengan nama-Mu ya Allah aku hidup dan aku mati"},
            
            {"id": 2, "nama": "Doa Bangun Tidur",
             "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا",
             "latin": "Alhamdulillahilladzi ahyana ba'da ma amatana",
             "artinya": "Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami"},
            
            {"id": 3, "nama": "Doa Sebelum Makan",
             "arab": "اللَّهُمَّ بَارِكْ لَنَا فِيمَا رَزَقْتَنَا",
             "latin": "Allahumma barik lana fima razaqtana",
             "artinya": "Ya Allah, berkahilah rezeki yang Engkau berikan kepada kami"},
            
            {"id": 4, "nama": "Doa Sesudah Makan",
             "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا",
             "latin": "Alhamdulillahilladzi ath'amana wa saqana",
             "artinya": "Segala puji bagi Allah yang telah memberi makan dan minum kepada kami"},
            
            {"id": 5, "nama": "Doa Masuk Masjid",
             "arab": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
             "latin": "Allahummaftah li abwaba rahmatika",
             "artinya": "Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu"},
            
            {"id": 6, "nama": "Doa Keluar Masjid",
             "arab": "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ",
             "latin": "Allahumma inni as'aluka min fadhlika",
             "artinya": "Ya Allah, aku memohon kepada-Mu sebagian dari karunia-Mu"},
            
            {"id": 7, "nama": "Doa Masuk Kamar Mandi",
             "arab": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ",
             "latin": "Allahumma inni a'udzubika minal khubutsi wal khabaitsi",
             "artinya": "Ya Allah, aku berlindung kepada-Mu dari gangguan setan"},
            
            {"id": 8, "nama": "Doa Keluar Kamar Mandi",
             "arab": "غُفْرَانَكَ", "latin": "Ghufranaka", "artinya": "Aku memohon ampunan-Mu"},
            
            {"id": 9, "nama": "Doa Sebelum Belajar",
             "arab": "رَبِّ زِدْنِي عِلْمًا", "latin": "Rabbi zidni 'ilma",
             "artinya": "Ya Tuhanku, tambahkanlah ilmu kepadaku"},
            
            {"id": 10, "nama": "Doa Sesudah Belajar",
             "arab": "اللَّهُمَّ إِنِّي أَسْتَوْدِعُكَ مَا عَلَّمْتَنِيهِ",
             "latin": "Allahumma inni astaudi'uka ma 'allamtaniihi",
             "artinya": "Ya Allah, aku menitipkan ilmu yang Engkau ajarkan kepadaku"},
            
            {"id": 11, "nama": "Doa Untuk Orang Tua",
             "arab": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا",
             "latin": "Rabbirhamhuma kama rabbayani shaghira",
             "artinya": "Ya Tuhanku, sayangilah keduanya sebagaimana mereka menyayangiku"},
            
            {"id": 12, "nama": "Doa Masuk Rumah",
             "arab": "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ الْمَوْلِجِ",
             "latin": "Allahumma inni as'aluka khairal mauliji",
             "artinya": "Ya Allah, aku memohon kepada-Mu sebaik-baik tempat masuk"},
            
            {"id": 13, "nama": "Doa Keluar Rumah",
             "arab": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ",
             "latin": "Bismillahi tawakkaltu 'alallah",
             "artinya": "Dengan nama Allah, aku bertawakal kepada Allah"},
            
            {"id": 14, "nama": "Doa Naik Kendaraan",
             "arab": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا",
             "latin": "Subhanalladzi sakhkhara lana hadza",
             "artinya": "Maha Suci Allah yang menundukkan kendaraan ini untuk kami"},
            
            {"id": 15, "nama": "Doa Keselamatan Dunia Akhirat",
             "arab": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً",
             "latin": "Rabbana atina fid dunya hasanah",
             "artinya": "Ya Tuhan kami, berilah kami kebaikan di dunia"}
        ]
        
        # Coba load dari file JSON dulu
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("doa_harian"):
                        print(f"✅ Loaded {len(data['doa_harian'])} doa from file")
                        return data['doa_harian']
            except Exception as e:
                print(f"⚠️ Gagal load file: {e}")
        
        # Jika file tidak ada, gunakan doa_default
        print(f"✅ Menggunakan {len(doa_default)} doa default")
        return doa_default
    
    def get_all_doa(self):
        
        return self.doa_list
    
    def get_random_doa(self):
        """Mengembalikan doa secara acak"""
        if self.doa_list:
            return random.choice(self.doa_list)
        return {"arab": "بِسْمِ اللَّهِ", "artinya": "Dengan nama Allah"}
    
    def get_doa_by_id(self, doa_id):
        """Mengembalikan doa berdasarkan ID"""
        for doa in self.doa_list:
            if doa.get("id") == doa_id:
                return doa
        return None
    
    def get_daily_doa(self):
        """Mengembalikan doa hari ini (berdasarkan tanggal)"""
        if self.doa_list:
            today = datetime.now().day
            index = (today - 1) % len(self.doa_list)
            return self.doa_list[index]
        return None
    
    def get_total_doa(self):
        """Mengembalikan jumlah total doa"""
        return len(self.doa_list)