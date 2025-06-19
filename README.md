# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institute adalah salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Jaya Jaya Institute dikenal sebagai institusi yang menerima siswa dari berbagai macam kalangan. Institusi pendidikan ini memiliki kelas pagi dan malam dan menyediakan lebih dari 10 pilihan jurusan yang beragam, mulai dari teknologi hingga layanan sosial.

### Permasalahan Bisnis

Permasalahan bisnis utama yang dihadapi oleh Jaya Jaya Institute adalah **tingginya dropout rate**, yang berarti banyak siswa tidak menyelesaikan pendidikannya sampai lulus. Hal ini disebabkan oleh beberapa faktor:

1. **Banyaknya jurusan yang harus diawasi** - Dengan lebih dari 10 jurusan, sulit untuk memantau performa setiap program secara mendetail
2. **Faktor finansial** - Biaya pendidikan dan status penghutang siswa
3. **Faktor akademis** - Performa nilai semester yang menurun
4. **Faktor demografis** - Usia dan gender siswa
5. **Faktor sosial** - Kebutuhan pendidikan khusus dan status beasiswa

Tingginya dropout rate ini merugikan institusi dari segi reputasi dan pendapatan, serta merugikan siswa yang kehilangan kesempatan pendidikan.

### Cakupan Proyek

Proyek ini mencakup tiga area utama:

1. **Analisis Data Eksploratif**
   - Menganalisis faktor-faktor penyebab tingginya dropout rate
   - Identifikasi pola dan tren dalam data siswa
   - Evaluasi performa per jurusan dan karakteristik siswa

2. **Pengembangan Model Machine Learning**
   - Membangun model prediksi dropout menggunakan Random Forest
   - Evaluasi dan validasi model
   - Deployment model untuk prediksi real-time

3. **Business Dashboard**
   - Membangun dashboard interaktif menggunakan Streamlit
   - Visualisasi data dengan filter dinamis
   - Tools untuk monitoring dan decision-making

### Persiapan

**Sumber data:** [Dicoding Dataset - Students Performance](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance)

**Setup environment:**

```bash
# Membuat virtual environment
python -m venv venv

# Aktivasi environment (Windows)
venv\Scripts\activate

# Aktivasi environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies yang dibutuhkan:**
```
streamlit
pandas
numpy
plotly
scikit-learn
joblib
matplotlib
```

## Business Dashboard

Dashboard interaktif telah dibuat menggunakan Streamlit dengan fitur-fitur berikut:

### 🎛️ **Filter Controls**
Pada bagian atas dashboard, terdapat empat filter utama:

1. **Status Siswa** - Dropout, Not Dropout (dengan sub-kategori Enrolled/Graduated)
2. **Jurusan/Course** - Semua jurusan yang tersedia (single selection)
3. **Waktu Kuliah** - Daytime (pagi) dan Evening (malam)
4. **Gender** - Male dan Female

### 📊 **Key Metrics**
- **Dropout Rate** - Persentase siswa yang dropout (prominent display)
- **Total Students** - Jumlah total siswa berdasarkan filter
- **Breakdown Status** - Jumlah siswa per kategori (Dropout, Enrolled, Graduated)

### 📈 **Visualisasi Data**

1. **Scholarship Holders by Status** - Bar chart penerima beasiswa berdasarkan status
2. **Average Grades per Semester** - Perbandingan nilai semester 1 dan 2 dengan analisis selisih
3. **Dropout Rate by Course** - Horizontal bar chart dropout rate per jurusan
4. **Student Characteristics** (Pie charts):
   - Educational Special Needs Distribution
   - Debtor Distribution  
   - Tuition Fees Up to Date Distribution
5. **Age Demographics** - Histogram usia pendaftaran dengan statistik (min, avg, max)

### 🔗 **Link Dashboard**
[**Akses Dashboard di sini**](https://student-performance-analyst-hadhi98.streamlit.app/)

## Menjalankan Sistem Machine Learning

Sistem prediksi dropout menggunakan algoritma **Random Forest** dengan langkah-langkah berikut:

### 🚀 **Cara Penggunaan Online**

1. **Buka Dashboard**
   ```
   https://student-performance-analyst-hadhi98.streamlit.app/
   ```

2. **Pilih Tab Prediction**
   - Klik "Prediction" pada sidebar navigation

3. **Input Data Siswa**
   - **Course**: Pilih jurusan (wajib diisi)
   - **Personal Info**: Gender, Age at enrollment, Admission grade
   - **Academic & Financial**: Special needs, Debtor status, Tuition status, Scholarship
   - **Grades**: First semester dan Second semester grades

4. **Prediksi**
   - Klik tombol "🔍 Predict Dropout Risk"
   - Hasil akan menampilkan:
     - **HIGH RISK**: Student likely to dropout (dengan rekomendasi)
     - **LOW RISK**: Student NOT likely to dropout (dengan rekomendasi)

### 💻 **Menjalankan Local**

```bash
# Clone repository
git clone <repository-url>
cd jaya-jaya-institute-analysis

# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run streamlit_app.py
```

### ⚠️ **Catatan Penting**
- Field "Course" harus dipilih (tidak boleh "None")
- Input numerik memiliki batas minimum dan maksimum
- Tekan Enter setelah mengisi nilai numerik
- Model akan menampilkan error message jika ada input yang tidak valid

## Conclusion

### 📊 **Temuan Utama**

1. **Faktor Finansial Dominan**
   - **32.2%** siswa dengan biaya pendidikan terbaru melakukan dropout
   - **22%** dari pelaku dropout adalah penghutang
   - Siswa penerima beasiswa memiliki dropout rate rendah (hanya **10%**)

2. **Pola Akademis**
   - Siswa dropout cenderung mengalami **penurunan nilai** dari semester 1 ke semester 2
   - Performa akademis yang konsisten berkorelasi dengan tingkat kelulusan

3. **Disparitas Antar Jurusan**
   - **Biofuel Production Technologies**: 66.67% dropout rate (12 siswa)
   - **Equinculture**: 55.32% dropout rate (62 siswa)
   - **Informatics Engineering**: 54.12% dropout rate

4. **Faktor Demografis**
   - Gender dan usia mempengaruhi tingkat dropout di beberapa jurusan
   - Perlu pembatasan usia untuk optimalisasi success rate

### Rekomendasi Action Items

Berdasarkan analisis data, Jaya Jaya Institute disarankan untuk mengimplementasikan strategi berikut:

#### 🏦 **1. Revisi Kebijakan Finansial**
- **Evaluasi biaya pendidikan terbaru** - Lakukan market research untuk memastikan kompetitivitas harga
- **Program beasiswa yang diperluas** - Tingkatkan jumlah penerima beasiswa untuk mengurangi dropout rate
- **Sistem pembayaran fleksibel** - Tawarkan cicilan atau program work-study untuk mengurangi beban finansial

#### 📚 **2. Peningkatan Support Akademis** 
- **Early Warning System** - Implementasikan monitoring otomatis untuk siswa dengan penurunan nilai
- **Academic Mentoring Program** - Assign mentor untuk siswa berisiko tinggi
- **Remedial Classes** - Sediakan kelas tambahan untuk siswa yang mengalami kesulitan

#### 🎯 **3. Evaluasi Program Studi**
- **Review kurikulum** jurusan dengan dropout rate tinggi (Biofuel, Equinculture, Informatics)
- **Quality assurance** untuk pengajar dan materi pembelajaran
- **Industry alignment** - Pastikan kurikulum sesuai dengan kebutuhan industri

#### 👥 **4. Targeted Intervention**
- **Gender-specific support** - Program khusus untuk gender minority di jurusan tertentu
- **Age consideration** - Implementasikan batas usia maksimal (≤50 tahun) untuk optimalisasi resources
- **Special needs accommodation** - Enhanced support untuk siswa dengan kebutuhan khusus

#### 📊 **5. Continuous Monitoring**
- **Dashboard monitoring** - Gunakan dashboard untuk tracking real-time metrics
- **Predictive analytics** - Implementasikan model ML untuk early detection
- **Regular evaluation** - Review quarterly untuk mengukur efektivitas intervensi

---

**Developed by:** Dwi Hadi Yulvi Baskoro (@hadhibaskoro)  
**Technology Stack:** Python, Streamlit, Plotly, Scikit-learn, Pandas  
**Model:** Random Forest Classifier  
**Deployment:** Streamlit Cloud