import folium
import requests
import csv
import time
from pathlib import Path

IP_FILE = "ips.txt"
OUTPUT_CSV = "mapped_ips.csv"
OUTPUT_MAP = "ip_map.html"

def load_ips(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def save_csv_row(ip, city, region, country, loc):
    with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ip, city, region, country, loc])

def init_csv():
    if not Path(OUTPUT_CSV).exists():
        with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "City", "Region", "Country", "Location"])

def map_ips(ip_list):
    m = folium.Map(location=[0, 0], zoom_start=2)
    for ip in ip_list:
        try:
            r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
            r.raise_for_status()
            data = r.json()
            loc = data.get("loc", "")
            city = data.get("city", "")
            region = data.get("region", "")
            country = data.get("country", "")
            print(f"{ip}: {city}, {region}, {country} ({loc})")

            save_csv_row(ip, city, region, country, loc)

            if loc:
                lat, lon = map(float, loc.split(","))
                folium.Marker(location=[lat, lon], popup=f"{ip}\n{city}, {region}, {country}").add_to(m)

            m.save(OUTPUT_MAP)
            time.sleep(1)  # Be polite and avoid rate limits

        except Exception as e:
            print(f"Error for {ip}: {e}")
            break  # Stop processing on failure

    m.save(OUTPUT_MAP)
    print(f"Map saved to {OUTPUT_MAP}")

def main():
    ip_list = load_ips(IP_FILE)
    init_csv()
    map_ips(ip_list)

if __name__ == "__main__":
    main()

