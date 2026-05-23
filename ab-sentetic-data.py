import numpy as np
import pandas as pd

# 1. Tekrarlanabilirlik için şansı sabitliyoruz (Kabul Kriteri)
np.random.seed(42)

# 2. Veri Üretimi
n_sayisi = 50 # Her form tipi için 50'şer kullanıcı denemiş olsun

# Grup A (Uzun Form - Eski Sistem): Ortalama 45 saniye, Standart Sapma 10
kayit_sure_A = np.random.normal(loc=45, scale=10, size=n_sayisi)

# Grup B (Adımlı Form - Yeni Sistem): Ortalama 38 saniye, Standart Sapma 8
kayit_sure_B = np.random.normal(loc=38, scale=8, size=n_sayisi)

# Eksi veya 5 saniyenin altında imkansız kayıt süreleri çıkmasın diye sınır koyuyoruz
kayit_sure_A = np.clip(kayit_sure_A, 5, None)
kayit_sure_B = np.clip(kayit_sure_B, 5, None)

# 3. Verileri Tabloya Çevirme (Sütun isimlerini senaryoya göre ayarladık)
veri_A = pd.DataFrame({
    'Kullanici_ID': range(1, n_sayisi + 1), 
    'Grup': 'A_Uzun_Form', 
    'Kayit_Suresi_Saniye': np.round(kayit_sure_A, 1) # Daha gerçekçi dursun diye 1 ondalığa yuvarladık
})

veri_B = pd.DataFrame({
    'Kullanici_ID': range(n_sayisi + 1, (2 * n_sayisi) + 1), 
    'Grup': 'B_Adimli_Form', 
    'Kayit_Suresi_Saniye': np.round(kayit_sure_B, 1)
})

# İki grubu alt alta birleştir
tum_veri = pd.concat([veri_A, veri_B], ignore_index=True)

# 4. CSV Olarak Kaydet
tum_veri.to_csv('kayit_sureleri_ab_testi.csv', index=False)

print("Senaryo 3 verisi başarıyla 'kayit_sureleri_ab_testi.csv' olarak kaydedildi!")