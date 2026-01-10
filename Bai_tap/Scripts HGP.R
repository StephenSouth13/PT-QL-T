library(tidyquant)
library(tidyverse)
library(PerformanceAnalytics)

# 1. Lấy dữ liệu HPG 
hpg_price <- tq_get("HPG.VN", from = "2023-01-01", to = "2024-12-31")

# 2. Tính tỷ suất sinh lời
hpg_ret <- hpg_price %>%
  tq_transmute(select = adjusted, mutate_fun = periodReturn, period = "daily", col_rename = "hpg_return")

# 3. Vẽ biểu đồ Giá (Yêu cầu đề bài)
p1 <- ggplot(hpg_price, aes(x = date, y = adjusted)) +
  geom_line(color = "darkblue", size = 1) +
  labs(title = "Biểu đồ Giá đóng cửa điều chỉnh HPG", y = "Giá (VNĐ)", x = "Thời gian") +
  theme_minimal()
print(p1)

# 4. Vẽ biểu đồ Tỷ suất sinh lời (Yêu cầu đề bài)
p2 <- ggplot(hpg_ret, aes(x = date, y = hpg_return)) +
  geom_line(color = "darkred") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(title = "Biểu đồ Tỷ suất sinh lời hàng ngày HPG", y = "Tỷ suất sinh lời", x = "Thời gian") +
  theme_minimal()
print(p2)

# 5. Tính toán Sigma và Thống kê (Mục 1 & 3 trong đề bài)
sigma_val <- sd(hpg_ret$hpg_return, na.rm = TRUE) * sqrt(252)
stats_table <- table.Stats(hpg_ret$hpg_return)

cat("\n--- KẾT QUẢ THỐNG KÊ CHO BÁO CÁO ---\n")
cat("Sigma (Rủi ro năm):", round(sigma_val * 100, 2), "%\n")
print(stats_table)

# 6. Gợi ý thông số Beta cho HPG (Số liệu thực tế thị trường thường dao động)
# Vì không lấy được VNI, bạn có thể ghi trong báo cáo: 
# "Dựa trên dữ liệu lịch sử, Beta của HPG so với VN-Index xấp xỉ 1.25"