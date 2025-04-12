from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import json
import os

class DataValidationError(Exception):
    """Exception untuk validasi data yang tidak valid."""
    pass

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        """Membuat direktori data jika belum ada."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    @lru_cache(maxsize=1)
    def load_data(self) -> Dict:
        """
        Memuat data mata kuliah, ruang, dan kelas untuk semester 2, 4, dan 6.
        Menggunakan caching untuk performa yang lebih baik.
        
        Returns:
            Dict: Dictionary yang berisi data mata kuliah, ruang, dan kelas.
        """
        data_file = os.path.join(self.data_dir, "schedule_data.json")
        
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            data = self._generate_default_data()
            self._save_data(data)
        
        self._validate_data(data)
        return data
    
    def _generate_default_data(self) -> Dict:
        """Menghasilkan data default jika file tidak ada."""
        semester_2 = [
            {"kode": "21EM222005", "nama": "Statistik Ekonomi", "sks": 3, "dosen": ["Fuad Ramdhan Ryanto, S.E.Ak., M.Ak.", "Joko Suseno, S.E., M.Ak., ACPA."]},
            {"kode": "21EM222006", "nama": "Mikro Ekonomi", "sks": 3, "dosen": ["Samsuddin, S.E., M.Si.", "Lita Afriyanti, S.E., M.M."]},
            {"kode": "21EM222007", "nama": "Ekonomi Islam", "sks": 2, "dosen": ["Sukardi, S.E., M.M.", "Nurlia, S.EI., M.Sc. IBF"]},
            {"kode": "21EM222008", "nama": "Manajemen Koperasi", "sks": 3, "dosen": ["Neni Triana M, S.E., M.M.", "Irfan Mahdi, S.E., M.M.", "Dr. Norasari Arani S.E., M.M.", "M. Faris Fakhri, S.M."]},
            {"kode": "21EM222009", "nama": "Etika Bisnis", "sks": 2, "dosen": ["Meizi Fachrizal, S.E., M.Si.", "Ananda Archie, S.E., M.A.B", "Darusman, B.Ec., M.Innov.Entr."]},
            {"kode": "21EM222010", "nama": "Hukum Bisnis", "sks": 2, "dosen": ["Mahardika Agung Madepo, S.I.Kom., M.B.A.", "Anisa Azzaulfa, S.H., M.H."]},
            {"kode": "21UM211006", "nama": "AIK 2 (Ibadah, Muamalah & Akhlak)", "sks": 2, "dosen": ["Eli, S.Ag., M.Pd.I.", "Musliadi, S.Sos.I., S.Pd.I., M.Pd."]},
            {"kode": "21UM211009", "nama": "Pendidikan Kewarganegaraan", "sks": 2, "dosen": ["Budianto, S.H., M.H."]},
            {"kode": "21UM211008", "nama": "English for Specific Purposes (ESP)", "sks": 2, "dosen": ["Ryani Yulian, M.Pd.", "Primatasha Desvira Dizza, M.Pd."]}
        ]
        
        semester_4 = [
            {"kode": "21EM422018", "nama": "Ekonomi dan Bisnis Global", "sks": 3, "dosen": ["Neni Triana M, S.E., M.M.", "M. Ebuziyya Aif. Ramadhan., S.E., M.M.", "Isyanti Khairunnisa, S.M., M.M."]},
            {"kode": "21EM422019", "nama": "Manajemen Keuangan Lanjutan", "sks": 3, "dosen": ["Edy Suryadi, S.E., M.M.", "Nurlia, S.EI., M.Sc. IBF", "M. Rizky Oktavianto, S.E., M.M."]},
            {"kode": "21EM422020", "nama": "Manajemen Sumber Daya Manusia Lanjutan", "sks": 3, "dosen": ["Devi Yasmin, S.E., M.M.", "Eru Ahmadia, S.E., M.M.", "Irfan Mahdi, S.E., M.M."]},
            {"kode": "21EM422021", "nama": "Manajemen Pemasaran Lanjutan", "sks": 3, "dosen": ["Ananda Archie, S.E., M.A.B", "Novita Puteri, S.E., M.M."]},
            {"kode": "21EM422022", "nama": "Kewirausahaan: Praktek", "sks": 2, "dosen": ["Samsuddin, S.E., M.Si.", "Fita Kurniasari, S.M.B., M.A.B.", "Sukardi, S.E., M.M."]},
            {"kode": "21EM422023", "nama": "Aplikasi Komputer", "sks": 2, "dosen": ["Fenni Supriadi, S.E., M.M.", "Arninda, S.Kom., M.M."]},
            {"kode": "21EM422024", "nama": "Ekonomi Manajerial", "sks": 3, "dosen": ["Dr. Dedi Hariyanto, S.E., M.M.", "Lina Budiarti, S.E., M.M."]},
            {"kode": "21UM411011", "nama": "AIK 4 (Islam dan Ilmu Pengetahuan)", "sks": 2, "dosen": ["Hermanto, S.Pd.I., M.Pd.I.", "Rahmat, S.Sy., M.H."]}
        ]
        
        semester_6 = [
            {"kode": "21EM623133", "nama": "Manajemen Keuangan Internasional", "sks": 4, "dosen": ["Heni Safitri, S.E., M.M."]},
            {"kode": "21EM623234", "nama": "Manajemen Pemasaran Internasional", "sks": 3, "dosen": ["Sumiyati, S.E., M.M."]},
            {"kode": "21EM623335", "nama": "Manajemen Sumber Daya Manusia Internasional", "sks": 3, "dosen": ["Devi Yasmin, S.E., M.M."]},
            {"kode": "21EM622036", "nama": "Sistem Informasi Manajemen", "sks": 3, "dosen": ["Dr. Dedi Hariyanto, S.E., M.M.", "Fita Kurniasari, S.M.B., M.A.B.", "Arninda, S.Kom., M.M.", "Ferdy Firmansyah, S.Kom., M.Kom."]},
            {"kode": "21EM622037", "nama": "Manajemen Operasional", "sks": 3, "dosen": ["Syafrani Daniel, S.E., M.M."]},
            {"kode": "21EM622038", "nama": "Penganggaran Perusahaan", "sks": 3, "dosen": ["Edy Suryadi, S.E., M.M.", "Zulmuis Mardan, S.E., M.M.", "Riski Anshori, S.E., M.M."]},
            {"kode": "21EM622039", "nama": "Metode Penelitian", "sks": 3, "dosen": ["Heni Safitri, S.E., M.M.", "Sumiyati, S.E., M.M."]}
        ]
        
        ruang_kuliah = ["301", "305", "306", "307", "314", "C204", "C302", "C407", "C507", "C604", "C701", "C801", "C504", "C606", "C702"]
        kelas_pagi = ["1", "4", "6", "9", "11", "12", "13", "14", "15"]
        kelas_malam = ["2"]
        
        return {
            "semester_2": semester_2,
            "semester_4": semester_4,
            "semester_6": semester_6,
            "ruang_kuliah": ruang_kuliah,
            "kelas_pagi": kelas_pagi,
            "kelas_malam": kelas_malam
        }
    
    def _save_data(self, data: Dict):
        """Menyimpan data ke file JSON."""
        data_file = os.path.join(self.data_dir, "schedule_data.json")
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _validate_data(self, data: Dict):
        """Memvalidasi integritas data."""
        required_fields = ["semester_2", "semester_4", "semester_6", "ruang_kuliah", "kelas_pagi", "kelas_malam"]
        
        for field in required_fields:
            if field not in data:
                raise DataValidationError(f"Field {field} tidak ditemukan dalam data")
            
        # Validasi semester
        for semester in ["semester_2", "semester_4", "semester_6"]:
            if not isinstance(data[semester], list):
                raise DataValidationError(f"{semester} harus berupa list")
            
            for course in data[semester]:
                if not all(key in course for key in ["kode", "nama", "sks", "dosen"]):
                    raise DataValidationError("Format mata kuliah tidak valid")
                
                if not isinstance(course["sks"], int) or course["sks"] <= 0:
                    raise DataValidationError("SKS harus berupa angka positif")
                
                if not isinstance(course["dosen"], list):
                    raise DataValidationError("Dosen harus berupa list")
    
    def get_semester_courses(self, semester: int) -> List[Dict]:
        """Mengambil daftar mata kuliah untuk semester tertentu."""
        if semester not in [2, 4, 6]:
            raise ValueError("Semester harus 2, 4, atau 6")
            
        semester_key = f"semester_{semester}"
        return self.load_data()[semester_key]
    
    def get_available_rooms(self) -> List[str]:
        """Mengambil daftar ruang kuliah yang tersedia."""
        return self.load_data()["ruang_kuliah"]
    
    def get_available_classes(self, semester: int) -> List[str]:
        """Mengambil daftar kelas yang tersedia untuk semester tertentu."""
        if semester not in [2, 4, 6]:
            raise ValueError("Semester harus 2, 4, atau 6")
            
        if semester == 6:
            return []  # Semester 6 tidak memiliki kelas
            
        return self.load_data()["kelas_pagi"]

data_loader = DataLoader()  # Singleton instance

# Fungsi kompatibel dengan kode lama
def load_data():
    return data_loader.load_data()