Harika bir script, Burak. Oldukça gelişmiş özellikler eklemişsin.

İstediğin GitHub deposu (`https://github.com/buraksocial/google-analytics-manipulative/`) için hazırladığım detaylı `README.md` dosyası aşağıdadır.

-----

````markdown
# Google Analytics (GA4) Manipülasyon Aracı

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Bu proje, Google Analytics 4 (GA4) mülklerine **Gelişmiş Ölçüm Protokolü (Measurement Protocol)** üzerinden sahte, ancak gerçekçi görünen ziyaretçi trafiği göndermek için tasarlanmış gelişmiş bir Python betiğidir.

Araç, sadece basit `page_view` (sayfa görüntüleme) hitleri göndermek yerine, **çoklu-iş parçacığı (multi-threading)**, **proxy desteği** ve **gelişmiş cihaz parmak izi (fingerprinting)** kullanarak tam bir kullanıcı yolculuğunu (organik arama, sayfada gezinme, site içi arama, dış linke tıklama) simüle eder.

---

## 🚨 ÖNEMLİ ETİK UYARI VE YASAL SORUMLULUK REDDİ

Bu araç, **yalnızca eğitim, test ve araştırma amaçlı** geliştirilmiştir.

* **Test Amaçlı Kullanım:** Kendi GA4 mülkünüzün veri toplama kapasitesini, olay (event) yapılandırmasını veya sunucu yükünü test etmek için kullanabilirsiniz.
* **Kötüye Kullanım Uyarısı:** Bu betiği, başkalarının analiz verilerini bozmak, yanıltıcı raporlar oluşturmak veya izniniz olmayan web sitelerine sahte trafik göndermek amacıyla kullanmak **Google'ın Hizmet Şartları'nın açık bir ihlalidir** ve yasa dışıdır.
* **Sorumluluk:** Bu aracın kullanımından doğacak tüm yasal ve etik sorumluluk tamamen kullanıcıya aittir. Bu depoyu (repository) kullanarak bu şartları kabul etmiş sayılırsınız.

---

## 🌟 Temel Özellikler

* **Çoklu İş Parçacığı (Multi-Threading):** `ThreadPoolExecutor` kullanarak aynı anda birden fazla (`MAX_WORKERS` ile sınırlı) ziyaretçi oturumunu simüle eder.
* **Proxy Desteği:** `proxies.txt` dosyasından proxy listesi okur ve her ziyaretçi oturumunu farklı bir IP adresi üzerinden çalıştırır. Proxy hatalarını (timeout, connection error) yakalar.
* **Gelişmiş Parmak İzi (Fingerprinting):**
    * **Dinamik User-Agent:** `DESKTOP_USER_AGENTS` ve `MOBILE_USER_AGENTS` listelerinden rastgele olarak güncel ve geçerli tarayıcı kimlikleri seçer.
    * **Ekran Çözünürlüğü (`sr`):** Cihaz türüne (mobil/desktop) göre rastgele ve yaygın ekran çözünürlükleri atar.
    * **Tarayıcı Dili (`ul`):** `COMMON_LANGUAGES` listesinden rastgele bir dil atar.
* **Gerçekçi Kullanıcı Yolculuğu (`run_full_journey`):**
    1.  **Organik Ziyaret:** Ziyaretçiyi `google.com`'dan geliyormuş gibi (`organic_search_term` ile) ana sayfaya yönlendirir.
    2.  **Sayfada Kalma Süresi (Dwell Time):** `SIMULATED_DWELL_TIME...` ayarları arasında rastgele bir süre (milisaniye cinsinden `engagement_time_msec`) sayfada bekleterek simüle eder.
    3.  **Kaydırma (`scroll`):** Sayfanın %90'ına kadar kaydırma olayını tetikler.
    4.  **Site İçi Arama (`view_search_results`):** Önceden tanımlanmış bir listeden rastgele bir terim seçerek site içi arama yapar ve arama sonuçları sayfasını ziyaret eder.
    5.  **Giden Tıklama (`click`):** Senaryo sonunda dış bir bağlantıya (örneğin, bir sosyal medya profili) tıklar.
* **Kontrollü Gönderim Hızı:** `HIT_INTERVAL_MSEC` ayarı ile her bir yeni ziyaretçi görevinin (thread) başlaması arasında belirli bir gecikme ekleyerek ani yüklenmeleri önler.

---

## 🛠️ Kurulum ve Yapılandırma

### 1. Ön Gereksinimler
* Python 3.9 veya daha üzeri bir sürüm.
* `requests` kütüphanesi.

### 2. Kurulum
1.  Bu depoyu klonlayın:
    ```bash
    git clone [https://github.com/buraksocial/google-analytics-manipulative.git](https://github.com/buraksocial/google-analytics-manipulative.git)
    cd google-analytics-manipulative
    ```

2.  Gerekli Python kütüphanesini yükleyin:
    ```bash
    pip install requests
    ```

### 3. Yapılandırma

Betiği çalıştırmadan önce **iki** ana dosyayı yapılandırmanız gerekir:

