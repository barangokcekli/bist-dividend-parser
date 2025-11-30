# bist-divident-parser

English | [Türkçe](#türkçe)

---

## English

`bist-divident-parser` is a small Python microservice built with **FastAPI** that parses **dividend** and **capital increase** data for BIST (Borsa İstanbul) stocks from **[fintables.com](https://fintables.com)** and exposes it as a JSON API.

### Features

- Scrapes dividend and capital increase tables for a given BIST ticker (e.g. `EREGL`) from `fintables.com`
- Parses and normalizes Turkish-formatted numbers (`%`, `₺`, thousand separators, commas, etc.)
- Returns structured JSON responses using **Pydantic** models
- Simple in-memory caching layer to avoid hitting `fintables.com` on every request

### Running locally

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the API:

   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000
   ```

4. Open the interactive docs (Swagger UI):

   ```text
   http://127.0.0.1:8000/docs
   ```

### Example request

```bash
GET /api/EREGL
```

Example JSON structure (simplified):

```json
{
  "ticker": "EREGL",
  "dividends": [
    {
      "date": "02-07-2025",
      "yield_percent": 0.94,
      "gross_per_share": 0.25,
      "net_per_share": 0.2125,
      "total_dividend": 1750000000.0,
      "payout_ratio": 13.0
    }
  ],
  "capital_increases": [
    {
      "date": "27-11-2024",
      "post_capital": 960336000.0,
      "paid_in_percent": 321.2,
      "private_placement_percent": null,
      "bonus_internal_percent": null,
      "bonus_dividend_percent": null
    }
  ]
}
```

> **Note:** This project is for educational / personal use. Please respect the terms of use and robots.txt rules of [fintables.com](https://fintables.com) and any other data sources you use.

---

## Türkçe

`bist-divident-parser`, **FastAPI** ile yazılmış küçük bir Python mikro-servisidir.  
BIST (Borsa İstanbul) hisseleri için **temettü** ve **sermaye artırımı** verilerini **[fintables.com](https://fintables.com)** adresinden parse eder ve JSON formatında bir API olarak sunar.

### Özellikler

- Verilen BIST hisse kodu (örneğin `EREGL`) için `fintables.com` üzerindeki temettü ve sermaye artırımı tablolarını çeker
- Türkçe sayı formatlarını ( `%`, `₺`, binlik ayırıcı nokta, ondalık virgül vs.) normalize eder
- **Pydantic** modelleriyle tip güvenli ve düzenli JSON çıktı üretir
- `fintables.com`’a her istekte gitmemek için basit bir bellek içi cache (in-memory cache) kullanır

### Lokal çalıştırma

1. Sanal ortam oluştur ve aktifleştir (opsiyonel ama tavsiye edilir):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Bağımlılıkları yükle:

   ```bash
   pip install -r requirements.txt
   ```

3. API’yi başlat:

   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000
   ```

4. Swagger arayüzünü aç:

   ```text
   http://127.0.0.1:8000/docs
   ```

### Örnek istek

```bash
GET /api/EREGL
```

Basitleştirilmiş örnek JSON çıktısı:

```json
{
  "ticker": "EREGL",
  "dividends": [
    {
      "date": "02-07-2025",
      "yield_percent": 0.94,
      "gross_per_share": 0.25,
      "net_per_share": 0.2125,
      "total_dividend": 1750000000.0,
      "payout_ratio": 13.0
    }
  ],
  "capital_increases": [
    {
      "date": "27-11-2024",
      "post_capital": 960336000.0,
      "paid_in_percent": 321.2,
      "private_placement_percent": null,
      "bonus_internal_percent": null,
      "bonus_dividend_percent": null
    }
  ]
}
```

> **Not:** Bu proje eğitim ve kişisel kullanım amaçlıdır. Lütfen [fintables.com](https://fintables.com) ve kullandığınız diğer veri kaynaklarının kullanım koşullarına ve robots.txt kurallarına saygı gösterin.
