from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 📊 БАЗА ДАННЫХ ЦЕН (базовая стоимость для 2024-2025 года)
BASE_PRICES = {
    # TOYOTA
    'toyota': {
        'camry': 3500000,
        'corolla': 2500000,
        'rav4': 4000000,
        'land cruiser': 9500000,
        'prado': 8000000,
        'highlander': 6000000,
        'avalon': 4500000,
        'yaris': 1800000,
        'c-hr': 3200000,
        'supra': 7500000
    },
    # BMW
    'bmw': {
        '3 series': 4000000,
        '5 series': 6000000,
        '7 series': 10000000,
        'x3': 5000000,
        'x5': 8000000,
        'x7': 11000000,
        'm3': 11000000,
        'm5': 14000000,
        'i4': 6500000,
        'ix': 10000000
    },
    # MERCEDES
    'mercedes': {
        'c-class': 5000000,
        'e-class': 7000000,
        's-class': 13000000,
        'gla': 4500000,
        'glc': 6000000,
        'gle': 9000000,
        'gls': 12000000,
        'a-class': 3500000,
        'cla': 4500000,
        'amg gt': 16000000
    },
    # AUDI
    'audi': {
        'a3': 3500000,
        'a4': 4500000,
        'a6': 6000000,
        'a8': 10000000,
        'q3': 4000000,
        'q5': 5500000,
        'q7': 8500000,
        'q8': 10000000,
        'e-tron': 9000000,
        'tt': 5500000
    },
    # LEXUS
    'lexus': {
        'es': 5000000,
        'rx': 7000000,
        'nx': 5500000,
        'gx': 8500000,
        'lx': 14000000,
        'is': 4500000,
        'ls': 11000000,
        'ux': 4000000,
        'rc': 6500000,
        'lc': 12000000
    },
    # KIA
    'kia': {
        'optima': 2800000,
        'sportage': 3500000,
        'sorento': 4200000,
        'rio': 1600000,
        'ceed': 2200000,
        'seltos': 2800000,
        'k5': 3200000,
        'mohave': 5000000,
        'picanto': 1300000,
        'stinger': 4500000
    },
    # HYUNDAI
    'hyundai': {
        'solaris': 1400000,
        'tucson': 3200000,
        'santa fe': 4000000,
        'creta': 2500000,
        'elantra': 2400000,
        'sonata': 3200000,
        'palisade': 5500000,
        'venue': 2000000,
        'kona': 2800000,
        'genesis': 6000000
    },
    # VOLKSWAGEN
    'volkswagen': {
        'golf': 3000000,
        'passat': 3500000,
        'tiguan': 3800000,
        'touareg': 6500000,
        'polo': 1800000,
        'jetta': 2500000,
        'atlas': 4500000,
        'arteon': 4500000,
        'id.4': 5000000,
        'taos': 3000000
    },
    # NISSAN
    'nissan': {
        'altima': 3000000,
        'sentra': 2200000,
        'rogue': 3500000,
        'pathfinder': 4500000,
        'murano': 3800000,
        'x-trail': 3200000,
        'qashqai': 2800000,
        'patrol': 6500000,
        'gt-r': 12000000,
        'leaf': 3500000
    },
    # FORD
    'ford': {
        'focus': 2500000,
        'fusion': 2800000,
        'escape': 3200000,
        'explorer': 4500000,
        'f-150': 5500000,
        'mustang': 5000000,
        'edge': 3800000,
        'ranger': 4000000,
        'bronco': 5500000,
        'ecosport': 2200000
    },
    # MAZDA
    'mazda': {
        'mazda3': 2800000,
        'mazda6': 3200000,
        'cx-3': 2500000,
        'cx-5': 3500000,
        'cx-9': 4500000,
        'mx-5': 4000000,
        'cx-30': 3000000,
        'cx-50': 3800000,
        'cx-60': 4200000,
        'cx-90': 5000000
    },
    # SUBARU
    'subaru': {
        'impreza': 2800000,
        'legacy': 3200000,
        'outback': 3800000,
        'forester': 3500000,
        'xv': 3000000,
        'wrx': 4500000,
        'ascent': 4500000,
        'crosstrek': 3200000,
        'brz': 4000000,
        'solterra': 5000000
    },
    # HONDA
    'honda': {
        'civic': 3000000,
        'accord': 3500000,
        'cr-v': 4000000,
        'pilot': 4500000,
        'hr-v': 3200000,
        'odyssey': 4500000,
        'fit': 2200000,
        'ridgeline': 4500000,
        'passport': 4200000,
        'insight': 3500000
    },
    # MITSUBISHI
    'mitsubishi': {
        'outlander': 3200000,
        'pajero': 4500000,
        'lancer': 2200000,
        'asx': 2500000,
        'eclipse cross': 3000000,
        'mirage': 1500000,
        'montero': 4500000,
        'galant': 2000000,
        'colt': 1800000,
        'attrage': 1600000
    },
    # CHEVROLET
    'chevrolet': {
        'cruze': 2200000,
        'malibu': 2800000,
        'equinox': 3200000,
        'traverse': 4000000,
        'tahoe': 7000000,
        'suburban': 7500000,
        'camaro': 5000000,
        'corvette': 9000000,
        'silverado': 6000000,
        'blazer': 4000000
    },
    # SKODA
    'skoda': {
        'octavia': 3000000,
        'superb': 3800000,
        'kodiaq': 4200000,
        'karoq': 3200000,
        'fabia': 2000000,
        'scala': 2500000,
        'kamiq': 2800000,
        'enyaq': 5000000,
        'rapid': 2200000,
        'yeti': 2800000
    },
    # VOLVO
    'volvo': {
        's60': 4500000,
        's90': 6000000,
        'v60': 4500000,
        'v90': 6500000,
        'xc40': 4500000,
        'xc60': 6000000,
        'xc90': 8000000,
        'c40': 6000000,
        'ex30': 5000000,
        'ex90': 9000000
    },
    # PORSCHE
    'porsche': {
        '911': 18000000,
        'cayenne': 12000000,
        'macan': 8000000,
        'panamera': 14000000,
        'taycan': 13000000,
        '718 boxster': 9000000,
        '718 cayman': 8500000,
        'cayenne coupe': 13000000
    },
    # JEEP
    'jeep': {
        'wrangler': 5500000,
        'grand cherokee': 6000000,
        'cherokee': 4000000,
        'compass': 3500000,
        'renegade': 3000000,
        'gladiator': 5500000,
        'wagoneer': 8000000,
        'grand wagoneer': 10000000
    },
    # LAND ROVER
    'landrover': {
        'range rover': 14000000,
        'range rover sport': 12000000,
        'range rover evoque': 6000000,
        'discovery': 8000000,
        'discovery sport': 6000000,
        'defender': 10000000
    }
}

