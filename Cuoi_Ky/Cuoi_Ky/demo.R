# ==============================================================================
# ĐỀ ÁN CÁ NHÂN CUỐI KỲ - TÀI CHÍNH ĐỊNH LƯỢNG
# Sinh viên thực hiện: [Tên của bạn]
# ==============================================================================

# --- 0. KHAI BÁO THƯ VIỆN ---
library(quantmod)
library(xts)
library(PerformanceAnalytics)
library(tseries)

# --- 1. CHUẨN BỊ DỮ LIỆU (CÂU 1 & 2) ---
# Lấy dữ liệu 5 mã HOSE: FPT, VCB, HPG, VNM, MSN
symbols <- c("FPT.VN", "VCB.VN", "HPG.VN", "VNM.VN", "MSN.VN")
getSymbols(symbols, src = "yahoo", from = "2024-04-10", to = "2026-04-10")

# Xử lý dữ liệu FPT cho Câu 1 (Làm sạch NA)
fpt_data <- na.omit(FPT.VN)
fpt_clean <- fpt_data
R_fpt <- na.omit(diff(log(Cl(fpt_clean)))) # Log return [cite: 8]

# --- 2. CÂU 1: PHÂN TÍCH KỸ THUẬT (3 ĐIỂM) ---
# Xuất file ảnh báo cáo Câu 1
png("PTKT_FPT.png", width = 1000, height = 800)
chartSeries(fpt_clean, theme = chartTheme("white"), name = "Phân tích kỹ thuật FPT")
addSMA(n = 5, col = "blue")   # SMA(5)
addSMA(n = 20, col = "red")   # SMA(20)
addMACD(fast = 12, slow = 26, signal = 9) # MACD
addBBands(n = 20, sd = 2)    # Bollinger Bands
addRSI(n = 14)               # RSI
dev.off()

# --- 3. CÂU 2A: THỐNG KÊ MÔ TẢ (7 ĐIỂM) ---
# Gộp giá đóng cửa và tính log return cho 5 mã
prices <- merge(Cl(FPT.VN), Cl(VCB.VN), Cl(HPG.VN), Cl(VNM.VN), Cl(MSN.VN))
colnames(prices) <- c("FPT", "VCB", "HPG", "VNM", "MSN")
R_all <- na.omit(diff(log(prices))) # [cite: 8]

# Tính toán các chỉ số thống kê [cite: 17-21, 35-45]
mu <- colMeans(R_all)
sd_v <- apply(R_all, 2, sd)
var_v <- apply(R_all, 2, var)
skew_v <- apply(R_all, 2, function(x) { m <- mean(x); s <- sd(x); mean((x - m)^3)/(s^3) })
ex_kurt_v <- apply(R_all, 2, function(x) { m <- mean(x); s <- sd(x); mean((x - m)^4)/(s^4) - 3 })

# Xuất bảng thống kê ra CSV (Excel nộp bài)
stats_table <- data.frame(Mean = mu, SD = sd_v, Variance = var_v, Skewness = skew_v, Excess_Kurtosis = ex_kurt_v)
write.csv(stats_table, "Bao_cao_Thong_ke_5_ma.csv")

# Xuất ảnh Histogram Câu 2A
png("Histogram_FPT.png", width = 800, height = 600)
hist(R_all[, "FPT"], breaks = 50, main = "Phân phối lợi nhuận FPT", col = "skyblue", xlab = "Log Return", border = "white")
dev.off()

# --- 4. CÂU 2B: LÝ THUYẾT DANH MỤC (MARKOWITZ) ---
# 1. Expected return vector, Covariance & Correlation matrix [cite: 57, 62]
print(ER_vector <- mu)
print(Sigma <- cov(R_all))
print(Corr_mat <- cor(R_all))

# 2. Xây dựng danh mục 2 mã (FPT & VCB) - Tìm MVP [cite: 116-117]
v1 <- Sigma["FPT", "FPT"]; v2 <- Sigma["VCB", "VCB"]; c12 <- Sigma["FPT", "VCB"]
w_fpt_mvp <- (v2 - c12) / (v1 + v2 - 2*c12)
w_vcb_mvp <- 1 - w_fpt_mvp

# 3. Danh mục 5 cổ phiếu tỷ trọng bằng nhau (w = 0.2) [cite: 136-138]
w5 <- rep(0.2, 5)
ERP5 <- sum(w5 * mu) # Lợi nhuận kỳ vọng
SDP5 <- sqrt(as.numeric(t(w5) %*% Sigma %*% w5)) # Rủi ro (sigma)
print(paste("LN kỳ vọng danh mục 5 mã:", round(ERP5, 6)))
print(paste("Rủi ro (Sigma) danh mục 5 mã:", round(SDP5, 6)))

# --- 5. CÂU 2C: MÔ HÌNH CAPM ---
# 1. Market Proxy & Excess Return
rf_annual <- 0.03
rf_daily <- rf_annual / 250
Rm <- rowMeans(R_all) # [cite: 265]D
FPT_excess <- R_all[, "FPT"] - rf_daily
Market_excess <- Rm - rf_daily

# 2. Tính Beta (2 cách) [cite: 275-281]
beta_way1 <- cov(FPT_excess, Market_excess) / var(Market_excess) # Cách 1: Công thức
model_fpt <- lm(FPT_excess ~ Market_excess) # Cách 2: Regression (OLS)
summary(model_fpt) # Ước lượng Alpha, Beta & Kiểm định Alpha=0

# 3. Vẽ đường SML [cite: 324-348]
beta_all <- apply(R_all, 2, function(x) cov(x - rf_daily, Market_excess) / var(Market_excess))
ER_annual <- colMeans(R_all) * 250
ERP_market <- mean(Rm) * 250 - rf_annual

png("SML_Chart.png", width = 800, height = 600)
plot(beta_all, ER_annual, pch = 16, col = "blue", xlab = "Beta", ylab = "Expected Return", main = "Security Market Line (SML)")
abline(a = rf_annual, b = ERP_market, col = "red", lwd = 2)
text(beta_all, ER_annual, labels = names(beta_all), pos = 4)
dev.off()
