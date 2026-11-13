"""
Sistem Pakar Forward Chaining - Diagnosis Kualitas Desain Visual
Nama: Lale Juliesti Ayuningkusuma
NIM: F1D02510064
"""
import json
import os
import sys

FILE_ATURAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aturan_kualitas_desain.json")


def muat_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cari_pertanyaan_dasar(kb):
    hasil_rule = {r["maka"] for r in kb["aturan"]}
    list_tanya = []
    for r in kb["aturan"]:
        for s in r["jika"]:
            if s not in hasil_rule and s not in list_tanya:
                list_tanya.append(s)
    return list_tanya


def forward_chain(rules, fakta_awal):
    """Mesin penelusuran forward chaining yang ringkas."""
    memori = set(fakta_awal)
    riwayat = []
    siklus = 1
    
    while True:
        baru = False
        for r in rules:
            if r["mode"] == "dan":
                cocok = all(s in memori for s in r["jika"])
            else:
                cocok = any(s in memori for s in r["jika"])

            if cocok and r["maka"] not in memori:
                memori.add(r["maka"])
                riwayat.append(r)
                baru = True
                print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")

        if not baru:
            break
        siklus += 1

    peta_rule = {r['maka']: r for r in rules}
    return memori, peta_rule, riwayat


def ambil_kesimpulan(peta_rule, memori):
    terpakai = set()
    for r in peta_rule.values():
        terpakai.update(s for s in r["jika"] if s in memori)
    return [f for f in peta_rule if f not in terpakai and f in memori]


def tanya_user(no, teks):
    while True:
        try:
            ans = input(f"{no}. {teks} (y/t) > ").strip().lower()
        except EOFError:
            sys.exit(1)
        if not sys.stdin.isatty():
            print(ans)
        if ans in ("y", "ya"):
            return True
        if ans in ("t", "tidak", "n"):
            return False
        print("   Jawab y atau t.")


def cetak_alasan(target, peta, memori, sumber_set, indent=0):
    if target not in peta:
        return
    r = peta[target]
    pakai = [s for s in r["jika"] if s in memori]
    sumber_set.update(r["sumber"])
    
    print("  " * (indent + 1) + f"{target} <- {r['id']} ({', '.join(pakai)}) [{', '.join(r['sumber'])}]")
    for sub in pakai:
        if sub in peta:
            cetak_alasan(sub, peta, memori, sumber_set, indent + 1)


def main():
    kb = muat_json(FILE_ATURAN)
    print(kb["judul"])
    print("Jawab y/t.")

    pertanyaan = cari_pertanyaan_dasar(kb)
    fakta_awal = []
    for i, p in enumerate(pertanyaan, 1):
        if tanya_user(i, kb["pertanyaan"][p]):
            fakta_awal.append(p)

    for a, b in kb.get("bertentangan", []):
        if a in fakta_awal and b in fakta_awal:
            print(f"\nKonflik: '{a}' dan '{b}' tidak boleh ya bersamaan.")
            sys.exit(1)

    print("\nFakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()

    memori, peta, log = forward_chain(kb["aturan"], fakta_awal)
    print(f"Siklus {len(log) + 1}: tidak ada aturan baru, berhenti\n")

    kesimpulan = ambil_kesimpulan(peta, memori)
    if not kesimpulan:
        print("Kesimpulan: tidak ada masalah yang dapat disimpulkan dari fakta yang diberikan.")
    else:
        print("Kesimpulan:", "; ".join(kesimpulan))
        print("Alasan:")
        sumber_set = set()
        for k in kesimpulan:
            cetak_alasan(k, peta, memori, sumber_set)
        print("Saran:")
        for k in kesimpulan:
            print(f"  - {k}: {kb['saran'][k]}")
        print("Sumber:")
        for s in sorted(sumber_set):
            print(f"  {s}: {kb['sumber'][s]}")

    print("\nCatatan:", kb["batas"])


if __name__ == "__main__":
    main()