import logging
from typing import List, Callable, Optional, Tuple
from jadwal_model import Jadwal
import random
import math

class TabuSearch:
    def __init__(self,
                 objective_function: Callable,
                 initial_solution: List[Jadwal],
                 max_iter: int = 100,
                 tabu_size: int = 10,
                 aspiration_threshold: float = 0.1,
                 diversification_threshold: float = 0.8,
                 intensification_threshold: float = 0.9):
        """
        Inisialisasi Tabu Search dengan parameter yang dapat dikonfigurasi.
        """
        self.objective = objective_function
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.best_fitness = self.objective(initial_solution)
        self.tabu_list = []
        self.max_iter = max_iter
        self.tabu_size = tabu_size
        self.aspiration_threshold = aspiration_threshold
        self.diversification_threshold = diversification_threshold
        self.intensification_threshold = intensification_threshold
        
        # Inisialisasi logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def get_neighbors(self, solution: List[Jadwal]) -> List[List[Jadwal]]:
        """
        Menghasilkan tetangga-tetangga dari solusi yang diberikan.
        """
        neighbors = []
        
        # Generate tetangga dengan swap
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                # Swap ruang
                neighbor = solution.copy()
                neighbor[i].ruang, neighbor[j].ruang = neighbor[j].ruang, neighbor[i].ruang
                neighbors.append(neighbor)
                
                # Swap waktu
                neighbor = solution.copy()
                neighbor[i].waktu_mulai, neighbor[j].waktu_mulai = neighbor[j].waktu_mulai, neighbor[i].waktu_mulai
                neighbor[i].waktu_selesai, neighbor[j].waktu_selesai = neighbor[j].waktu_selesai, neighbor[i].waktu_selesai
                neighbors.append(neighbor)
                
                # Swap dosen
                neighbor = solution.copy()
                neighbor[i].dosen, neighbor[j].dosen = neighbor[j].dosen, neighbor[i].dosen
                neighbors.append(neighbor)
        
        # Tambahkan variasi dengan mengubah waktu secara acak
        for i in range(len(solution)):
            neighbor = solution.copy()
            time_diff = random.randint(-30, 30)  # Perubahan waktu dalam menit
            neighbor[i].waktu_mulai = max(0, min(24*60, neighbor[i].waktu_mulai + time_diff))
            neighbor[i].waktu_selesai = max(0, min(24*60, neighbor[i].waktu_selesai + time_diff))
            neighbors.append(neighbor)
        
        return neighbors
        
    def aspiration_criteria(self, solution: List[Jadwal], fitness: float) -> bool:
        """
        Kriteria aspirasi untuk memungkinkan solusi yang lebih baik di luar daftar tabu.
        """
        return fitness < self.best_fitness * (1 - self.aspiration_threshold)
        
    def diversification(self, solution: List[Jadwal]) -> bool:
        """
        Strategi diversifikasi untuk menjauh dari solusi yang tidak produktif.
        """
        current_fitness = self.objective(solution)
        return current_fitness > self.best_fitness * (1 - self.diversification_threshold)
        
    def intensification(self, solution: List[Jadwal]) -> bool:
        """
        Strategi intensifikasi untuk fokus pada solusi yang menjanjikan.
        """
        current_fitness = self.objective(solution)
        return current_fitness < self.best_fitness * (1 - self.intensification_threshold)
        
    def update_tabu_list(self, move: Tuple[List[Jadwal], List[Jadwal]]):
        """
        Memperbarui daftar tabu dengan move terbaru.
        """
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_size:
            self.tabu_list.pop(0)
        
    def search(self) -> Tuple[List[Jadwal], float, dict]:
        """
        Melakukan pencarian menggunakan Tabu Search.
        """
        metrics = {
            'iterations': [],
            'best_fitness': [],
            'current_fitness': [],
            'tabu_size': [],
            'diversification_count': 0,
            'intensification_count': 0
        }
        
        diversification_count = 0
        intensification_count = 0
        
        for iteration in range(self.max_iter):
            neighbors = self.get_neighbors(self.current_solution)
            best_neighbor = None
            best_fitness = float('inf')
            
            for neighbor in neighbors:
                fitness = self.objective(neighbor)
                move = (self.current_solution, neighbor)
                
                # Cek apakah move ada di daftar tabu
                if move not in self.tabu_list:
                    if fitness < best_fitness:
                        best_neighbor = neighbor
                        best_fitness = fitness
                
                # Cek kriteria aspirasi
                if self.aspiration_criteria(neighbor, fitness):
                    best_neighbor = neighbor
                    best_fitness = fitness
                    break
            
            if best_neighbor is None:
                # Jika tidak ada tetangga yang valid, gunakan diversifikasi
                diversification_count += 1
                metrics['diversification_count'] += 1
                
                # Pilih tetangga secara acak
                best_neighbor = random.choice(neighbors)
                best_fitness = self.objective(best_neighbor)
            
            # Update solusi terbaik
            if best_fitness < self.best_fitness:
                self.best_solution = best_neighbor
                self.best_fitness = best_fitness
                
                # Cek intensifikasi
                if self.intensification(best_neighbor):
                    intensification_count += 1
                    metrics['intensification_count'] += 1
            
            # Update solusi saat ini
            self.current_solution = best_neighbor
            self.update_tabu_list((self.current_solution, best_neighbor))
            
            # Catat metrik
            metrics['iterations'].append(iteration)
            metrics['best_fitness'].append(self.best_fitness)
            metrics['current_fitness'].append(best_fitness)
            metrics['tabu_size'].append(len(self.tabu_list))
            
            # Logging
            self.logger.info(f"Iterasi {iteration + 1}/{self.max_iter}")
            self.logger.info(f"Fitness terbaik: {self.best_fitness:.4f}")
            self.logger.info(f"Ukuran daftar tabu: {len(self.tabu_list)}")
            
            # Cek kondisi berhenti
            if self.best_fitness <= 0:
                self.logger.info("Solusi optimal ditemukan!")
                break
            
            if iteration >= self.max_iter - 1:
                self.logger.info("Mencapai batas iterasi maksimum")
        
        # Ringkasan hasil
        self.logger.info("\nRingkasan Hasil:")
        self.logger.info(f"Fitness terbaik: {self.best_fitness:.4f}")
        self.logger.info(f"Jumlah diversifikasi: {diversification_count}")
        self.logger.info(f"Jumlah intensifikasi: {intensification_count}")
        
        return self.best_solution, self.best_fitness, metrics