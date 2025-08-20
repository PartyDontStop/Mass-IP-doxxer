import requests
import threading

threads_count = 10

def process_ip(line):
    line = line.strip()
    if not line:
        return
    ip_parts = line.split(".")
    if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
        return
    last_octet = int(ip_parts[3]) + 1
    if last_octet > 255:
        return
    ip_parts[3] = str(last_octet)
    new_ip = ".".join(ip_parts)
    informationAPI = "http://ip-api.com/json/" + new_ip
    response = requests.get(informationAPI)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "query" in data and "country" in data:
            with open("Data/output.txt", "a") as f_out:
                f_out.write(data["query"] + " | " + data["country"] + " | " + data["regionName"] + " | " + data["isp"] + "\n")
            print(f"Successfully processed {line} (200 OK)")

def process():
    with open("Data/input.txt", "r") as f:
        lines = f.readlines()

    threads = []
    for line in lines:
        t = threading.Thread(target=process_ip, args=(line,))
        threads.append(t)
        t.start()
        while threading.active_count() > threads_count:
            pass

    for t in threads:
        t.join()

process()