def calculate_price(brand, model, year, mileage, condition):
    """
    Рассчитывает цену автомобиля на основе:
    - Базовой цены модели
    - Года выпуска (амортизация)
    - Пробега
    - Состояния
    """
    
    brand_lower = brand.lower()
    model_lower = model.lower()
    
    # Получаем базовую цену
    base_price = None
    
    if brand_lower in BASE_PRICES:
        brand_models = BASE_PRICES[brand_lower]
        
        # Точное совпадение
        if model_lower in brand_models:
            base_price = brand_models[model_lower]
        else:
            # Ищем частичное совпадение
            for m_name, m_price in brand_models.items():
                if m_name in model_lower or model_lower in m_name:
                    base_price = m_price
                    break
    
    # Если не нашли - используем среднюю цену 3 млн
    if base_price is None:
        base_price = 3000000
    
    print(f"\n{'='*60}")
    print(f"🚗 {brand} {model} ({year}г.)")
    print(f"📊 Базовая цена: {base_price:,} ₽")
    
    # 🔧 КОРРЕКТИРОВКА ПО ГОДУ (амортизация)
    current_year = 2026
    age = current_year - int(year)
    if age < 0:
        age = 0
    
    # Премиум авто медленнее дешевеют
    if base_price > 8000000:
        depreciation_rate = 0.94  # 6% в год
    elif base_price > 5000000:
        depreciation_rate = 0.92  # 8% в год
    else:
        depreciation_rate = 0.90  # 10% в год
    
    price_after_year = base_price * (depreciation_rate ** age)
    print(f"📅 После учета возраста ({age} лет): {price_after_year:,.0f} ₽")
    
    # 🔧 КОРРЕКТИРОВКА ПО ПРОБЕГУ
    mileage = int(mileage)
    
    if mileage > 200000:
        mileage_factor = 0.70  # -30%
    elif mileage > 150000:
        mileage_factor = 0.78  # -22%
    elif mileage > 100000:
        mileage_factor = 0.85  # -15%
    elif mileage > 75000:
        mileage_factor = 0.92  # -8%
    elif mileage > 50000:
        mileage_factor = 0.96  # -4%
    elif mileage > 25000:
        mileage_factor = 0.99  # -1%
    else:
        mileage_factor = 1.0   # 0%
    
    price_after_mileage = price_after_year * mileage_factor
    print(f"🛣️ После учета пробега ({mileage:,} км): {price_after_mileage:,.0f} ₽")
    
    # 🔧 КОРРЕКТИРОВКА ПО СОСТОЯНИЮ
    condition_factors = {
        'excellent': 1.15,  # +15%
        'good': 1.0,        # 0%
        'fair': 0.82,       # -18%
        'damaged': 0.60     # -40%
    }
    
    condition_factor = condition_factors.get(condition.lower(), 1.0)
    final_price = price_after_mileage * condition_factor
    
    print(f"⚙️ Состояние: {condition} (коэффициент {condition_factor})")
    print(f"💰 ИТОГОВАЯ ЦЕНА: {final_price:,.0f} ₽")
    print(f"{'='*60}\n")
    
    return int(final_price)


@app.route('/api/get-price', methods=['POST'])
def get_price():
    try:
        data = request.json
        print(f"\n📥 Получен запрос: {data}")
        
        brand = data.get('brand', '')
        model = data.get('model', '')
        year = data.get('year', 2020)
        mileage = data.get('mileage', 0)
        condition = data.get('condition', 'good')
        
        # Рассчитываем цену
        price = calculate_price(brand, model, year, mileage, condition)
        
        return jsonify({
            'success': True,
            'price': price,
            'source': 'AutoPriceAI Database'
        })
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AutoPriceAI Server запущен!")
    print("📡 Адрес: http://localhost:5000")
    print("💾 Режим: Локальная база данных (200+ моделей)")
    print("="*60 + "\n")
    app.run(debug=True)