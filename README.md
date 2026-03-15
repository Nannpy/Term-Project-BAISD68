# AI Disease Surveillance Analytics Dashboard

ระบบ **Dashboard วิเคราะห์และพยากรณ์โรคติดต่อด้วย AI** สำหรับข้อมูลเฝ้าระวังโรค (Disease Surveillance Data)

พัฒนาด้วย

* Python
* Pandas
* Plotly
* Plotly Dash

ระบบนี้ผสานการวิเคราะห์ข้อมูลระบาดวิทยา (Epidemiological Analytics) เข้ากับ **Machine Learning Prediction** เพื่อช่วยในการ

* วิเคราะห์สถานการณ์โรค
* ตรวจจับพื้นที่เสี่ยงการระบาด
* วิเคราะห์ความล่าช้าในการรายงานโรค
* แจ้งเตือนการระบาดล่วงหน้า

---

# ภาพรวมของระบบ

ระบบนี้เป็น **Data Analytics + AI Prediction Platform** สำหรับข้อมูลเฝ้าระวังโรคติดต่อ

ฟีเจอร์หลักของระบบประกอบด้วย

* Dashboard วิเคราะห์ข้อมูลโรค
* การแสดงผลเชิงพื้นที่ (Geographic Analysis)
* การวิเคราะห์ข้อมูลประชากร (Demographic Analysis)
* การวิเคราะห์ระบบรายงานโรค (Surveillance Monitoring)
* โมเดล Machine Learning สำหรับการพยากรณ์

ระบบถูกออกแบบให้สามารถ **เพิ่มโมเดล AI ใหม่ได้ในอนาคต**

---

# วิธีใช้งาน (Quick Start)

ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

รัน Dashboard

```bash
python dashboard/app.py
```

เปิดผ่าน browser

```
http://127.0.0.1:8050
```

---

# โครงสร้างโปรเจค

```
project/
├── dashboard/
│   └── app.py                  # จุดเริ่มต้นของ Dash Application
│
├── core/
│   ├── data_loader.py          # โหลดและทำความสะอาดข้อมูล
│   ├── feature_engineering.py  # สร้าง feature สำหรับวิเคราะห์
│   └── kpi_engine.py           # คำนวณ KPI ต่างๆ
│
├── visualization/
│   ├── theme.py                # theme และ style ของ dashboard
│   └── charts.py               # ฟังก์ชันสร้างกราฟ
│
├── ui/
│   ├── layout.py               # layout ของ dashboard
│   ├── callbacks.py            # Dash callbacks
│   └── filters.py              # ระบบ filter ข้อมูล
│
├── ml/
│   ├── model_interface.py      # โครงสร้างมาตรฐานของ ML model
│   ├── feature_pipeline.py     # เตรียม feature สำหรับ ML
│   ├── predictor.py            # โหลดโมเดลและทำนายผล
│   └── model_registry.py       # ระบบลงทะเบียนโมเดล
│
├── models/
│   ├── diseasehotspot.pkl      # โมเดลทำนายพื้นที่เสี่ยง
│   └── reportinglag.pkl        # โมเดลทำนายความล่าช้าในการรายงาน
│
├── requirements.txt
└── README.md
```

---

# ส่วนต่างๆของ Dashboard

Dashboard แบ่งออกเป็น 5 ส่วนหลัก

| Tab          | รายละเอียด                |
| ------------ | ------------------------- |
| Overview     | ภาพรวมการระบาดของโรค      |
| Geographic   | การกระจายตัวตามพื้นที่    |
| Demographic  | การวิเคราะห์ข้อมูลประชากร |
| Surveillance | วิเคราะห์ระบบรายงานโรค    |
| Prediction   | การพยากรณ์ด้วย AI         |

---

# ระบบ Filter

ผู้ใช้สามารถกรองข้อมูลได้ผ่าน filter ด้านบนของ dashboard

* Year
* Province
* District
* Sex
* Age Group

กราฟทั้งหมดจะปรับตาม filter ที่เลือกแบบ **interactive**

---

# KPI Dashboard

Dashboard แสดงตัวชี้วัดสำคัญ ได้แก่

| KPI                | ความหมาย             |
| ------------------ | -------------------- |
| Total Cases        | จำนวนผู้ป่วยทั้งหมด  |
| Total Deaths       | จำนวนผู้เสียชีวิต    |
| Case Fatality Rate | อัตราการเสียชีวิต    |
| Average Age        | อายุเฉลี่ยของผู้ป่วย |
| Male : Female      | สัดส่วนเพศของผู้ป่วย |

---

# 1 Overview (ภาพรวมการระบาด)

ส่วนนี้แสดงแนวโน้มของโรคตามเวลา

### Cases Over Time

กราฟแสดงจำนวนผู้ป่วยตามช่วงเวลา
ช่วยวิเคราะห์แนวโน้มการระบาด

### Deaths Over Time

กราฟแสดงจำนวนผู้เสียชีวิตตามเวลา

