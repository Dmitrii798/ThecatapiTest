# cleanup.py
import requests

API_KEY = "live_ASeqC0q4fFuXwIzSij0GJgDYqQLl9YPAz1xfJAjHCbnrX0B1qLi7QDSYKvt2vfje"
url = "https://api.thecatapi.com/v1"
headers = {"x-api-key": API_KEY}

# 1. Получить все favourites
resp = requests.get(f"{url}/favourites", headers=headers)
print(f"Status: {resp.status_code}")
favourites = resp.json()
print(f"Всего favourites: {len(favourites)}")

# 2. Удалить все
for fav in favourites:
    del_resp = requests.delete(f"{url}/favourites/{fav['id']}", headers=headers)
    print(f"Удалён favourite {fav['id']}: {del_resp.status_code}")

# 3. Проверить, что пусто
resp = requests.get(f"{url}/favourites", headers=headers)
print(f"После очистки: {len(resp.json())} favourites")
