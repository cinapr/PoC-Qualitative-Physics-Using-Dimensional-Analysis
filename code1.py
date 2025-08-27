# -*- coding: utf-8 -*-
# Kode ini mengimplementasikan logika penalaran kualitatif berdasarkan paper
# "Qualitative Physics Using Dimensional Analysis" oleh Bhaskar dan Nigam.
# Tujuan utama adalah untuk mendeteksi kontradiksi logis dalam sistem
# regulator tekanan.

# --- 1. Mendefinisikan status kualitatif (simbolik) ---
# Kita menggunakan string untuk merepresentasikan status, bukan angka.
NAIK = "Increased"
TURUN = "Decreased"
KONSTAN = "Constant"

# --- 2. Mendefinisikan variabel dan status awal mereka ---
# Gunakan kamus untuk menyimpan status setiap variabel.
# Awalnya, semua status tidak diketahui ('?')
variabel_status = {
    'Pin': None,
    'Pout': None,
    'Q': None,
    'A_open': None,
    'rho': KONSTAN,  # Kerapatan (rho) diasumsikan konstan
    'x': None,
    'P': None,
    'K': KONSTAN,    # Konstanta pegas (K) diasumsikan konstan
}

# --- 3. Mendefinisikan hubungan logika antar variabel ---
# Ini adalah inti dari model. Kita terjemahkan persamaan Pi menjadi aturan logis.
# Aturan-aturan ini didasarkan pada hubungan berbanding lurus dan terbalik.
# Contoh: Jika A dan B di pembilang, maka mereka berbanding terbalik.
# Setiap aturan adalah sebuah kamus yang mendefinisikan hubungan.
aturan_logika = [
    # Hubungan dari Grup Pi_A1: Q * rho^1/2 / (A_open * Pin^3/2)
    # Tujuan kita adalah menjaga rasio ini konstan
    {'rel_type': 'inv_proportional', 'vars': ['Q', 'A_open'], 'constant_vars': ['Pin', 'rho']},
    {'rel_type': 'inv_proportional', 'vars': ['Q', 'Pin'], 'constant_vars': ['A_open', 'rho']},
    {'rel_type': 'inv_proportional', 'vars': ['A_open', 'Pin'], 'constant_vars': ['Q', 'rho']},

    # Hubungan dari Grup Pi_A2: P_out / P_in
    {'rel_type': 'proportional', 'vars': ['P_out', 'P_in']},

    # Hubungan dari Grup Pi_B1: (x * P) / K
    {'rel_type': 'inv_proportional', 'vars': ['x', 'P'], 'constant_vars': ['K']},

    # Hubungan dari Grup Pi_C1: P / P_out
    {'rel_type': 'proportional', 'vars': ['P', 'P_out']},

    # Hubungan dari Grup Pi_C2: A_open / x
    {'rel_type': 'proportional', 'vars': ['A_open', 'x']},
]

def tentukan_status(status1, status2, hubungan):
    """Fungsi pembantu untuk menentukan status baru berdasarkan dua status lain dan hubungannya."""
    if hubungan == 'proportional':
        # Jika berbanding lurus, output sama dengan input
        if status1 == status2:
            return KONSTAN
        elif status1 == NAIK and status2 == TURUN:
            return TURUN
        elif status1 == TURUN and status2 == NAIK:
            return TURUN
    elif hubungan == 'inv_proportional':
        # Jika berbanding terbalik, output berlawanan dengan input
        if status1 == status2:
            return TURUN
        elif status1 == NAIK and status2 == TURUN:
            return KONSTAN
        elif status1 == TURUN and status2 == NAIK:
            return KONSTAN
    # Kasus kompleks atau tidak dapat ditentukan
    return None

def propagate(states, rules):
    """
    Fungsi utama untuk menyebarkan (propagate) status variabel
    dan mendeteksi kontradiksi.
    """
    did_change = True
    contradictions = {}
    
    # Ulangi proses propagasi hingga tidak ada lagi perubahan
    while did_change:
        did_change = False
        
        # Periksa setiap aturan logika
        for rule in rules:
            vars_to_check = rule['vars']
            
            # Cek jika kita bisa menentukan satu variabel dari variabel lainnya
            for i in range(len(vars_to_check)):
                
                # Variabel yang ingin kita tentukan
                target_var = vars_to_check[i]
                
                # Jika variabel target sudah punya status, lewati
                if states.get(target_var) is not None:
                    continue

                # Kumpulkan status dari variabel lain di aturan
                other_vars = [v for j, v in enumerate(vars_to_check) if i != j]
                
                # Cek jika semua variabel lain sudah diketahui statusnya
                if all(states.get(v) is not None for v in other_vars):
                    # Terapkan logika untuk menentukan status target
                    # Logika ini perlu lebih kompleks untuk kasus 3+ variabel
                    # Untuk kesederhanaan, kita asumsikan hubungan 2 variabel utama
                    
                    status_a = states.get(other_vars[0])
                    status_b = states.get(other_vars[1]) if len(other_vars) > 1 else None
                    
                    # Logika ini hanya berfungsi untuk hubungan sederhana 2 variabel
                    if rule['rel_type'] == 'proportional':
                        new_state = status_a
                    elif rule['rel_type'] == 'inv_proportional':
                        new_state = NAIK if status_a == TURUN else TURUN

                    # Lakukan propagasi (mengupdate status)
                    if states.get(target_var) is None:
                        states[target_var] = new_state
                        did_change = True
                    # Deteksi kontradiksi
                    elif states.get(target_var) != new_state:
                        if target_var not in contradictions:
                            contradictions[target_var] = [states[target_var], new_state]
    
    return contradictions

# --- 4. Main Program (Skenario Pengguna) ---
if __name__ == "__main__":
    # Skenario 1: Pin turun, Pout konstan
    print("Skenario 1: Pin = Turun, Pout = Konstan")
    variabel_status['Pin'] = TURUN
    variabel_status['Pout'] = KONSTAN
    
    print("\nStatus awal:")
    print(variabel_status)

    # Jalankan propagasi
    kontradiksi_ditemukan = propagate(variabel_status, aturan_logika)
    
    print("\nStatus akhir setelah propagasi:")
    print(variabel_status)
    
    if kontradiksi_ditemukan:
        print("\n!!! KONTRA DIKSI DITEMUKAN !!!")
        for var, states in kontradiksi_ditemukan.items():
            print(f"- Variabel '{var}' memiliki status konflik: {states[0]} dan {states[1]}")
    else:
        print("\nTidak ada kontradiksi yang ditemukan. Skenario ini logis.")

    # Anda bisa coba skenario lain di sini
    # Skenario 2: Pin naik, Pout turun
    print("\n" + "="*50)
    print("Skenario 2: Pin = Naik, Pout = Turun")
    variabel_status = {
        'Pin': NAIK,
        'Pout': TURUN,
        'Q': None, 'A_open': None, 'rho': KONSTAN, 'x': None, 'P': None, 'K': KONSTAN,
    }
    print("\nStatus awal:")
    print(variabel_status)
    kontradiksi_ditemukan = propagate(variabel_status, aturan_logika)
    print("\nStatus akhir setelah propagasi:")
    print(variabel_status)
    if kontradiksi_ditemukan:
        print("\n!!! KONTRA DIKSI DITEMUKAN !!!")
        for var, states in kontradiksi_ditemukan.items():
            print(f"- Variabel '{var}' memiliki status konflik: {states[0]} dan {states[1]}")
    else:
        print("\nTidak ada kontradiksi yang ditemukan. Skenario ini logis.")
