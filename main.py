"""
Google Analytics Manipulative Mini Script

Contact for Premium Script.

Author;
Github: buraksocial
Telegram: @merhabaworld
Instagram: bur4ksocial
"""
import requests
import json
import time
import random
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 10 

PROXY_FILE = "proxies.txt"

HIT_INTERVAL_MSEC = 500

SIMULATED_DWELL_TIME_MIN_SEC = 8
SIMULATED_DWELL_TIME_MAX_SEC = 15 

USER_AGENT_TYPES = ['desktop', 'mobile']

ADVANCED_FINGERPRINT_SPOOFING = True

DESKTOP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edge/117.0.2045.60",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
]

COMMON_LANGUAGES = ["en-US", "tr-TR", "en-GB", "de-DE", "fr-FR", "es-ES"]
DESKTOP_RESOLUTIONS = ["1920x1080", "1536x864", "1440x900", "1366x768", "2560x1440"]
MOBILE_RESOLUTIONS = ["390x844", "414x896", "393x851", "360x780", "428x926"]

def get_random_fingerprint():
    """
    Ayarlara göre rastgele bir Cihaz Profili (Parmak İzi) oluşturur.
    """
    device_type = random.choice(USER_AGENT_TYPES)
    fingerprint = {}

    if device_type == 'desktop':
        fingerprint['user_agent'] = random.choice(DESKTOP_USER_AGENTS)
        fingerprint['screen_resolution'] = random.choice(DESKTOP_RESOLUTIONS)
    else: 
        fingerprint['user_agent'] = random.choice(MOBILE_USER_AGENTS)
        fingerprint['screen_resolution'] = random.choice(MOBILE_RESOLUTIONS)

    if ADVANCED_FINGERPRINT_SPOOFING:
        fingerprint['language'] = random.choice(COMMON_LANGUAGES)
    else:
        fingerprint['language'] = None 

    return fingerprint

class GA4Visitor:
    """
    Proxy, Dwell Time ve Fingerprint desteği eklendi.
    """

    API_SECRET = "xx6N5G_fQoivgzpbbPkyfQ" 
    MEASUREMENT_ID = "G-C0EXMKMVJF" 

    BASE_URL = "https://www.google-analytics.com/mp/collect"

    def __init__(self, proxy_string=None, fingerprint=None):
        self.api_url = f"{self.BASE_URL}?measurement_id={self.MEASUREMENT_ID}&api_secret={self.API_SECRET}"

        self.client_id = str(uuid.uuid4())
        self.session_id = str(random.randint(1000000000, 9999999999))

        fingerprint = fingerprint or get_random_fingerprint() 

        self.headers = {
            'User-Agent': fingerprint['user_agent']
        }
        self.language = fingerprint.get('language')
        self.screen_resolution = fingerprint.get('screen_resolution')

        self.proxy_string = proxy_string
        self.proxy_dict = None
        if self.proxy_string:
            self.proxy_dict = {
                "http": self.proxy_string,
                "httpsS": self.proxy_string
            }

        self.current_page_location = None
        self.current_page_referrer = None

        self.log_prefix = f"[{self.proxy_string or 'LOKAL IP'} | {self.client_id[-6:]}]"

        print(f"{self.log_prefix} Yeni ziyaretçi oluşturuldu (Session: {self.session_id}).")
        print(f"{self.log_prefix}   -> UA: {self.headers['User-Agent'][:40]}...")
        print(f"{self.log_prefix}   -> SR: {self.screen_resolution}, Dil: {self.language or 'Belirtilmedi'}")

    def _send_event(self, event_name, params):
        """
        GA4'e bir olay göndermek için kullanılan ana (özel) metot.
        Dwell Time ve Fingerprint verileri eklendi.
        """

        if 'engagement_time_msec' not in params:
            if event_name == 'page_view':
                dwell_msec = str(random.randint(SIMULATED_DWELL_TIME_MIN_SEC * 1000, SIMULATED_DWELL_TIME_MAX_SEC * 1000))
            else:
                dwell_msec = str(random.randint(100, 1500)) 
            params['engagement_time_msec'] = dwell_msec

        if self.screen_resolution:
            params['sr'] = self.screen_resolution

        if self.language: 
            params['ul'] = self.language

        if 'session_id' not in params:
            params['session_id'] = self.session_id

        payload = {
            'client_id': self.client_id,
            'events': [{
                'name': event_name,
                'params': params
            }]
        }

        try:
            response = requests.post(
                self.api_url, 
                json=payload, 
                headers=self.headers,
                proxies=self.proxy_dict,
                timeout=15
            )

            if response.status_code == 204:
                print(f"{self.log_prefix} -> Başarılı: '{event_name}' (Süre: {params['engagement_time_msec']}ms) gönderildi.")
            else:
                print(f"{self.log_prefix} -> Hata: {response.status_code} - {response.text}")

        except requests.exceptions.ProxyError:
            print(f"{self.log_prefix} -> HATA: Proxy'ye bağlanılamadı.")
        except requests.exceptions.ConnectTimeout:
            print(f"{self.log_prefix} -> HATA: Proxy'ye bağlanırken zaman aşımı.")
        except requests.exceptions.ReadTimeout:
            print(f"{self.log_prefix} -> HATA: Proxy'den yanıt beklenirken zaman aşımı.")
        except requests.exceptions.RequestException as e:
            print(f"{self.log_prefix} -> HATA: Genel İstek Hatası - {e}")

    def _simulate_wait(self, min_sec=2, max_sec=5):
        wait_time = random.uniform(min_sec, max_sec)
        print(f"{self.log_prefix} ... {wait_time:.1f} saniye bekleniyor ...")
        time.sleep(wait_time)

    def event_page_view(self, page_location, page_referrer, page_title, organic_search_term=None):
        print(f"{self.log_prefix} OLAY: Sayfa Görüntüleme (page_view) - {page_location}")
        self.current_page_location = page_location
        self.current_page_referrer = page_referrer
        params = {'page_location': page_location, 'page_referrer': page_referrer, 'page_title': page_title}
        if organic_search_term:
            params.update({'source': 'google', 'medium': 'organic', 'term': organic_search_term})
        self._send_event('page_view', params)

    def event_scroll(self, percent=90):
        print(f"{self.log_prefix} OLAY: Kaydırma (scroll)")
        params = {'page_location': self.current_page_location, 'percent_scrolled': str(percent)}
        self._send_event('scroll', params)

    def event_site_search(self, search_term):
        print(f"{self.log_prefix} OLAY: Site İçi Arama (view_search_results) - '{search_term}'")
        params = {'page_location': self.current_page_location, 'search_term': search_term}
        self._send_event('view_search_results', params)

        self.event_page_view(
            page_location=f"https://www.yourdomain.com/search?q={search_term}",
            page_referrer=self.current_page_location,
            page_title=f"{search_term} Arama Sonuçları"
        )

    def event_outbound_click(self, link_url):
        print(f"{self.log_prefix} OLAY: Giden Tıklama (click) - {link_url}")
        params = {'page_location': self.current_page_location, 'link_url': link_url, 'outbound': 'true'}
        self._send_event('click', params)

    def run_full_journey(self):
        """
        Tam bir ziyaretçi yolculuğu senaryosu.
        """
        print(f"{self.log_prefix} === ZİYARETÇİ YOLCULUĞU BAŞLADI ===")

        self.event_page_view(
            page_location="https://www.yourdomain.com/",
            page_referrer="https://www.google.com/search?q=yoursite",
            page_title="yoursite Ana Sayfa",
            organic_search_term="yoursite"
        )
        self._simulate_wait(2, 4)

        self.event_scroll(percent=random.randint(70, 100))
        self._simulate_wait(3, 5)

        search_term = random.choice(["python", "seo", "analytics", "bot", "yoursite nedir"])
        self.event_site_search(search_term=search_term)
        self._simulate_wait(4, 6)

        self.event_outbound_click(link_url="https://www.github.com/yoursite")

        print(f"{self.log_prefix} === YOLCULUK TAMAMLANDI ===")

