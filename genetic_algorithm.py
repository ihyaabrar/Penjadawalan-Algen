import logging
import random
import math
from typing import List, Callable, Optional, Tuple, Dict
from jadwal_model import Jadwal

class AlgoritmaGenetika:
    def __init__(self,
                 data: Dict[str, List[Dict]],
                 ukuran_populasi: int = 50,
                 generasi: int = 100,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.1,
                 elitism_rate: float = 0.1):
        """
        Inisialisasi Algoritma Genetika dengan parameter yang dapat dikonfigurasi.
        
        Args:
            data: Dictionary yang berisi data mata kuliah per semester.
            ukuran_populasi: Ukuran populasi.
            generasi: Jumlah generasi.
            crossover_rate: Probabilitas crossover.
            mutation_rate: Probabilitas mutasi.
            elitism_rate: Persentase individu terbaik yang dipertahankan.
        """
        self.data = data
        self.ukuran_populasi = ukuran_populasi
        self.generasi = generasi
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        
        # Inisialisasi logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Statistik
        self.best_fitness = float('inf')
        self.best_solution = None
        self.metrics = {
            'generations': [],
            'best_fitness': [],
            'average_fitness': [],
            'diversity': [],
            'crossover_count': 0,
            'mutation_count': 0
        }
        
        # Validasi data
        self.validate_data()
        
    def validate_data(self):
        """
        Memvalidasi integritas data.
        """
        required_semesters = ['semester_2', 'semester_4', 'semester_6']
        
        for semester in required_semesters:
            if semester not in self.data:
                raise ValueError(f"Data untuk {semester} tidak ditemukan")
            
            for course in self.data[semester]:
                required_fields = ['kode', 'nama', 'sks', 'dosen']
                if not all(field in course for field in required_fields):
                    raise ValueError(f"Format mata kuliah tidak valid: {course}")
                    
                if not isinstance(course['sks'], int) or course['sks'] <= 0:
                    raise ValueError(f"SKS tidak valid untuk mata kuliah {course['nama']}")
                    
                if not isinstance(course['dosen'], list):
                    raise ValueError(f"Dosen harus berupa list untuk mata kuliah {course['nama']}")
                    
    def generate_random_jadwal(self) -> List[Jadwal]:
        """
        Menghasilkan jadwal acak berdasarkan data input.
        """
        jadwal = []
        
        # Gabungkan semua mata kuliah dari semua semester
        all_courses = []
        for semester in ['semester_2', 'semester_4', 'semester_6']:
            all_courses.extend(self.data[semester])
        
        for course in all_courses:
            # Generate waktu acak
            waktu = random.choice([
                {"mulai": 8*60, "selesai": 10*60},  # 08:00-09:40
                {"mulai": 10*60, "selesai": 12*60},  # 09:50-11:30
                {"mulai": 13*60, "selesai": 15*60},  # 13:00-14:40
                {"mulai": 15*60, "selesai": 17*60},  # 14:50-16:30
                {"mulai": 17*60, "selesai": 19*60}   # 16:40-18:20
            ])
            
            # Generate hari acak
            hari = random.choice(["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
            
            # Generate ruang acak
            ruang = random.choice([
                "301", "305", "306", "307", "314", "C204", "C302", "C407", 
                "C507", "C604", "C701", "C801", "C504", "C606", "C702"
            ])
            
            # Pilih dosen acak
            dosen = random.choice(course["dosen"])
            
            # Buat Jadwal
            jadwal.append(Jadwal(
                hari=hari,
                waktu_mulai=waktu["mulai"],
                waktu_selesai=waktu["selesai"],
                matakuliah=course,
                dosen=dosen,
                ruang=ruang,
                kelas=str(random.randint(1, 15)),  # Kelas 1-15 untuk pagi
                semester=int(semester.split("_")[-1])  # Ambil nomor semester
            ))
        
        return jadwal
        
    def calculate_fitness(self, individu: List[Jadwal]) -> float:
        """
        Menghitung fitness berdasarkan konflik jadwal.
        """
        conflicts = 0
        
        # Cek konflik ruang
        for i in range(len(individu)):
            for j in range(i + 1, len(individu)):
                jadwal_i = individu[i]
                jadwal_j = individu[j]
                
                if jadwal_i.hari == jadwal_j.hari:
                    if jadwal_i.ruang == jadwal_j.ruang:
                        if jadwal_i.overlaps(jadwal_j):
                            conflicts += 1
                    if jadwal_i.dosen == jadwal_j.dosen:
                        if jadwal_i.overlaps(jadwal_j):
                            conflicts += 1
                    if jadwal_i.kelas == jadwal_j.kelas:
                        if jadwal_i.semester == jadwal_j.semester:
                            if jadwal_i.overlaps(jadwal_j):
                                conflicts += 1
        
        # Normalisasi fitness
        fitness = 1 / (1 + conflicts)
        return fitness
        
    def tournament_selection(self, populasi: List[List[Jadwal]], tournament_size: int = 5) -> List[Jadwal]:
        """
        Seleksi turnamen untuk memilih individu terbaik.
        """
        selected = random.sample(populasi, tournament_size)
        return min(selected, key=lambda x: self.calculate_fitness(x))
        
    def crossover(self, parent1: List[Jadwal], parent2: List[Jadwal]) -> Tuple[List[Jadwal], List[Jadwal]]:
        """
        Melakukan crossover antara dua parent.
        """
        if random.random() > self.crossover_rate:
            return parent1, parent2
            
        # One-point crossover
        point = random.randint(1, len(parent1) - 1)
        
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        self.metrics['crossover_count'] += 1
        return child1, child2
        
    def mutate(self, individu: List[Jadwal]) -> List[Jadwal]:
        """
        Melakukan mutasi pada individu.
        """
        mutated = individu.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                # Mutasi waktu
                if random.random() < 0.33:
                    waktu = random.choice([
                        {"mulai": 8*60, "selesai": 10*60},
                        {"mulai": 10*60, "selesai": 12*60},
                        {"mulai": 13*60, "selesai": 15*60},
                        {"mulai": 15*60, "selesai": 17*60},
                        {"mulai": 17*60, "selesai": 19*60}
                    ])
                    mutated[i].waktu_mulai = waktu["mulai"]
                    mutated[i].waktu_selesai = waktu["selesai"]
                
                # Mutasi hari
                elif random.random() < 0.33:
                    hari = random.choice(["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
                    mutated[i].hari = hari
                
                # Mutasi ruang
                else:
                    ruang = random.choice([
                        "301", "305", "306", "307", "314", "C204", "C302", "C407", 
                        "C507", "C604", "C701", "C801", "C504", "C606", "C702"
                    ])
                    mutated[i].ruang = ruang
                
                self.metrics['mutation_count'] += 1
        
        return mutated
        
    def calculate_diversity(self, populasi: List[List[Jadwal]]) -> float:
        """
        Menghitung keragaman populasi.
        """
        if len(populasi) < 2:
            return 0.0
            
        diversity = 0.0
        for i in range(len(populasi)):
            for j in range(i + 1, len(populasi)):
                diff = sum(1 for k in range(len(populasi[i])) 
                          if populasi[i][k].to_dict() != populasi[j][k].to_dict())
                diversity += diff
        
        return diversity / (len(populasi) * (len(populasi) - 1) * len(populasi[0]))
        
    def run(self) -> Tuple[List[Jadwal], float, dict]:
        """
        Menjalankan algoritma genetika.
        """
        # Inisialisasi populasi
        populasi = [self.generate_random_jadwal() for _ in range(self.ukuran_populasi)]
        
        for gen in range(self.generasi):
            # Evaluasi populasi
            fitness_scores = [self.calculate_fitness(ind) for ind in populasi]
            
            # Simpan statistik
            self.metrics['generations'].append(gen)
            self.metrics['best_fitness'].append(min(fitness_scores))
            self.metrics['average_fitness'].append(sum(fitness_scores) / len(fitness_scores))
            self.metrics['diversity'].append(self.calculate_diversity(populasi))
            
            # Logging
            self.logger.info(f"Generasi {gen + 1}/{self.generasi}")
            self.logger.info(f"Fitness terbaik: {min(fitness_scores):.4f}")
            self.logger.info(f"Fitness rata-rata: {sum(fitness_scores) / len(fitness_scores):.4f}")
            self.logger.info(f"Keragaman: {self.calculate_diversity(populasi):.4f}")
            
            # Seleksi elit
            num_elites = max(2, int(self.ukuran_populasi * self.elitism_rate))
            elites = sorted(populasi, key=lambda x: self.calculate_fitness(x))[:num_elites]
            
            # Buat generasi baru
            new_populasi = elites.copy()
            
            while len(new_populasi) < self.ukuran_populasi:
                # Seleksi parent
                parent1 = self.tournament_selection(populasi)
                parent2 = self.tournament_selection(populasi)
                
                # Crossover
                children = self.crossover(parent1, parent2)
                
                # Mutasi
                for child in children:
                    new_child = self.mutate(child)
                    new_populasi.append(new_child)
                    
                    # Jika sudah mencapai ukuran populasi, hentikan
                    if len(new_populasi) >= self.ukuran_populasi:
                        break
            
            # Update populasi
            populasi = new_populasi[:self.ukuran_populasi]
            
            # Update solusi terbaik
            current_best = min(populasi, key=lambda x: self.calculate_fitness(x))
            current_fitness = self.calculate_fitness(current_best)
            
            if current_fitness < self.best_fitness:
                self.best_fitness = current_fitness
                self.best_solution = current_best
                
            # Cek kondisi berhenti
            if self.best_fitness <= 0:
                self.logger.info("Solusi optimal ditemukan!")
                break
            
            if gen >= self.generasi - 1:
                self.logger.info("Mencapai batas generasi maksimum")
        
        # Ringkasan hasil
        self.logger.info("\nRingkasan Hasil:")
        self.logger.info(f"Fitness terbaik: {self.best_fitness:.4f}")
        self.logger.info(f"Jumlah crossover: {self.metrics['crossover_count']}")
        self.logger.info(f"Jumlah mutasi: {self.metrics['mutation_count']}")
        
        return self.best_solution, self.best_fitness, self.metrics