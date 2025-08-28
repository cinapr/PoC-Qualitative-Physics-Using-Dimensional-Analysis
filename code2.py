# -*- coding: utf-8 -*-
# Kode ini mengimplementasikan logika penalaran kualitatif kualitatif
# untuk sistem regulator tekanan, sesuai dengan tugas yang diberikan.
#
# Tujuan utama kode ini adalah:
# a. Memungkinkan pengguna menentukan status (Naik, Turun, Konstan) untuk variabel.
# b. Menyebarkan status ini ke variabel lain menggunakan hubungan Pi.
# c. Mendeteksi dan melaporkan kontradiksi jika ada.

# --- 1. Mendefinisikan status kualitatif (simbolik) ---
# Menggunakan string untuk merepresentasikan status.
NAIK = "Increased"
TURUN = "Decreased"
KONSTAN = "Constant"
TIDAK_DIKETAHUI = None

# --- 2. Mendefinisikan Model: Variabel dan Aturan Pi ---
# Kamus untuk menyimpan status setiap variabel.
# Variabel 'rho' dan 'K' diasumsikan konstan.
variabel_status = {
    'Pin': TIDAK_DIKETAHUI,
    'Pout': TIDAK_DIKETAHUI,
    'Q': TIDAK_DIKETAHUI,
    'A_open': TIDAK_DIKETAHUI,
    'rho': KONSTAN,
    'x': TIDAK_DIKETAHUI,
    'P': TIDAK_DIKETAHUI,
    'K': KONSTAN,
}

# --- 3. Aturan Logika Kualitatif Berdasarkan Hubungan Pi ---
# Kita akan mendefinisikan aturan sebagai fungsi untuk setiap grup Pi.
# Ini lebih mudah dipahami dan diuji daripada menggunakan kamus aturan.

def propagate_pi_a1(status):
    """
    Logika untuk Pi_A1 = (Q * rho^1/2) / (A_open * Pin^3/2)
    Karena Pi_A1 konstan, jika salah satu di pembilang atau penyebut berubah,
    variabel lain harus berubah untuk menyeimbangkannya.
    """
    if status['Q'] == NAIK:
        # Jika Q naik, maka (A_open * Pin) harus naik
        # Ini menyiratkan bahwa A_open atau Pin atau keduanya harus naik
        # Karena ini tidak bisa ditentukan secara pasti, kita tidak bisa menetapkan nilai.
        # Logika ini hanya bisa bekerja jika satu variabel konstan.
        # Contoh sederhana: Jika Pin dan rho konstan, dan Q naik, maka A_open harus naik.
        if status['Pin'] == KONSTAN and status['rho'] == KONSTAN:
            return {'A_open': NAIK}
    if status['A_open'] == TURUN:
        if status['Pin'] == KONSTAN and status['rho'] == KONSTAN:
            return {'Q': TURUN}
    # Tambahkan lebih banyak kondisi sesuai kebutuhan jika Pin atau A_open diketahui dan yang lain tidak
    return {}

def propagate_pi_a2(status):
    """
    Logika untuk Pi_A2 = Pout / Pin
    Pout dan Pin berbanding lurus.
    """
    if status['Pin'] == NAIK:
        return {'Pout': NAIK}
    if status['Pin'] == TURUN:
        return {'Pout': TURUN}
    if status['Pout'] == NAIK:
        return {'Pin': NAIK}
    if status['Pout'] == TURUN:
        return {'Pin': TURUN}
    return {}

def propagate_pi_b1(status):
    """
    Logika untuk Pi_B1 = (x * P) / K
    x dan P berbanding terbalik (karena K konstan).
    """
    if status['x'] == NAIK:
        return {'P': TURUN}
    if status['x'] == TURUN:
        return {'P': NAIK}
    if status['P'] == NAIK:
        return {'x': TURUN}
    if status['P'] == TURUN:
        return {'x': NAIK}
    return {}