def load_proxies(filename):
    """proxies.txt dosyasından proxy listesini okur."""
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        print(f"HATA: '{filename}' dosyası bulunamadı.")
        return []
    except Exception as e:
        print(f"HATA: Proxy dosyası okunurken hata: {e}")
        return []

def run_visitor_task(proxy):
    """
    Bir thread (iş parçacığı) tarafından çalıştırılacak olan ana görev.
    Rastgele bir parmak izi oluşturur, ziyaretçiyi başlatır ve yolculuğu çalıştırır.
    """
    try:

        fingerprint = get_random_fingerprint()

        visitor = GA4Visitor(proxy_string=proxy, fingerprint=fingerprint)
        visitor.run_full_journey()
        return f"BAŞARILI: {proxy}"
    except Exception as e:
        return f"HATA: {proxy} - {e}"

if __name__ == "__main__":
    print(f"--- Hit Engine Başlatılıyor (Maksimum {MAX_WORKERS} thread) ---")
    print(f"--- Hit Aralığı: {HIT_INTERVAL_MSEC}ms ---")

    proxies = load_proxies(PROXY_FILE)
    hit_interval_sec = HIT_INTERVAL_MSEC / 1000.0 

    if not proxies:
        print("Hiç proxy bulunamadı veya dosya okunamadı. Çıkılıyor.")
        exit()

    print(f"Toplam {len(proxies)} adet proxy yüklendi.")
    print("Ziyaretçi görevleri oluşturuluyor...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = []

        for proxy in proxies:
            print(f"[ANA KONTROLCÜ] Görev oluşturuluyor: {proxy}")
            future = executor.submit(run_visitor_task, proxy)
            futures.append(future)

            if hit_interval_sec > 0:
                print(f"[ANA KONTROLCÜ] Sonraki görev için {hit_interval_sec:.2f} sn bekleniyor (Hit Interval)...")
                time.sleep(hit_interval_sec)

        print("[ANA KONTROLCÜ] Tüm görevler gönderildi. Tamamlanmaları bekleniyor...")
        for future in as_completed(futures):

            try:
                result = future.result()
                print(f"[ANA KONTROLCÜ] Görev sonucu: {result}")
            except Exception as e:
                print(f"[ANA KONTROLCÜ] Bir görevde istisna oluştu: {e}")

    print("--- Tüm Ziyaretçi Görevleri Tamamlandı ---")
