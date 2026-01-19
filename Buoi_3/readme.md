# Buổi 3: Phân tích Rủi ro và Mô hình Định giá Tài sản Vốn (CAPM)

Tài liệu tóm tắt lý thuyết về rủi ro đầu tư và hướng dẫn thực hành ước lượng hệ số Beta, đường SML trên ngôn ngữ R.

---

## 1. Lý thuyết về Rủi ro Tổng thể (Total Risk)

Trong đầu tư tài chính, rủi ro tổng thể của một tài sản được cấu thành từ hai thành phần:

### a. Rủi ro phi hệ thống (Unsystematic Risk)
* **Bản chất:** Là rủi ro nội tại, đặc thù của riêng doanh nghiệp hoặc ngành (ví dụ: đình công, sai phạm lãnh đạo).
* **Đặc điểm:** Có thể triệt tiêu bằng cách đa dạng hóa danh mục đầu tư. Khi số lượng tài sản tăng lên, rủi ro này sẽ **tiến về 0**.

### b. Rủi ro hệ thống (Systematic Risk)
* **Bản chất:** Là rủi ro từ các tác động bên ngoài, vĩ mô (ví dụ: lạm phát, lãi suất, chính trị).
* **Đặc điểm:** Ảnh hưởng đến toàn bộ thị trường và **không thể loại bỏ** bằng cách đa dạng hóa.
* **Thước đo:** Được đo lường bằng hệ số **Beta ($\beta$)**.

---

## 2. Mô hình Định giá Tài sản Vốn (CAPM) & SML

Mô hình CAPM thiết lập mối quan hệ giữa lợi nhuận kỳ vọng và rủi ro hệ thống.

### 2.1 Công thức tính Beta ($\beta$)
$$\beta_i = \frac{Cov(R_i, R_m)}{Var(R_m)}$$

### 2.2 Phương trình CAPM
$$E(R_i) = R_f + \beta_i(E(R_m) - R_f)$$

**Trong đó:**
- $R_f$: Lãi suất phi rủi ro (Risk-free rate).
- $E(R_m) - R_f$: Phần bù rủi ro thị trường (Market Risk Premium).
- $E(R_i)$: Tỷ suất sinh lời kỳ vọng của tài sản $i$.

---

## 3. Thực hành trên R

### 3.1 Thiết lập dữ liệu ban đầu
Giả sử lãi suất phi rủi ro là 3%/năm và thị trường hoạt động 250 ngày/năm.

```r
# 1. Tính lợi nhuận thị trường (Market Return)
Rm <- rowMeans(R) 

# 2. Thiết lập lãi suất phi rủi ro
rf_annual <- 0.03
rf_daily  <- rf_annual / 250

# 3. Tính lợi nhuận vượt mức (Excess Returns)
Ri_excess <- R - rf_daily
Rm_excess <- Rm - rf_daily

3.2 Ước lượng BetaCách 1: Tính toán theo công thức hiệp phương saiRbeta_calc <- apply(R, 2, function(x) cov(x, Rm) / var(Rm))
Cách 2: Sử dụng mô hình hồi quy (Phương pháp chuẩn)$$R_i - R_f = \alpha_i + \beta_i(R_m - R_f) + \epsilon_i$$R# Ví dụ cho chỉ số DAX
capm_DAX <- lm(Ri_excess[, "DAX"] ~ Rm_excess)
summary(capm_DAX)

# Giải thích cho sinh viên:
# - (Intercept) = alpha (Hệ số chặn)
# - Rm_excess   = beta (Hệ số góc)
# - R-squared    = Mức độ biến động mà CAPM giải thích được
3.3 Ước lượng hàng loạt cho toàn bộ danh mụcR# Lấy toàn bộ Beta từ mô hình hồi quy
beta_lm <- apply(Ri_excess, 2, function(x) coef(lm(x ~ Rm_excess))[2])

# Lấy toàn bộ Alpha
alpha_lm <- apply(Ri_excess, 2, function(x) coef(lm(x ~ Rm_excess))[1])

# Hiển thị kết quả so sánh
round(cbind(alpha = alpha_lm, beta = beta_lm), 4)
3.4 Tính toán Lợi nhuận kỳ vọng (Expected Return)So sánh lợi nhuận dự báo theo mô hình CAPM với lợi nhuận thực tế.RERm <- mean(as.numeric(Rm)) * 250          # Lợi nhuận thị trường năm hóa
ERP <- ERm - as.numeric(rf_annual)         # Phần bù rủi ro thị trường

# Tính ER theo công thức CAPM
ER_capm <- as.numeric(rf_annual) + as.numeric(beta_lm) * as.numeric(ERP)

# So sánh với thực tế
ER_real <- colMeans(R) * 250
round(cbind(Real = ER_real, CAPM = ER_capm), 4)
4. Vẽ đường SML (Security Market Line)Đường SML giúp trực quan hóa mối quan hệ giữa rủi ro ($\beta$) và lợi nhuận.R# 1. Chuẩn bị dữ liệu
assets <- colnames(R)
beta_all <- as.numeric(beta_lm)
ER_real_all <- as.numeric(ER_real)

# 2. Tạo đường thẳng SML lý thuyết
x_line <- seq(min(beta_all) - 0.1, max(beta_all) + 0.1, length.out = 200)
y_line <- rf_annual + x_line * ERP

# 3. Vẽ đồ thị
plot(x_line, y_line, type = "l", lwd = 2,
     xlim = range(beta_all) + c(-0.1, 0.1),
     ylim = range(ER_real_all) + c(-0.02, 0.02),
     xlab = expression(beta), ylab = "Expected return (annual)",
     main = "Security Market Line (SML) – European Indices")

# 4. Thêm các điểm dữ liệu thực tế
points(beta_all, ER_real_all, pch = 16, cex = 1.4)
text(beta_all, ER_real_all, labels = assets, pos = 4, cex = 0.9)

# 5. Chú thích
legend("topleft", legend = c("SML", "Realized return"),
       lty = c(1, NA), pch = c(NA, 16), bty = "n")
5. Kiểm định Mô hìnhĐể xác định CAPM có giải thích tốt dữ liệu hay không, ta kiểm định giá trị Alpha ($\alpha$):Lý thuyết: Trong thị trường hiệu quả, $\alpha$ phải bằng 0.Nếu $\alpha$ không có ý nghĩa thống kê (p-value > 0.05): CAPM không bị bác bỏ, lợi nhuận được giải thích tốt bởi rủi ro hệ thống.Nếu $\alpha$ khác 0 (p-value < 0.05): CAPM không giải thích hết lợi nhuận. Có thể có cơ hội đầu tư (Underpriced/Overpriced).Cập nhật lần cuối: Năm 2026



INPUT theo mô hinh Top-Down:
Ví dụ đầu tư cổ phiếu: Kinh tế vĩ mô -> Ngành ->Cty(Tài chính) =>Input:
- Lãi suất phi rủi ro
- Lãi suất cổ phiếu
- Rủi ro hệ thống (Beta)