### Weekly Case Trends

แสดงจำนวนผู้ป่วยในแต่ละสัปดาห์ของปี
ช่วยวิเคราะห์ **seasonality ของโรค**

---

# 2 Geographic Analysis

วิเคราะห์การกระจายของโรคตามพื้นที่

### Top Provinces by Case Count

จังหวัดที่มีจำนวนผู้ป่วยมากที่สุด

### Top Districts by Case Count

อำเภอที่มีจำนวนผู้ป่วยสูง

ช่วยระบุ **พื้นที่ที่มีภาระโรคสูง**

---

# 3 Demographic Analysis

วิเคราะห์ข้อมูลประชากรของผู้ป่วย

### Age Distribution

การกระจายตัวของอายุผู้ป่วย

### Sex Distribution

สัดส่วนเพศของผู้ป่วย

* Male
* Female
* Unknown

### Cases by Age Group

แบ่งผู้ป่วยตามช่วงอายุ เช่น

```
0–4
5–14
15–24
25–34
35–44
45–54
55–64
65+
```

### Top Occupations

อาชีพที่พบผู้ป่วยมากที่สุด

---

# 4 Surveillance Monitoring

วิเคราะห์ประสิทธิภาพของระบบรายงานโรค

### Reporting Delay Distribution

จำนวนวันที่ใช้ในการรายงานผู้ป่วย

### Diagnosis Delay Distribution

ระยะเวลาระหว่างเริ่มป่วยจนถึงการวินิจฉัย

### Average Reporting Delay by Province

ค่าเฉลี่ยความล่าช้าในการรายงานของแต่ละจังหวัด

ช่วยตรวจสอบ **ประสิทธิภาพของระบบ surveillance**

---

# 5 AI Prediction

ส่วนนี้เป็นระบบ **Machine Learning Prediction**

ใช้โมเดล AI เพื่อพยากรณ์

* พื้นที่เสี่ยงการระบาด
* ความล่าช้าในการรายงาน

ผู้ใช้สามารถเลือก

```
Province → District → Run Prediction
```

---

# ผลลัพธ์การพยากรณ์

ระบบจะแสดงผลลัพธ์ เช่น

```
Risk Level: LOW
Province: นครนายก
District: คลองหลวง
Hotspot Probability: 30.29%
Predicted Reporting Lag: 8.8 days
```

---

# Hotspot Probability Gauge

แสดงความน่าจะเป็นของการเกิดพื้นที่เสี่ยง

| Probability | Risk Level    |
| ----------- | ------------- |
| 0–40%       | Low Risk      |
| 40–70%      | Medium Risk   |
| 70–80%      | High Risk     |
| 80–100%     | Outbreak Risk |

---

# Feature Importance (AI Explanation)

แสดงว่า feature ใดมีผลต่อการพยากรณ์ของโมเดลมากที่สุด

ตัวอย่าง feature

* Population Density
* Seasonal Factor
* Average Age
* Reporting Delay
* Case Count
* Death Rate

ช่วยให้ผู้ใช้เข้าใจว่า **โมเดลตัดสินใจอย่างไร**

---

# Outbreak Early Warning

ระบบมีระบบแจ้งเตือนการระบาด

เงื่อนไข

```
Hotspot Probability ≥ 0.80
```

ระบบจะแสดง

```
⚠ OUTBREAK WARNING
High outbreak risk detected
```

เพื่อให้สามารถตอบสนองต่อการระบาดได้เร็วขึ้น

---

# Machine Learning Models

ระบบใช้โมเดล AI 2 โมเดล

### Disease Hotspot Prediction

ใช้พยากรณ์ความเสี่ยงการเกิด **พื้นที่ระบาด**

Output

```
Hotspot Probability
Risk Level
```

---

### Reporting Lag Predictor

ใช้พยากรณ์ความล่าช้าในการรายงานผู้ป่วย

Output

```
Predicted Reporting Delay (days)
```

---

# การเพิ่มโมเดล AI ใหม่

สามารถเพิ่มโมเดลใหม่ได้โดย

1 Train model
2 Implement ModelInterface
3 Register ใน model_registry
4 เรียกใช้ผ่าน predictor

ตัวอย่าง registry

```python
REGISTRY = {
    "hotspot": "ml.hotspot_predictor.HotspotPredictor",
    "delay": "ml.delay_predictor.ReportingDelayPredictor",
}
```

---

# การใช้งานร่วมกับ Framework อื่น

สามารถนำ Dashboard ไปใช้ร่วมกับ

* Flask
* FastAPI

ตัวอย่าง

```python
from dashboard.app import create_app

dash_app = create_app()
flask_server = dash_app.server
```

---

# การพัฒนาในอนาคต

แนวทางพัฒนาต่อ

* Real-time surveillance data
* Spatio-temporal outbreak prediction
* Automated outbreak alerts
* Multi-disease monitoring
* Integration with public health systems

---

# License

สำหรับการใช้งานภายในและการพัฒนาเพิ่มเติม