def propagate_pi_c1(status):
    """
    Logika untuk Pi_C1 = P / Pout
    P dan Pout berbanding lurus.
    """
    if status['Pout'] == NAIK:
        return {'P': NAIK}
    if status['Pout'] == TURUN:
        return {'P': TURUN}
    if status['P'] == NAIK:
        return {'Pout': NAIK}
    if status['P'] == TURUN:
        return {'Pout': TURUN}
    return {}

def propagate_pi_c2(status):
    """
    Logika untuk Pi_C2 = x / A_open^1/2
    x dan A_open berbanding lurus.
    """
    if status['x'] == NAIK:
        return {'A_open': NAIK}
    if status['x'] == TURUN:
        return {'A_open': TURUN}
    if status['A_open'] == NAIK:
        return {'x': NAIK}
    if status['A_open'] == TURUN:
        return {'x': TURUN}
    return {}

def propagate_all_rules(status):
    """Menjalankan semua fungsi propagasi secara berulang."""
    did_change = True
    while did_change:
        did_change = False
        
        # Simpan status sebelum perubahan
        initial_status = status.copy()
        
        # Jalankan propagasi dari setiap aturan
        status.update(propagate_pi_a1(status))
        status.update(propagate_pi_a2(status))
        status.update(propagate_pi_b1(status))
        status.update(propagate_pi_c1(status))
        status.update(propagate_pi_c2(status))
        
        # Cek apakah ada perubahan yang terjadi
        if initial_status != status:
            did_change = True
    return status

# --- 4. Main Program (Skenario Pengguna) ---
if __name__ == "__main__":
    
    # === Skenario 1: Sesuai dengan tugas (Regulator bekerja) ===
    # Tentukan tujuan kualitatif
    print("Skenario 1: Pin = Turun, Pout = Konstan")
    variabel_status_1 = variabel_status.copy()
    variabel_status_1['Pin'] = TURUN
    variabel_status_1['Pout'] = KONSTAN
    
    print("\nStatus Awal:")
    print(variabel_status_1)
    
    # Jalankan propagasi
    status_akhir_1 = propagate_all_rules(variabel_status_1)
    
    print("\nStatus Akhir Setelah Propagasi:")
    print(status_akhir_1)
    
    # Cek kontradiksi
    kontradiksi_1 = {}
    for var, status in status_akhir_1.items():
        if isinstance(status, list) and len(status) > 1:
            kontradiksi_1[var] = status
            
    if kontradiksi_1:
        print("\n!!! KONTRA DIKSI DITEMUKAN !!!")
        for var, states in kontradiksi_1.items():
            print(f"- Variabel '{var}' memiliki status konflik: {states[0]} dan {states[1]}")
    else:
        print("\nTidak ada kontradiksi yang ditemukan. Skenario ini logis.")
        
    # === Skenario 2: Contoh Kontradiksi ===
    # Tentukan tujuan kualitatif yang bertentangan
    print("\n" + "="*50)
    print("Skenario 2: Pin = Naik, Pout = Turun")
    variabel_status_2 = variabel_status.copy()
    variabel_status_2['Pin'] = NAIK
    variabel_status_2['Pout'] = TURUN
    
    print("\nStatus Awal:")
    print(variabel_status_2)
    
    # Jalankan propagasi
    status_akhir_2 = propagate_all_rules(variabel_status_2)
    
    print("\nStatus Akhir Setelah Propagasi:")
    print(status_akhir_2)
    
    # Cek kontradiksi
    kontradiksi_2 = {}
    for var, status in status_akhir_2.items():
        if isinstance(status, list) and len(status) > 1:
            kontradiksi_2[var] = status
            
    if kontradiksi_2:
        print("\n!!! KONTRA DIKSI DITEMUKAN !!!")
        for var, states in kontradiksi_2.items():
            print(f"- Variabel '{var}' memiliki status konflik: {states[0]} dan {states[1]}")
    else:
        print("\nTidak ada kontradiksi yang ditemukan. Skenario ini logis.")
