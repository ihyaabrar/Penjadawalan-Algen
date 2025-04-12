from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class Hari(Enum):
    SENIN = "Senin"
    SELASA = "Selasa"
    RABU = "Rabu"
    KAMIS = "Kamis"
    JUMAT = "Jumat"

class Kelas(Enum):
    PAGI = "pagi"
    MALAM = "malam"

class Matakuliah:
    def __init__(self, kode: str, nama: str, sks: int):
        self.kode = kode
        self.nama = nama
        self.sks = sks

    def __eq__(self, other):
        return isinstance(other, Matakuliah) and self.kode == other.kode

@dataclass
class Jadwal:
    hari: Hari
    waktu_mulai: int  # Waktu dalam menit dari tengah malam
    waktu_selesai: int  # Waktu dalam menit dari tengah malam
    matakuliah: Matakuliah
    dosen: str
    ruang: str
    kelas: Kelas
    semester: int
    
    def __post_init__(self):
        self._validate_time()
        self._validate_semester()
    
    def _validate_time(self):
        if self.waktu_mulai >= self.waktu_selesai:
            raise ValueError("Waktu mulai harus lebih awal dari waktu selesai")
            
        if self.waktu_mulai < 0 or self.waktu_selesai > 24*60:
            raise ValueError("Waktu harus dalam rentang 0-1440 menit")
    
    def _validate_semester(self):
        if self.semester not in [2, 4, 6]:
            raise ValueError("Semester harus 2, 4, atau 6")
    
    def overlaps(self, other: 'Jadwal') -> bool:
        """Memeriksa apakah dua jadwal bertabrakan."""
        if self.hari != other.hari or self.ruang != other.ruang:
            return False
            
        return (self.waktu_mulai < other.waktu_selesai and other.waktu_mulai < self.waktu_selesai)
    
    def get_duration(self) -> int:
        """Mengembalikan durasi jadwal dalam menit."""
        return self.waktu_selesai - self.waktu_mulai
    
    def to_dict(self) -> Dict:
        """Mengembalikan representasi dictionary dari jadwal."""
        return {
            "hari": self.hari.value,
            "waktu_mulai": self.waktu_mulai,
            "waktu_selesai": self.waktu_selesai,
            "matakuliah": {
                "kode": self.matakuliah.kode,
                "nama": self.matakuliah.nama,
                "sks": self.matakuliah.sks
            },
            "dosen": self.dosen,
            "ruang": self.ruang,
            "kelas": self.kelas.value,
            "semester": self.semester
        }
    
    def __str__(self):
        # Convert menit ke format HH:MM
        start_hour = self.waktu_mulai // 60
        start_minute = self.waktu_mulai % 60
        end_hour = self.waktu_selesai // 60
        end_minute = self.waktu_selesai % 60
        
        return (f"{self.hari.value}, {start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}, "
                f"{self.matakuliah.nama}, {self.dosen}, {self.ruang}, "
                f"Kelas {self.kelas.value}, Semester {self.semester}")