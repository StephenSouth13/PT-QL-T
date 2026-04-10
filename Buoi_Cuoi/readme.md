# 📊 Portfolio Optimization & Financial Theory (Markowitz - CAPM)

## 👨‍💻 Author
Quách Thành Long

---

# 🧠 1. Efficient Frontier (Đường biên hiệu quả)

## 📌 Định nghĩa
Efficient Frontier là tập hợp các danh mục đầu tư tối ưu:
- Mang lại **lợi nhuận kỳ vọng cao nhất** cho một mức rủi ro nhất định
- Hoặc **rủi ro thấp nhất** cho một mức lợi nhuận kỳ vọng nhất định

## 📈 Hình dáng
- Trục X: Rủi ro (σ - Standard Deviation)
- Trục Y: Lợi nhuận kỳ vọng (E[R])
- Dạng: Đường cong hướng **lên trên và sang trái**

## 🎯 Ý nghĩa
- Danh mục nằm trên đường → **Hiệu quả**
- Danh mục nằm dưới → **Kém hiệu quả**
  - Vì tồn tại danh mục khác:
    - Cùng rủi ro → lời hơn
    - Cùng lợi nhuận → ít rủi ro hơn

---

# 🛡 2. Minimum Variance Portfolio (MVP)

## 📌 Định nghĩa
Danh mục có **rủi ro thấp nhất có thể** khi kết hợp các tài sản.

👉 Đây là **điểm ngoài cùng bên trái của Efficient Frontier**

## 🧮 Công thức (2 tài sản)

\[
w_1 = \frac{\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}}{\sigma_2^2 - \sigma_{12}}
\]

## 💡 Ý nghĩa
- Xác định tỷ trọng đầu tư tối ưu để **giảm rủi ro tối đa**
- Trong code:
```python
w_fpt_mvp = ...
💰 3. CAPM (Capital Asset Pricing Model)
📌 Công thức
𝐸
(
𝑅
𝑖
)
=
𝑅
𝑓
+
𝛽
𝑖
[
𝐸
(
𝑅
𝑚
)
−
𝑅
𝑓
]
E(R
i
	​

)=R
f
	​

+β
i
	​

[E(R
m
	​

)−R
f
	​

]
🔍 Giải thích
Rf (Risk-free rate)
→ Lãi suất phi rủi ro (trái phiếu chính phủ)
β (Beta)
→ Độ nhạy của cổ phiếu so với thị trường
Market Risk Premium
→ 
𝐸
(
𝑅
𝑚
)
−
𝑅
𝑓
E(R
m
	​

)−R
f
	​


→ Phần bù rủi ro thị trường
🎯 Ý nghĩa

CAPM giúp trả lời:

Một cổ phiếu "xứng đáng" có lợi nhuận bao nhiêu dựa trên rủi ro của nó?

📊 4. Statistics (Giải mã bảng dữ liệu)
📉 Standard Deviation (SD)
Đo lường rủi ro tổng thể
SD cao → biến động mạnh → khó đoán
📐 Skewness (Độ lệch)
= 0 → Phân phối chuẩn

0 → Lệch phải
→ Có khả năng xuất hiện lợi nhuận cực cao (hiếm)

< 0 → Lệch trái
→ Rủi ro giảm mạnh bất ngờ (nguy hiểm)
⚠️ Excess Kurtosis (Độ nhọn dư)
= 0 → Chuẩn

0 → Fat tail (đuôi béo)

👉 Ý nghĩa:

Thị trường thực tế KHÔNG "hiền" như lý thuyết
Các cú sập mạnh xảy ra thường xuyên hơn
📈 5. Alpha (α) & Beta (β) - Regression
📌 Mô hình
lm(FPT_excess ~ Market_excess)
🔵 Beta (β)
Độ nhạy với thị trường
Ví dụ:
β = 1.058
→ Thị trường tăng 1% → FPT tăng ~1.058%

👉 >1 → cổ phiếu "aggressive"
👉 <1 → cổ phiếu "defensive"

🟢 Alpha (α)
Lợi nhuận vượt kỳ vọng

👉 Nếu:

α > 0 và p-value < 0.05
→ Bạn đang outperform thị trường 😎

👉 Nhưng nếu:

α ≈ 0, p-value lớn
→ Cổ phiếu vận hành đúng thị trường (efficient)
🧠 Kết luận cốt lõi
Efficient Frontier = giới hạn tối ưu
MVP = điểm ít rủi ro nhất
CAPM = định giá lợi nhuận hợp lý
Beta = độ nhạy
Alpha = khả năng "đánh bại thị trường"
❓ Có thật là khó đánh bại thị trường?

👉 Theo lý thuyết:

Thị trường gần như hiệu quả (Efficient Market Hypothesis)

👉 Điều đó nghĩa là:

Rất khó để consistently:
Kiếm lợi nhuận vượt thị trường
Nếu không có lợi thế đặc biệt (data, insight, timing)

