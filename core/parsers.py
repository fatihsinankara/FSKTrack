import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArasKargoParser:
    def __init__(self, tracking_url):
        self.tracking_url = tracking_url

    def parse(self):
        try:
            logger.info(f"Fetching URL: {self.tracking_url}")
            response = requests.get(self.tracking_url)

            # Sayfanın başarılı şekilde yüklendiğini kontrol et
            if response.status_code != 200:
                return {
                    'status': 'Hata',
                    'message': f'Sayfa yüklenemedi, durum kodu: {response.status_code}',
                    'tracking_number': 'Bilinmiyor',
                    'movements': [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
                }
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Sayfada kritik bir öğe olup olmadığını kontrol et
            if not soup.find("span", {"id": "Son_Durum"}) and not soup.find("span", {"id": "labelShipmentCode"}):
                return {
                    'status': 'Hata',
                    'message': 'Sayfa beklendiği gibi yüklenmedi veya kargo verileri bulunamadı',
                    'tracking_number': 'Bilinmiyor',
                    'movements': [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
                }
            
            # Teslimat durumu ve takip numarasını alma
            status_element = soup.find("span", {"id": "Son_Durum"})
            tracking_number_element = soup.find("span", {"id": "labelShipmentCode"})
            status = status_element.get_text(strip=True) if status_element else "Durum bilgisi bulunamadı"
            tracking_number = tracking_number_element.get_text(strip=True) if tracking_number_element else "Takip numarası bulunamadı"
            
            # Hareketleri alma
            movements = []
            movement_table = soup.find("table", {"id": "transactionsDataGrid"})
            if movement_table:
                rows = movement_table.find_all("tr")[1:]  # İlk satır başlık
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        movements.append({
                            'tarih': cols[0].get_text(strip=True),
                            'il': cols[1].get_text(strip=True),
                            'birim': cols[2].get_text(strip=True),
                            'islem': cols[3].get_text(strip=True)
                        })
            else:
                movements = [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
            
            return {
                'status': status,
                'tracking_number': tracking_number,
                'movements': movements
            }

        except Exception as e:
            logger.error(f"Parsing error: {str(e)}")
            return {
                'error': str(e),
                'status': 'Hata oluştu',
                'tracking_number': 'Bilinmiyor',
                'movements': [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
            }

class YurticiKargoParser:
    def __init__(self, tracking_url):
        self.tracking_url = tracking_url

    def parse(self):
        try:
            logger.info(f"Fetching URL: {self.tracking_url}")
            response = requests.get(self.tracking_url)

            # Sayfanın başarılı şekilde yüklendiğini kontrol et
            if response.status_code != 200:
                return {
                    'status': 'Hata',
                    'message': f'Sayfa yüklenemedi, durum kodu: {response.status_code}',
                    'tracking_number': 'Bilinmiyor',
                    'movements': [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
                }
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Gönderi Bilgileri tablosundan gerekli verileri çek
            details = {}
            info_table = soup.find('table', class_='tableForm')
            if info_table:
                rows = info_table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) == 2:
                        label = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        details[label] = value

            return {
                'status': details.get("Gönderi Durumu", "Durum bilgisi bulunamadı"),
                'tracking_number': details.get("Gönderi Kodu", "Takip numarası bulunamadı"),
                'movements': [{'tarih': 'Veri yok', 'il': '', 'birim': '', 'islem': ''}]  # Hareketler bilgisi burada güncellenebilir
            }

        except Exception as e:
            logger.error(f"Parsing error: {str(e)}")
            return {
                'error': str(e),
                'status': 'Hata oluştu',
                'tracking_number': 'Bilinmiyor',
                'movements': [{'tarih': 'Veri bulunamadı', 'il': '', 'birim': '', 'islem': ''}]
            }