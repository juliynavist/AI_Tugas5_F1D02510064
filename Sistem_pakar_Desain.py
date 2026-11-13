"""Sistem pakar sederhana: diagnosis masalah kualitas desain digital.
Metode: Forward Chaining (mesin ditulis sendiri, tanpa library tambahan).
Pengetahuan dibaca dari kb_desain.json.
"""
import json
import os
import sys

BERKAS_KB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kb_desain.json")


def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def syarat_terpenuhi(aturan, memori):
    """mode 'dan' = semua syarat ada di memori, mode 'atau' = salah satu cukup."""
    if aturan["mode"] == "dan":
        return all(s in memori for s in aturan["jika"])
    return any(s in memori for s in aturan["jika"])


def fakta_dasar(kb):
    """Fakta yang tidak pernah menjadi hasil aturan -> ditanyakan ke user (urut kemunculan)."""
    hasil_aturan = {a["maka"] for a in kb["aturan"]}
    urut = []
    for a in kb["aturan"]:
        for s in a["jika"]:
            if s not in hasil_aturan and s not in urut:
                urut.append(s)
    return urut


def forward_chaining(aturan, fakta_awal):
    """Mulai dari fakta awal, jalankan aturan yang cocok, ulangi sampai tidak ada aturan baru."""
    memori = set(fakta_awal)
    asal = {}       # fakta turunan -> aturan yang menghasilkannya
    log = []        # urutan aturan yang dijalankan
    while True:
        cocok = [a for a in aturan
                 if a["maka"] not in memori and syarat_terpenuhi(a, memori)]
        if not cocok:
            break
        r = cocok[0]                 # ambil aturan pertama
        memori.add(r["maka"])
        asal[r["maka"]] = r          # bahan "alasan"
        log.append(r)
    return memori, asal, log


def cari_kesimpulan(asal, memori):
    """Kesimpulan = fakta turunan yang tidak dipakai sebagai syarat oleh aturan yang sudah berjalan."""
    terpakai = set()
    for r in asal.values():
        terpakai.update(s for s in r["jika"] if s in memori)
    return [f for f in asal if f not in terpakai]


def tanya(nomor, teks):
    while True:
        try:
            jawab = input(f"{nomor}. {teks} (y/t) > ").strip().lower()
        except EOFError:
            print("\nInput berakhir sebelum semua pertanyaan terjawab.")
            sys.exit(1)
        if not sys.stdin.isatty():
            print(jawab)  # supaya transkrip dari input pipa tetap terbaca
        if jawab in ("y", "ya"):
            return True
        if jawab in ("t", "tidak", "n"):
            return False
        print("   Jawab dengan y atau t.")


def jelaskan(fakta, asal, memori, kunci_sumber, indent=0):
    """Cetak rantai alasan secara rekursif: fakta <- aturan (syarat yang dipakai)."""
    r = asal[fakta]
    dipakai = [s for s in r["jika"] if s in memori]
    kunci_sumber.update(r["sumber"])
    print("  " * (indent + 1) + f"{fakta} <- {r['id']} ({', '.join(dipakai)}) [{', '.join(r['sumber'])}]")
    for s in dipakai:
        if s in asal:
            jelaskan(s, asal, memori, kunci_sumber, indent + 1)


def main():
    kb = muat_kb(BERKAS_KB)
    print(kb["judul"])
    print("Jawab y/t.")

    dasar = fakta_dasar(kb)
    awal = []
    for i, f in enumerate(dasar, 1):
        if tanya(i, kb["pertanyaan"][f]):
            awal.append(f)

    for a, b in kb.get("bertentangan", []):
        if a in awal and b in awal:
            print(f"\nJawaban bertentangan: '{a}' dan '{b}' tidak mungkin keduanya ya. Ulangi program.")
            sys.exit(1)

    print("\nFakta awal:", ", ".join(awal) if awal else "(tidak ada)")
    print()

    memori, asal, log = forward_chaining(kb["aturan"], awal)
    for n, r in enumerate(log, 1):
        print(f"Siklus {n}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(log) + 1}: tidak ada aturan baru, berhenti\n")

    kesimpulan = cari_kesimpulan(asal, memori)
    if not kesimpulan:
        print("Kesimpulan: tidak ada masalah yang dapat disimpulkan dari fakta yang diberikan.")
    else:
        print("Kesimpulan:", "; ".join(kesimpulan))
        print("Alasan:")
        kunci_sumber = set()
        for k in kesimpulan:
            jelaskan(k, asal, memori, kunci_sumber)
        print("Saran:")
        for k in kesimpulan:
            print(f"  - {k}: {kb['saran'][k]}")
        print("Sumber:")
        for s in sorted(kunci_sumber):
            print(f"  {s}: {kb['sumber'][s]}")

    print("\nCatatan:", kb["batas"])

if __name__ == "__main__":
    main()