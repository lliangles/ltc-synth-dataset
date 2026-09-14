# 資料字典 / Data Dictionary

本文件說明三個資料表(`caregivers.csv`、`clients.csv`、`service_logs.csv`)的所有欄位定義與生成邏輯,供資料分析師 / 模型訓練使用。

---

## 一、居服員主檔 `caregivers.csv`

記錄提供長照服務的第一線人員(居服員)基本屬性,主要用於人力資源配置與成本計算。

| 欄位 | 型態 | 說明與生成邏輯 |
|---|---|---|
| `caregiver_id` | String | 居服員唯一識別碼,格式 `CG` + 三位數(例:`CG001`) |
| `name` | String | 居服員名稱(例:`居服員_1`)——佔位符,無真實個資 |
| `experience_years` | Integer | 實務經驗年資。隨機抽取自 `{1, 2, 3, 5, 8, 10}` |
| `primary_region` | String | 主責駐點鄉鎮市。依苗栗縣各鄉鎮實際人口比例作權重分配 |
| `cost_level` | String | 人力成本 / 薪資級距:`Senior` / `Mid` / `Junior`,可用於預測人力成本 |

---

## 二、個案主檔 `clients.csv`

記錄接受長照服務的失能個案基本資料,包含失能程度與地理位置。

| 欄位 | 型態 | 說明與生成邏輯 |
|---|---|---|
| `client_id` | String | 個案唯一識別碼,格式 `CL` + 三位數(例:`CL001`) |
| `care_level_cms` | Integer | 衛福部核定「長照需要等級」(CMS),範圍 2–8 級,數字越大代表失能越嚴重 |
| `complexity_weight` | Float | 照護複雜度加權係數,公式:`1.0 + (CMS − 2) × 0.15`,量化失能程度對服務造成的額外負擔 |
| `district` | String | 個案居住鄉鎮市,依苗栗縣人口實際分佈權重配置 |
| `location_lat` | Float | 模擬緯度(基於北緯 24.5° + 微小隨機擾動) |
| `location_lng` | Float | 模擬經度(基於東經 120.8° + 微小隨機擾動) |

---

## 三、服務派工與核銷日誌 `service_logs.csv`

資料集核心交易表(Transaction Table),記錄居服員每日對個案提供的服務細節、交通時間與核銷點數。

| 欄位 | 型態 | 說明與生成邏輯 |
|---|---|---|
| `caregiver_id` | String | 執行服務的居服員 ID(對應 `caregivers.csv` 外部鍵) |
| `client_id` | String | 接受服務的個案 ID(對應 `clients.csv` 外部鍵) |
| `service_date` | Date | 服務日期,格式 `YYYY-MM-DD`,從 `2026-08-01` 起算 14 天 |
| `travel_time_min` | Integer | 單趟交通時間(分鐘)。偏鄉(泰安、獅潭、南庄):30–50 分;一般地區:10–25 分 |
| `actual_service_hours` | Float | 實際服務工時(小時)。當次服務項目基本分鐘數總和,加上 −5 至 +15 分鐘隨機浮動,最低 0.5 小時 |
| `care_types_completed` | String | 當次執行的長照照顧組合代碼(BA 碼)。隨機抽 1–3 項,逗號分隔(例:`BA01,BA07`) |
| `service_base_points` | Integer | 政府法定基準點數(新台幣元)。當次各 BA 碼法定點數加總 |
| `final_weighted_points` | Integer | 模型加權負荷點數。`service_base_points × complexity_weight`,四捨五入 |

---

## 附註

- 所有姓名、ID 均為系統生成佔位符,不對應任何真實個人。
- 地理座標僅供資料結構練習,不宜用於實際地理分析。
- 詳細法規對照與參數依據,見 [`DATA_GOVERNANCE.md`](./DATA_GOVERNANCE.md)。
