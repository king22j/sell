import requests

# Aranacak eşyaların Steam'deki tam isimleri
ITEMS_TO_CHECK = [
    "AK-47 | Redline (Field-Tested)",
    "AWP | Asiimov (Field-Tested)"
]

def get_csfloat_price(item_name):
    url = f"https://csfloat.com/api/v1/listings?market_hash_name={item_name}&limit=1"
    try:
        response = requests.get(url)
        data = response.json()
        if data and len(data) > 0:
            # CSFloat fiyatları cent cinsinden verir, dolara çeviriyoruz
            price = data[0]['price'] / 100 
            return price
    except Exception as e:
        print(f"CSFloat hatası ({item_name}): {e}")
    return None

def get_skinport_price(item_name):
    url = f"https://api.skinport.com/v1/items?market_hash_name={item_name}"
    try:
        response = requests.get(url)
        data = response.json()
        if data and len(data) > 0:
            return data[0]['min_price']
    except Exception as e:
        print(f"Skinport hatası ({item_name}): {e}")
    return None

def main():
    print("--- Envanter Fiyat Karşılaştırması ---\n")
    for item in ITEMS_TO_CHECK:
        print(f"Eşya: {item}")
        
        csfloat_price = get_csfloat_price(item)
        skinport_price = get_skinport_price(item)
        
        if csfloat_price:
            print(f"CSFloat En Düşük: ${csfloat_price:.2f}")
        else:
            print("CSFloat: Bulunamadı")
            
        if skinport_price:
            print(f"Skinport En Düşük: ${skinport_price:.2f}")
        else:
            print("Skinport: Bulunamadı")
            
        print("-" * 30)

if __name__ == "__main__":
    main()
