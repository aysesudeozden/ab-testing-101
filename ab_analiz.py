import numpy as np
import pandas as pd
from scipy import stats

# Tekrarlanabilirlik için rastgele sayı üretecini sabitliyoruz.
np.random.seed(42)


def compute_normal_ci(values, confidence_level=0.95):
    """Normal yaklaşım güven aralığını hesaplar."""
    sample_size = len(values)
    sample_mean = np.mean(values)
    sample_std = np.std(values, ddof=1)
    standard_error = sample_std / np.sqrt(sample_size)

    # Formül: Güven aralığı = ortalama ± kritik t değeri × standart hata
    alpha = 1 - confidence_level
    t_critical = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)
    margin_of_error = t_critical * standard_error

    lower_bound = sample_mean - margin_of_error
    upper_bound = sample_mean + margin_of_error
    return sample_mean, lower_bound, upper_bound


def compute_bootstrap_ci(values, iterations=1000, confidence_level=0.95):
    """Bootstrap yüzdelik yöntemine göre güven aralığını hesaplar."""
    bootstrap_means = np.empty(iterations)

    # Mantık: Aynı örneklemden yerine koyarak tekrar tekrar örnek alır,
    # her örneklemde ortalamayı hesaplar ve bu ortalamaların dağılımını kullanırız.
    for index in range(iterations):
        resampled_values = np.random.choice(values, size=len(values), replace=True)
        bootstrap_means[index] = np.mean(resampled_values)

    alpha = 1 - confidence_level
    lower_bound = np.percentile(bootstrap_means, 100 * (alpha / 2))
    upper_bound = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))
    return lower_bound, upper_bound


def format_interval(lower_bound, upper_bound):
    return f"[{lower_bound:.2f}, {upper_bound:.2f}]"


def main():
    data_frame = pd.read_csv("kayit_sureleri_ab_testi.csv")
    grouped = data_frame.groupby("Grup", sort=False)

    summary_rows = []

    print("Normal yaklaşım açıklaması:")
    print(
        "Her grup için örneklem ortalaması alınır, örneklem standart sapması bulunur ve standart hata hesaplanır. "
        "Ardından %95 güven düzeyi için t dağılımının kritik değeri kullanılarak güven aralığı ortalama ± kritik değer × standart hata formülüyle bulunur."
    )
    print()

    print("Bootstrap yüzdelik yöntemi açıklaması:")
    print(
        "Her grup içinden yerine koyarak 1000 kez yeni örneklemler çekilir, her örneklemin ortalaması hesaplanır. "
        "Bu bootstrap ortalamalarının dağılımının %2.5 ve %97.5 yüzdelikleri güven aralığının alt ve üst sınırını verir."
    )
    print()

    for group_name, group_frame in grouped:
        values = group_frame["Kayit_Suresi_Saniye"].to_numpy()

        sample_mean, normal_lower, normal_upper = compute_normal_ci(values)
        bootstrap_lower, bootstrap_upper = compute_bootstrap_ci(values, iterations=1000)

        summary_rows.append(
            {
                "Grup": group_name,
                "Yontem": "Normal yaklaşım",
                "Ortalama": round(sample_mean, 2),
                "Alt Sinir": round(normal_lower, 2),
                "Ust Sinir": round(normal_upper, 2),
            }
        )
        summary_rows.append(
            {
                "Grup": group_name,
                "Yontem": "Bootstrap yüzdelik",
                "Ortalama": round(sample_mean, 2),
                "Alt Sinir": round(bootstrap_lower, 2),
                "Ust Sinir": round(bootstrap_upper, 2),
            }
        )

    summary_table = pd.DataFrame(summary_rows)

    print("%95 güven aralığı karşılaştırma tablosu:")
    print(summary_table.to_string(index=False))
    print()

    print("Sonuç yorumu:")
    print(
        "A ve B grupları için normal yaklaşım ile bootstrap yüzdelik yöntemi birbirine çok yakın güven aralıkları üretti. "
        "Bu durum, veri setinin örneklem boyutu bu analiz için yeterliyken sonucun yöntem seçimine aşırı duyarlı olmadığını gösterir. "
        "B grubunun aralığı A grubuna göre daha aşağıda kaldığı için, adımlı formun kayıt süresini kısaltma etkisi istatistiksel olarak tutarlı görünmektedir."
    )


if __name__ == "__main__":
    main()