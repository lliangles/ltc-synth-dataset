# ltc-synth-dataset

**符合衛福部支付基準的長照 2.0 擬真合成資料集**
Rule-based synthetic dataset for Taiwan's Long-Term Care 2.0 (LTC 2.0) service system, aligned with MOHW payment standards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Data: Synthetic](https://img.shields.io/badge/Data-100%25%20Synthetic-brightgreen.svg)](#data-privacy)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python%203-blue.svg)](#stack)

---

## 為什麼做這個 / Why this project

台灣長照 2.0 服務派工資料公開性極低——涉及個資,加上 BA 碼、CMS 等級、給付點數等制度門檻,想動手練習的學生與研究者幾乎沒有現成起點。

這個 repo 提供一份**符合衛福部支付基準**的合成資料集:20 名居服員 × 60 名個案 × 14 天服務日誌,規則透明、法規對接明確,可直接用於研究、教學與原型開發。作者在學期間修過資料處理相關課程後,利用暑假把構想落實成可重現的存庫,同時作為個人作品集。

**適合的用途**
- 排班演算法(VRP / TSP)測試資料
- 資料工程 pipeline 練習
- 長照相關 AI 產品原型
- 課程作業與教學範例

**不適合的用途**
- 實際政策決策或業務營運——資料為規則合成,具體人口權重需自行核實(見「資料驗證狀態」章節)
- 需要真實個案分布或真實地理軌跡的研究

> Public LTC dispatch data in Taiwan is scarce due to privacy and regulatory complexity. This repo provides a rule-based, MOHW-aligned synthetic dataset (20 caregivers × 60 clients × 14 days) for prototyping, coursework, and portfolio use — no privacy risk, no application paperwork.

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

## 資料驗證狀態 / Data Verification Status

本節透明說明資料集中各項技術主張的驗證程度,協助使用者判斷可信度範圍。
_(驗證日期:2026-09)_

| 資料項 | 狀態 | 來源 / 說明 |
|---|---|---|
| BA01, BA02, BA07, BA10, BA14, BA15, BA16 點數 | **已驗證** | 對應衛福部長照 2.0 給付支付基準;點數與現行公告一致 |
| CMS 2–8 級為法定給付對象 | **已驗證** | 「長期照顧服務申請及給付辦法」第 3 條 |
| 苗栗縣 18 鄉鎮清單 | **已驗證** | 苗栗縣行政區劃 |
| 個案複雜度加權公式 `1.0 + (CMS−2) × 0.15` | **研究假設** | 專案自訂之 Care Complexity Index,非政府公式 |
| 各鄉鎮人口權重具體數值 | **方向性正確** | 城鎮權重高、偏鄉低的分佈方向符合公開資料;具體百分比為研究估算,未逐項對照特定年月統計 |
| 偏鄉交通時間區間(30–50 分) | **實務估算** | 依苗栗山區地形推估;非實測 |
| 次數型 BA 項目工時 | **實務估算** | 依長照特約機構作業常態推估;非法定值 |
| BA15 / BA16 未實作 -1/-2 細分版本 | **簡化** | 現行法規有 BA15-1 自用 / BA15-2 共用等細分,本資料集採基準版 |

**分類說明:**
- **已驗證**:對應現行政府公告,可直接引用
- **研究假設**:專案自訂模型,可修改替換
- **方向性正確 / 實務估算**:大方向合理但具體數值需自行核實
- **簡化**:相對於完整法規結構的合理縮減

> 使用者若需將本資料集用於實務決策(而非演算法測試 / 教學),請自行對照衛福部最新公告與地方主管機關統計。

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

GitHub: [@lliangles](https://github.com/lliangles)
Contact: `186920554+lliangles@users.noreply.github.com`
