```
# Sistem Pakar Forward Chaining - Diagnosis Kualitas Desain Digital

**Nama:** Lale Juliesti Ayuningkusuma  
**NIM:** F1D02510064  
**Mata Kuliah:** Kecerdasan Buatan (MKL1303131) - Teknik Informatika UNRAM  

---

## 1. Topik dan Cara Menjalankan

**Topik:** Diagnosis masalah kualitas desain digital (poster, ilustrasi, materi visual) berdasarkan tiga aspek utama: keterbacaan teks (kontras), ketajaman gambar saat dicetak (resolusi), dan kesesuaian warna layar dengan hasil cetak (RGB vs CMYK).

* **Bahasa:** Python 3 (diuji pada Python versi terbaru), tanpa memerlukan *library* eksternal tambahan.
* **Berkas Utama:**
* `pakar_desain_visual.py` (Mesin inferensi *Forward Chaining* dan antarmuka CLI).
* `aturan_kualitas_desain.json` (Basis pengetahuan berisi aturan, pertanyaan, saran, dan referensi sumber).
* `hasil_pengujian.txt` (Dokumen transkrip lengkap berisi 5 skenario pengujian sistem).
* `screenshot/` (Folder berisi tangkapan layar terminal dari hasil eksekusi program).

* **Cara Menjalankan (dari folder repository):**
```bash
python pakar_desain_visual.py

```
Jawab setiap pertanyaan interaktif yang muncul dengan mengetik `y` (ya) atau `t` (tidak). Pastikan nilai rasio kontras dan resolusi (ppi) telah diperiksa sebelumnya menggunakan alat bantu seperti pengecek kontras atau dialog *Image Size* pada aplikasi desain.

---

## 2. Sumber dan Tabel Aturan

Basis pengetahuan disusun berdasarkan dokumentasi standar aksesibilitas dan alur kerja desain profesional dari W3C serta Adobe:

| ID | Sumber Referensi |
| --- | --- |
| S1 | *Understanding SC 1.4.3: Contrast (Minimum) (Level AA)*. W3C Web Accessibility Initiative. |
| S2 | *Resize images*. Adobe Photoshop Help. |
| S3 | *Image size, resolution, and resampling in Photoshop*. Adobe Photoshop Help. |
| S4 | *About color modes*. Adobe Creative Cloud Help. |
| S5 | *Choose a CMYK equivalent for a non-printable color*. Adobe Photoshop Help. |

Aturan dalam `aturan_kualitas_desain.json` merupakan adaptasi dan parafrase langsung dari sumber-sumber tersebut:

| Aturan | IF (Kondisi) | THEN (Kesimpulan) | Sumber |
| --- | --- | --- | --- |
| R1 | teks berukuran normal **AND** rasio kontras teks di bawah 4,5:1 | kontras teks kurang | S1 |
| R2 | teks berukuran besar **AND** rasio kontras teks di bawah 3:1 | kontras teks kurang | S1 |
| R3 | desain akan dicetak **AND** resolusi gambar di bawah 300 ppi pada ukuran cetak akhir | resolusi cetak kurang | S2, S3 |
| R4 | resolusi cetak kurang **AND** hasil cetak gambar terlihat buram atau pecah | gambar buram karena resolusi rendah | S3 |
| R5 | desain dibuat dalam mode RGB **AND** desain akan dicetak **AND** warna hasil cetak terlihat lebih kusam dari layar | perbedaan gamut warna RGB ke CMYK | S4, S5 |

**Penjelasan Alur & Rantai Aturan:**

Rantai penalaran terbentuk melalui aturan beruntun seperti $R3 \rightarrow R4$, di mana keluaran suatu aturan menjadi fakta baru bagi aturan berikutnya. Program dirancang untuk menampilkan kesimpulan akhir berupa fakta turunan yang tidak lagi bertindak sebagai syarat bagi aturan aktif lainnya.

---

## 3. Metode: Forward Chaining

Pendekatan *Forward Chaining* (penalaran maju) dipilih karena proses diagnosis umumnya dimulai dari pengumpulan gejala di lapangan (seperti teks yang sulit dibaca, hasil cetak buram, atau warna yang kusam) menuju diagnosis akhir masalah.

**Algoritma Singkat:**

1. Memori awal diisi dengan fakta-fakta yang dijawab "ya" oleh pengguna.
2. Program melakukan perulangan untuk mencocokkan aturan yang kondisi syaratnya terpenuhi oleh memori dan kesimpulannya belum ada di dalam memori.
3. Jika ditemukan, aturan tersebut dieksekusi dengan menambahkan kesimpulannya ke memori.
4. Proses berulang hingga tidak ada lagi aturan baru yang dapat diaktifkan.

Program juga dilengkapi validasi untuk menolak kombinasi jawaban yang bertentangan secara logika (misalnya menyatakan ukuran teks normal dan besar secara bersamaan).

---

## 4. Kasus Uji

Pengujian dilakukan melalui 5 skenario utama untuk menguji ketepatan aturan tunggal, rantai bertingkat, kasus negatif, hingga validasi konflik:

| # | Skenario / Fokus Uji | Jawaban "ya" (Nomor Pertanyaan) | Kesimpulan / Hasil Diagnosis |
| --- | --- | --- | --- |
| 1 | Diagnostik Kontras Teks | Pertanyaan 1, 2 | kontras teks kurang (R1) |
| 2 | Resolusi Cetak Bertingkat | Pertanyaan 5, 6, 7 | gambar buram karena resolusi rendah ($R3 \rightarrow R4$) |
| 3 | Kasus Negatif (Normal) | Pertanyaan 5 saja | *tidak ada masalah yang dapat disimpulkan* |
| 4 | Manajemen Warna Cetak | Pertanyaan 5, 8, 9 | perbedaan gamut warna RGB ke CMYK (R5) |
| 5 | Validasi Konflik Fakta | Pertanyaan 1 & 3 bersamaan | Program menolak input & berhenti (*Conflict Detection*) |

Seluruh log keluaran pengujian secara lengkap tercatat di dalam berkas `hasil_pengujian.txt`.

**Dokumentasi Screenshot Pengujian:**

* **Kasus 1:** `screenshot/kasus1.png`
* **Kasus 2:** `screenshot/kasus2.png`
* **Kasus 3:** `screenshot/kasus3.png`

---

## 5. Batas Keberlakuan

Sistem pakar ini berbasis standar dokumentasi resmi W3C (WCAG 2.1) dan panduan Adobe Photoshop, sehingga berfokus khusus pada tiga aspek teknis: keterbacaan kontras teks, resolusi cetak, dan perbedaan ruang warna RGB-CMYK. Program ini tidak mengevaluasi aspek estetika visual, tata letak artistik secara menyeluruh, atau standar khusus dari percetakan tertentu. Hasil diagnosis bersifat sebagai rekomendasi awal dan bukan pengganti pertimbangan profesional desainer.

---

## 6. Penggunaan Alat Bantu AI

Dalam pengerjaan tugas ini, saya memanfaatkan AI sebagai alat bantu untuk mendiskusikan struktur kode, merapikan format basis pengetahuan, serta membantu merumuskan dokumentasi berdasarkan arahan dan ide orisinal saya sendiri. Seluruh isi aturan logika, referensi sumber, serta implementasi program telah saya pelajari, teliti, dan verifikasi sendiri kebenarannya.

```