
# 📊 Portfolio Theory – Lợi nhuận & Rủi ro

## 1. 📈 Lợi nhuận kỳ vọng *(Expected Return – E(r))*

Lợi nhuận kỳ vọng của danh mục được tính dựa trên tỷ trọng đầu tư và lợi nhuận kỳ vọng của từng tài sản.

### 🔹 Công thức tổng quát

E(rp)=∑i=1nwi⋅E(ri)E(r_p) = \sum_{i=1}^{n} w_i \cdot E(r_i)
**E**(**r**p****)**=**i**=**1**∑**n****w**i****⋅**E**(**r**i****)**
**Trong đó:**

* `w_i`: Tỷ trọng đầu tư vào tài sản *i*
* `E(r_i)`: Lợi nhuận kỳ vọng của tài sản *i*

---

### 🔹 Đo lường

* Ước lượng từ dữ liệu lịch sử
* Phương pháp:
* Trung bình cộng
* Trung bình có trọng số
* Độ biến động: **σ (Sigma)**

---

## 2. ⚠️ Rủi ro *(Risk)*

Rủi ro của danh mục được đo bằng độ lệch chuẩn (σ) hoặc phương sai.

### 🔹 Công thức

σp=∑wi2σi2+∑∑wiwj Cov(ri,rj)\sigma_p = \sqrt
**σ**p=**∑**w**i**2σ**i**2+**∑∑**w**i****w**jC**o**v**(**r**i,**r**j)**
------------------------------------

## 3. 🔁 Bán khống *(Short Selling)*

### 📌 Khái niệm

wx<0w_x < 0
**w**x<**0**

* Nhà đầu tư vay tài sản để bán
* Kỳ vọng mua lại với giá thấp hơn

---

### 🔹 Ví dụ minh họa

| Tài sản | Tỷ trọng     |
| --------- | -------------- |
| X         | `w_x = -0.1` |
| Y         | `w_y = 1.1`  |

👉 Tổng danh mục:

wx+wy=1w_x + w_y = 1
**w**x+**w**y=**1**
-----------

### 🔹 Diễn giải

* Bán khống **10% cổ phiếu X**
* Dùng tiền để đầu tư **110% vào cổ phiếu Y**

➡️ Kết quả:

* Tăng lợi nhuận kỳ vọng (nếu Y tốt hơn)
* Nhưng rủi ro tăng mạnh

---

## 4. 📊 Công thức lợi nhuận danh mục (2 tài sản)

E(rp)=wx⋅E(rx)+wy⋅E(ry)E(r_p) = w_x \cdot E(r_x) + w_y \cdot E(r_y)
**E**(**r**p)**=**w**x****⋅**E**(**r**x****)**+**w**y****⋅**E**(**r**y****)
---------------------------------------------------------------------

## 5. ⚡ Insight quan trọng

### ✔ Không bán khống

0≤wi≤10 \le w_i \le 1
**0**≤**w**i≤**1**

### ❗ Có bán khống

* `w_i < 0` → Short
* `w_i > 1` → Leverage

➡️ Danh mục có đòn bẩy cao hơn

---

## 6. 🚀 Ứng dụng thực tế

* Tối ưu danh mục đầu tư *(Modern Portfolio Theory)*
* Xây dựng Efficient Frontier
* Tối ưu hóa Sharpe Ratio

---

## ✨ Tổng kết

| Yếu tố  | Ý nghĩa             |
| --------- | --------------------- |
| `E(r)`  | Lợi nhuận kỳ vọng |
| `σ`    | Rủi ro               |
| `w < 0` | Bán khống           |
| `w > 1` | Đòn bẩy            |

Hiệp phương sai(Covariance) là gì ?
Là đo lường sự chuyển của 2 biến ngẫu nhiên đặt trong sự tương quan lẫn nhau