#### A. `proxies.txt` Dosyası
Betiğin çalışacağı dizinde `proxies.txt` adında bir dosya oluşturun. İçerisine kullanmak istediğiniz proxy'leri her satıra bir adet gelecek şekilde ekleyin.

**Format:**
````

http://kullaniciadi:sifre@ip\_adresi:port
http://ip\_adresi:port
https://kullaniciadi:sifre@ip\_adresi:port

````

#### B. Ana Python Betiği (`.py`)
Betiğin en üst kısmındaki **Global Ayarlar** bölümünü düzenleyin:

* **GA4 Bilgileri:**
    * `API_SECRET`: GA4 Measurement Protocol API sırrınız.
        > *Bunu almak için: GA4 Yönetim > (Mülkünüz) > Veri Akışları > (Akışınızı Seçin) > Measurement Protocol API sırları > Yeni Oluştur*
    * `MEASUREMENT_ID`: `G-` ile başlayan Ölçüm Kimliğiniz.

* **Performans Ayarları:**
    * `MAX_WORKERS`: Aynı anda çalışacak maksimum iş parçacığı (thread) sayısı. Proxy sayınızdan fazla olmamalıdır.
    * `HIT_INTERVAL_MSEC`: Her yeni görevin başlaması arasındaki milisaniye cinsinden bekleme süresi (örneğin, 1000 = 1 saniye).

* **Simülasyon Ayarları:**
    * `SIMULATED_DWELL_TIME_MIN_SEC`: Bir ziyaretçinin bir sayfada kalacağı minimum saniye.
    * `SIMULATED_DWELL_TIME_MAX_SEC`: Bir ziyaretçinin bir sayfada kalacağı maksimum saniye.
    * `ADVANCED_FINGERPRINT_SPOOFING`: `True` yapılırsa dil ve çözünürlük verilerini de sahte olarak üretir.

---

## 🚀 Çalıştırma

Tüm yapılandırmaları tamamladıktan sonra, betiği terminal veya komut istemcisinden çalıştırabilirsiniz:

```bash
python main.py 
````

*(Eğer dosya adınız farklıysa `main.py` yerine kendi dosya adınızı yazın)*

Betiğiniz çalışmaya başlayacak, proxy'leri yükleyecek ve her bir proxy için sırayla (`HIT_INTERVAL_MSEC` aralığıyla) bir ziyaretçi görevi başlatacaktır. Her ziyaretçinin gerçekleştirdiği eylemleri konsolda anlık olarak görebilirsiniz.

-----

## ⚙️ Kodun Derinlemesine İncelemesi

### `get_random_fingerprint()`

Bu fonksiyon, her ziyaretçi için benzersiz bir cihaz profili oluşturur.

1.  Önce `USER_AGENT_TYPES` listesinden (`desktop` veya `mobile`) rastgele bir cihaz türü seçer.
2.  Seçilen türe göre ilgili `..._USER_AGENTS` ve `..._RESOLUTIONS` listelerinden bir User-Agent ve ekran çözünürlüğü seçer.
3.  `ADVANCED_FINGERPRINT_SPOOFING` aktifse, `COMMON_LANGUAGES` listesinden bir dil kodu ekler.

### `GA4Visitor` Sınıfı

Her bir iş parçacığı (thread) bu sınıftan bir nesne oluşturur.

  * `__init__`: Ziyaretçiyi oluşturur. Benzersiz bir `client_id` (cihazı temsil eder) ve `session_id` (ziyareti temsil eder) üretir. Proxy ve parmak izi bilgilerini (headers, language, sr) ayarlar.
  * `_send_event`: GA4'e veri gönderen çekirdek metottur.
      * Olay parametrelerine (`params`) otomatik olarak `engagement_time_msec`, `sr`, `ul`, ve `session_id` gibi parmak izi ve oturum verilerini ekler.
      * Veriyi `requests.post` ile GA4 Measurement Protocol API'sine (`self.api_url`) gönderir.
      * Proxy ve bağlantı hatalarını (Timeout, ProxyError) yakalayarak konsola log basar.
  * `event_...` Metotları: (`event_page_view`, `event_scroll` vb.)
      * GA4'ün standart olaylarını (`page_view`, `scroll`, `view_search_results`, `click`) tetiklemek için kullanılan yardımcılardır.
  * `run_full_journey`:
      * Bir ziyaretçinin baştan sona simülasyonunu yönetir.
      * Olaylar arasında `_simulate_wait` ile rastgele süreler bekleyerek gerçekçi bir gezinme davranışı sergiler.

### `if __name__ == "__main__":` Bloğu

  * Ana kontrolcüdür.
  * `load_proxies` ile proxy'leri belleğe alır.
  * `ThreadPoolExecutor`'ü `MAX_WORKERS` limitiyle başlatır.
  * Bir `for` döngüsü içinde her bir proxy için `executor.submit(run_visitor_task, proxy)` komutuyla yeni bir görev oluşturur.
  * `time.sleep(hit_interval_sec)` komutuyla görevler arasında `HIT_INTERVAL_MSEC` kadar bekler.
  * Tüm görevler bittiğinde `as_completed` ile sonuçları toplar ve programı sonlandırır.

<!-- end list -->

```
```
