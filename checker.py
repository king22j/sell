import requests

# Kopyaladığın CSFloat API anahtarını buraya yapıştır (Tırnak işaretlerini silme!)
CSFLOAT_API_KEY = "TvSzCKhgjj-KzrPML-1JjIaZB6OlSDgv"

ITEMS_TO_CHECK = [
    "AK-47 | Redline (Field-Tested)",
    "AWP | Asiimov (Field-Tested)"
]

def get_skinport_prices():
    # Skinport tüm CS2 eşyalarını tek seferde çekmemizi ister, bu daha güvenlidir.
    url = "https://api.skinport.com/v1/items?app_id=730&currency=USD"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Eğer dönen veri bir liste ise (başarılıysa)
        if isinstance(data, list):
            prices = {}
            for item in data:
                prices[item['market_hash_name']] = item.get('min_price')
            return prices
        else:
            print(f"Skinport beklenmeyen bir hata verdi: {data}")
            return {}
            
    except Exception as e:
        print(f"Skinport veri çekme hatası: {e}")
        return {}

def get_csfloat_price(item_name):
    url = f"https://csfloat.com/api/v1/listings?market_hash_name={item_name}&limit=1"
    headers = {
        "Authorization": CSFLOAT_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Eğer gelen veri bir listeyse ve içi boş değilse fiyatı al
        if isinstance(data, list) and len(data) > 0:
            return data[0]['price'] / 100 
        # Eğer API bir hata mesajı döndürdüyse (örn: API anahtarı yanlışsa)
        elif isinstance(data, dict) and 'message' in data:
            print(f"CSFloat API Hatası ({item_name}): {data['message']}")
        else:
            print(f"CSFloat'ta satışta eşya bulunamadı: {item_name}")
            
    except Exception as e:
        print(f"CSFloat bağlantı hatası ({item_name}): {e}")
        
    return None

def main():
    print("--- Envanter Fiyat Karşılaştırması ---\n")
    
    print("Skinport fiyatları toplu olarak çekiliyor, lütfen bekleyin...")
    skinport_all_prices = get_skinport_prices()
    print("Skinport verileri alındı.\n")
    
    for item in ITEMS_TO_CHECK:
        print(f"Eşya: {item}")
        
        csfloat_price = get_csfloat_price(item)
        skinport_price = skinport_all_prices.get(item)
        
        if csfloat_price:
            print(f"CSFloat En Düşük: ${csfloat_price:.2f}")
        else:
            print("CSFloat: Bulunamadı (veya hata oluştu)")
            
        if skinport_price:
            print(f"Skinport En Düşük: ${skinport_price:.2f}")
        else:
            print("Skinport: Bulunamadı")
            
        print("-" * 30)

if __name__ == "__main__":
    main()
