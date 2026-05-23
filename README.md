# 📊 A/B Testi 101: Veri Bilimi Özet İstatistik ve Basit A/B Düşüncesi

Bu proje, bir e-ticaret veya web uygulamasında kayıt formunun tasarımı değiştirildiğinde (Eski Uzun Form vs. Yeni Adımlı Form) kullanıcıların kayıt sürelerinin nasıl değiştiğini incelemektedir. Veri bilimi prensipleri çerçevesinde özet istatistikleri sunar, şans faktörünü elemeyi amaçlayan bir Permütasyon Testi simülasyonu çalıştırır ve p-hacking (veri manipülasyonu) tuzaklarını ele alır.

---

## 🔍 1. Veri Kaynağı ve Sentetik Veri Üretimi

Projedeki veriler, gerçek dünya kayıt sürelerini taklit etmek üzere sentetik olarak üretilmiştir. 

* **Veri Üretim Kodu:** [ab-sentetic-data.py](file:///c:/Users/DELL/Dropbox/PC/Desktop/ab-testing-101/ab-sentetic-data.py)
* **Yöntem:** NumPy kütüphanesinin normal dağılım fonksiyonu (`np.random.normal`) kullanılarak iki grup için kayıt süreleri üretilmiştir. Sürelerin mantıklı sınırlar içinde kalması için minimum 5 saniye filtresi uygulanmıştır.
* **Tekrarlanabilirlik:** Verinin her çalıştırıldığında aynı şekilde üretilmesi için rastgele sayı üreteci seed'i `np.random.seed(42)` olarak sabitlenmiştir.
* **Oluşan Veri Seti:** [kayit_sureleri_ab_testi.csv](file:///c:/Users/DELL/Dropbox/PC/Desktop/ab-testing-101/kayit_sureleri_ab_testi.csv) (100 satır: 50 satır A grubu, 50 satır B grubu).

---

## 📊 2. Özet İstatistik Tablosu

Üretilen veri setinden elde edilen temel özet istatistikler aşağıdaki gibidir:

| Grup (Tasarım Tipi) | Kullanıcı Sayısı ($n$) | Ortalama Kayıt Süresi (Saniye) | Standart Sapma (Saniye) |
| :--- | :---: | :---: | :---: |
| **A_Uzun_Form** *(Eski Sistem)* | 50 | **42.75** | 9.33 |
| **B_Adimli_Form** *(Yeni Sistem)* | 50 | **38.14** | 6.99 |

* **Gözlemlenen Ortalama Fark (Observed Difference):** Yeni tasarım (B grubu), eski tasarıma (A grubu) göre ortalama **4.61 saniye** daha hızlı kayıt tamamlanmasını sağlamıştır.

---

## 🎲 3. İstatistiksel Karşılaştırma: Permütasyon Testi (Randomization Test)

İki grup arasındaki bu 4.61 saniyelik farkın **şans eseri** mi oluştuğunu yoksa **tasarımın gerçek etkisinden** mi kaynaklandığını anlamak için **Permütasyon Testi** (Rastgeleleştirme Testi) uygulanmıştır.

> [!NOTE]
> ### Permütasyon Testinin Mantığı
> 1. A grubundan 50 ve B grubundan 50 olmak üzere tüm 100 kişinin kayıt süresini tek bir torbaya atıp iyice karıştırıyoruz.
> 2. Bu torbadan rastgele 50'şer kişilik iki yeni yapay grup çekiyoruz ve aralarındaki ortalama farkı hesaplıyoruz.
> 3. Bu karıştırma ve yeniden grup oluşturma işlemini tam **10.000 kez** tekrarlıyoruz (Simülasyon).
> 4. Bu 10.000 şans eseri denemede elde ettiğimiz yapay farkların kaç tanesinin, bizim ilk başta bulduğumuz **4.61 saniyelik gerçek farktan** büyük veya eşit olduğunu sayıyoruz.
> 5. **Sonuç (p-değeri):** Yaptığımız analizde $p = 0.0055$ (%0.55) bulunmuştur. Yani, gruplar arasında hiçbir gerçek fark olmasaydı bile şans eseri böyle bir fark görme ihtimalimiz 10.000'de sadece 55'tir. Bu oran kabul gören kritik sınır olan %5'ten ($p < 0.05$) küçük olduğu için, **yeni tasarımın kayıt sürelerini kısalttığı istatistiksel olarak kanıtlanmıştır.**

### Matematiksel İfade
$$p\text{-değeri} = \frac{\sum_{i=1}^{N} I(|\text{diff\_perm}_i| \ge |\text{diff\_obs}|)}{N}$$
* *Burada $N = 10.000$ simülasyon sayısını, $\text{diff\_obs}$ gerçekte bulduğumuz farkı (4.61 saniye), $\text{diff\_perm}_i$ ise şans eseri simülasyonlardaki farkları ifade eder.*

---

## ⚠️ 4. p-hacking (Veri Hırsızlığı / Manipülasyonu) Tuzağı

A/B testlerinde yapılan en büyük hatalardan biri "p-hacking" yani anlamlı bir sonuç bulana kadar veriyi ve metrikleri eğip bükmektir.

> [!WARNING]
> ### 3 Cümlelik Örnek Senaryo ile p-hacking Riski
> 1. Bir e-ticaret ekibi, yeni bir arayüz tasarımının başarısını ölçmek için dönüşüm oranı, sayfada kalma süresi, sepete ekleme oranı, buton tıklamaları ve hemen çıkma oranı gibi 20 farklı metriği aynı anda test etmiştir.
> 2. Bu 20 metrikten sadece "sepete ekleme oranı" tamamen şans eseri $p < 0.05$ (istatistiksel olarak anlamlı) çıktığı için ekip diğer tüm metrikleri gizleyip sadece bu metriği raporlamış ve "yeni tasarımımız harika çalışıyor" sonucuna varmıştır.
> 3. Ancak bu durum, aslında hiçbir gerçek etki olmamasına rağmen sadece çok fazla zar atılarak rastgele bir tane düşeş bulma tuzağıdır ve ürün tüm kullanıcılara açıldığında hiçbir ciro artışı getirmeyerek hayal kırıklığıyla sonuçlanacaktır.

---

## 🛠️ 5. Nasıl Çalıştırılır?

Analiz kodunu çalıştırmak ve yukarıdaki özet tabloyu ile p-değerini kendi gözlerinizle görmek için şu adımları izleyebilirsiniz:

1. Gerekli kütüphaneleri yükleyin (henüz yüklü değilse):
   ```bash
   pip install pandas numpy
   ```
2. Analiz kodunu çalıştırın:
   ```bash
   python ab_analiz.py
   ```
   *Kod, tekrarlanabilirlik için kilitlenmiş bir seed (`np.random.seed(42)`) kullandığından, her çalıştırdığınızda tam olarak aynı istatistikleri ve $p = 0.0055$ değerini verecektir.*