import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# 可重現性:固定亂數種子,任何人 clone 下來重跑都會拿到相同資料集
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# 輸出到 repo 根目錄下的 data/,不受執行位置影響(此腳本位於 src/)
output_dir = Path(__file__).resolve().parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. 真實基礎資料 (參照政府 Open Data 苗栗縣人口與長照推估結構)
# ==========================================
# 依據政府開放資料之鄉鎮失能人口比例，設定各區域的生成權重 (加總為 1.0)
# 頭份、苗栗、竹南等大城鎮權重高；獅潭、西湖等偏鄉人口少、權重低
MIAOLI_OPEN_DATA_WEIGHTS = {
    "頭份市": 0.18, "苗栗市": 0.16, "竹南鎮": 0.14, "苑裡鎮": 0.08, 
    "後龍鎮": 0.06, "通霄鎮": 0.06, "公館鄉": 0.05, "銅鑼鄉": 0.04, 
    "大湖鄉": 0.04, 
    "三義鄉": 0.03, "造橋鄉": 0.03, "頭屋鄉": 0.03, "卓蘭鎮": 0.03, 
    "南庄鄉": 0.02, "西湖鄉": 0.02, "三灣鄉": 0.01, "獅潭鄉": 0.01, "泰安鄉": 0.01
}

districts = list(MIAOLI_OPEN_DATA_WEIGHTS.keys())
weights = list(MIAOLI_OPEN_DATA_WEIGHTS.values())

# 長照 2.0 照顧組合代碼 (BA碼) 及其基本點數 (衛福部支付基準)
BA_CODES = {
    "BA01": {"name": "基本身體清潔", "points": 260, "unit": "次"},
    "BA02": {"name": "基本日常照顧", "points": 195, "unit": "30分鐘"},
    "BA07": {"name": "協助沐浴及洗頭", "points": 325, "unit": "次"},
    "BA10": {"name": "翻身拍背", "points": 155, "unit": "次"},
    "BA14": {"name": "陪同就醫", "points": 685, "unit": "1.5小時"},
    "BA15": {"name": "家務協助", "points": 195, "unit": "30分鐘"},
    "BA16": {"name": "代購或代領或代送服務", "points": 130, "unit": "次"}
}

# 次數型服務無法直接由 unit 推分鐘，保留每次服務的預設工時
BA_EVENT_DEFAULT_MIN = {
    "BA01": 30,
    "BA07": 50,
    "BA10": 20,
    "BA16": 20
}

def get_base_minutes(code):
    unit = BA_CODES[code]["unit"]
    if unit.endswith("分鐘"):
        return int(float(unit.replace("分鐘", "")))
    if unit.endswith("小時"):
        return int(float(unit.replace("小時", "")) * 60)
    if unit == "次":
        return BA_EVENT_DEFAULT_MIN.get(code, 30)
    raise ValueError(f"無法解析的 unit: {unit} (code={code})")

# 1. 生成居服員主檔 (caregivers)
num_caregivers = 20
caregivers = []
for i in range(1, num_caregivers + 1):
    caregivers.append({
        "caregiver_id": f"CG{i:03d}",
        "name": f"居服員_{i}",
        "experience_years": random.choice([1, 2, 3, 5, 8, 10]),
        # 居服員的駐點區域也依據人口稠密度（Open Data權重）進行分配
        "primary_region": random.choices(districts, weights=weights, k=1)[0],
        "cost_level": random.choice(["Senior", "Junior", "Mid"])
    })
df_cg = pd.DataFrame(caregivers)

# 2. 生成個案主檔 (clients) - 依據衛福部 CMS 失能等級
num_clients = 60
clients = []
for i in range(1, num_clients + 1):
    cms = random.randint(2, 8) # 長照主要服務 2-8 級
    # 關鍵：利用 Open Data 權重決定個案落點，符合真實長照人口地理分佈
    assigned_district = random.choices(districts, weights=weights, k=1)[0]
    
    clients.append({
        "client_id": f"CL{i:03d}",
        "care_level_cms": cms,
        "complexity_weight": round(1.0 + (cms - 2) * 0.15, 2), # CMS 越重，權重越高
        "district": assigned_district,
        "location_lat": round(24.5 + random.uniform(-0.10, 0.10), 4),
        "location_lng": round(120.8 + random.uniform(-0.10, 0.10), 4)
    })
df_cl = pd.DataFrame(clients)

# 3. 生成服務日誌 (service_logs) - 結合真實地理交通與支付核銷邏輯
logs = []
start_date = datetime(2026, 8, 1)

for day in range(14):
    current_date = start_date + timedelta(days=day)
    for cg in caregivers:
        daily_clients = random.sample(clients, random.randint(3, 5))
        for cl in daily_clients:
            # 實務邏輯：若個案在偏遠原鄉（泰安、獅潭、南庄），交通時間權重拉高
            if cl["district"] in ["泰安鄉", "獅潭鄉", "南庄鄉"]:
                travel_time = random.randint(30, 50)
            else:
                travel_time = random.randint(10, 25)
            
            # 抽選 1~3 個長照 2.0 照顧組合代碼 (BA碼)
            sampled_ba_codes = random.sample(list(BA_CODES.keys()), random.randint(1, 3))
            total_base_min = sum([get_base_minutes(code) for code in sampled_ba_codes])
            total_points = sum([BA_CODES[code]["points"] for code in sampled_ba_codes])
            
            # 實際服務工時模擬
            actual_hours = round((total_base_min + random.randint(-5, 15)) / 60, 1)
            if actual_hours < 0.5: actual_hours = 0.5
            
            # 計算政府核銷點數 (加計個案CMS失能加權)
            weighted_points = round(total_points * cl["complexity_weight"])

            logs.append({
                "caregiver_id": cg["caregiver_id"],
                "client_id": cl["client_id"],
                "service_date": current_date.strftime("%Y-%m-%d"),
                "travel_time_min": travel_time,
                "actual_service_hours": actual_hours,
                "care_types_completed": ",".join(sampled_ba_codes),
                "service_base_points": total_points,
                "final_weighted_points": weighted_points
            })

df_logs = pd.DataFrame(logs)

# 匯出 CSV
caregivers_path = output_dir / "caregivers.csv"
clients_path = output_dir / "clients.csv"
service_logs_path = output_dir / "service_logs.csv"

def save_csv_with_fallback(df, target_path):
    try:
        df.to_csv(target_path, index=False, encoding="utf-8-sig")
        return target_path
    except PermissionError:
        # 檔案被占用時，改存為時間戳版本，避免整體流程中斷
        fallback_path = target_path.with_stem(f"{target_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        df.to_csv(fallback_path, index=False, encoding="utf-8-sig")
        return fallback_path

caregivers_path = save_csv_with_fallback(df_cg, caregivers_path)
clients_path = save_csv_with_fallback(df_cl, clients_path)
service_logs_path = save_csv_with_fallback(df_logs, service_logs_path)

print("長照 2.0 擬真合成資料集(含苗栗 Open Data 權重分佈)生成完畢")
print(f"caregivers.csv 路徑: {caregivers_path}")
print(f"clients.csv 路徑: {clients_path}")
print(f"service_logs.csv 路徑: {service_logs_path}")
print(f"caregivers 筆數: {len(df_cg)}")
print(f"clients 筆數: {len(df_cl)}")
print(f"service_logs 筆數: {len(df_logs)}")


