# ltc-synth-dataset

**符合衛福部支付基準的長照 2.0 擬真合成資料集**
Rule-based synthetic dataset for Taiwan's Long-Term Care 2.0 (LTC 2.0) service system, aligned with MOHW payment standards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Data: Synthetic](https://img.shields.io/badge/Data-100%25%20Synthetic-brightgreen.svg)](#data-privacy)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python%203-blue.svg)](#stack)

---

## 為什麼做這個 / Why this project

長照 2.0 是台灣現行最重要的社會照護制度之一,但公開可用的服務派工資料極少——一方面涉及個資,另一方面制度本身(BA 碼、CMS 等級、給付點數)對開發者、學生、研究者都有一定門檻。

我在大一資管課程接觸資料集建構後,發現「與其等別人開放資料,不如自己動手做一份**規則合法、法規對接明確、結構真實**的合成資料集」,可以用來:

- 練習資料工程 pipeline
- 給排班演算法、成本模型、視覺化 dashboard 當測試資料
- 讓其他學生 / 研究者可以直接拿來做 side project,不需要跟主管機關申請

這個 repo 就是這個想法的第一個版本。

> Public Long-Term Care service dispatch data in Taiwan is scarce due to privacy and regulatory complexity. This repo provides a **rule-based, regulation-aligned synthetic dataset** for algorithm prototyping, coursework, and portfolio use — no privacy risk, no application paperwork.

---

## 資料集內容 / What's inside

| 檔案 | 筆數 | 說明 |
|---|---|---|
| `data/caregivers.csv` | 20 名居服員 | ID / 姓名 / 年資 / 主要駐點 / 職級 |
| `data/clients.csv` | 60 名個案 | ID / CMS 失能等級 / 複雜度加權 / 苗栗鄉鎮 / 模擬經緯度 |
| `data/service_logs.csv` | 1,125 筆服務日誌 | 14 天派工紀錄,含交通時間、實際工時、BA 碼組合、基準點數、加權點數 |
| `src/generate.py` | Python 腳本 | Rule-Based Synthetic Data Engine(pandas + numpy) |
| `docs/DATA_DICTIONARY.md` | 資料字典 | 每張表每個欄位的定義與生成邏輯 |
| `docs/DATA_GOVERNANCE.md` | 治理文件 | 每個關鍵參數對應的政府公開資料 / 法規依據 |

---

## 技術特色 / Technical highlights

### 1. 真實基礎資料 — Real-world grounded

- 地理權重:20 個苗栗鄉鎮的個案 / 居服員分佈,依據**苗栗縣政府民政處**現住人口統計比例分配(頭份 18%、苗栗市 16%、竹南 14%……泰安 1%)。
- 座標:基於北緯 24.5°、東經 120.8° 加入小幅隨機擾動,符合苗栗實際範圍。

### 2. 法規對接 — Regulation-aligned

| 欄位 | 對接法規 |
|---|---|
| BA 碼點數 | 衛福部「[長期照顧給付及支付基準](https://www.mohw.gov.tw/cp-4637-57129-1.html)」附表三 |
| CMS 2–8 級 | 「[長期照顧服務申請及給付辦法](https://www.mohw.gov.tw/cp-18-57129-1.html)」第 3 條 |
| 偏鄉交通時間差異 | 泰安、獅潭、南庄山區地形實況 |

BA 碼金額**完全對應**現行給付標準(1 點 = 新台幣 1 元)。CMS 排除第 1 級(未達給付門檻),聚焦法定給付對象。

### 3. 邏輯化擬真 — Logic-driven, not random noise

服務工時、每日案量(3–5 案 / 人)、複雜度加權公式 `1.0 + (CMS − 2) × 0.15` 都寫入 Python 腳本,不是純隨機。基準點數與加權點數清楚拆分為 `service_base_points`(政府法定)與 `final_weighted_points`(研究模型),避免混淆。

### 4. 資料隱私與合規 — Data privacy

**100% 合成資料,無真人個資風險。** 所有姓名為「居服員_1」等佔位符;地址僅到鄉鎮層級 + 模擬座標。

---

## 快速開始 / Quick start

```bash
# Clone
git clone https://github.com/lliangles/ltc-synth-dataset.git
cd ltc-synth-dataset

# 讀取資料
python
>>> import pandas as pd
>>> logs = pd.read_csv("data/service_logs.csv")
>>> logs.head()

# 重新生成資料集(可調整參數)
python src/generate.py
```

---

## Stack

- Python 3.x
- pandas / numpy
- Rule-Based Synthetic Data Engine(自實作)

---

## 未來延伸應用 / Potential extensions

- **排班演算法 PoC**:用 service_logs 當輸入,套 VRP / TSP 做居服員路徑最佳化。
- **人力成本模型**:結合 `cost_level` × `actual_service_hours` 估算月度人事支出。
- **視覺化 dashboard**:苗栗縣熱區圖 + 居服員負荷分析。
- **偏鄉加成擴充**:參考衛福部原住民族地區給付加計 20% 規則,豐富法規對接深度。
- **BA 碼組合限制**:目前隨機抽 1–3 項,可加入互斥組合的實務規則。

---

## Data Privacy

This dataset is **100% synthetic**. All names are placeholders (e.g. `居服員_1`), all addresses are aggregated to township level with jittered coordinates, and no record corresponds to any real caregiver or client. Safe to publish, redistribute, and use in academic / commercial contexts under the MIT License.

---

## 授權 / License

- **Code & data**: [MIT License](./LICENSE)
- **法規引用**:衛生福利部相關法規為公開資料,依政府資訊公開法可自由引用。

---

## 引用紀錄 / Used in

_這個章節保留給後續使用這份資料集的比賽、課程作業、論文、作品集。_

<!-- 使用範例:
- [Project Name] — 用途簡述 — 2026/XX
- 課程名稱 - 學期 - 使用範圍
-->

---

## 作者 / Author

**Liang** — Information Management, National United University (NUU)
GitHub: [@lliangles](https://github.com/lliangles)
