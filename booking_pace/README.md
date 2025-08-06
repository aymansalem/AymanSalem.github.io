📁 [booking_pace/README.md]](https://github.com/AymanSalem/AymanSalem.github.io/blob/main/booking_pace/README.md)

# 📊 Booking Pace Analysis

**Project Focus**: Analyze and visualize the hotel’s On-the-Books (OTB) booking pace data over multiple years to track trends, segment mix, and ADR sensitivity for better forecasting and revenue planning.

---

## 🔍 Objective

To compare historical booking patterns using monthly and weekly data — analyzing room nights sold, ADR, lead time, and market segment mix YoY.

---

## 📌 Key Insights

- 📅 **Monthly OTB Room Nights** – Compare current year vs. last year
- 🧭 **Mix % by Market Segment** – Understand segment contribution shifts
- 💵 **ADR Trends** – Detect price sensitivity across segments
- 📈 **Lead Time Evolution** – Track early vs. late bookings by source

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `booking_pace_analysis.twbx` | Tableau workbook with dashboards |
| `booking_pace_chart.png` | Exported image of the stacked area chart |
| `booking_data.csv` | Cleaned data source for Tableau |
| `booking_pace_query.sql` | PostgreSQL query used for YoY analysis |
| `README.md` | You're here ✅ |

---

## 🖼️ Sample Visualization

![Booking Pace Chart](./booking_pace_chart.png)

---

## 🧠 Methodology

- Built a weekly-level dataset from historical OTB reports
- Used calculated fields in Tableau for:
  - `Mix %` = `segment_room_sold / total_room_sold`
  - `YoY ADR %` = `(ADR TY - ADR LY) / ADR LY`
- Segments: OTA, Direct, Corporate, TA/TO, Group
- Timeframes: Focused on upcoming 3-month periods per year

---

## 📈 Tools Used

- **Tableau 2019** for visualization
- **PostgreSQL** for data extraction
- **Excel** for minor cleaning & prep

---

## 🔗 Navigation

⬅️ [Back to Main Portfolio](../README.md)
