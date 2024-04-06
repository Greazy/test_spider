# Yelp Spider

Business spider for Yelp

## Installation

```bash
pip install -r requirements.txt
```

## Usage

If you want to change category or location change this fields in main.py:

```python
category_name = 'Movers'
location = 'San Francisco'
```

Inside spider/spiders

```bash
scrapy runspider main.py
```

## Result

Result will be saved in items.json
