import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf # Mày cài bằng lệnh: pip install yfinance

# --- 1. DATA INGESTION & PRE-PROCESSING ---
symbols = ["FPT.VN", "VCB.VN", "HPG.VN", "VNM.VN", "MSN.VN"]
print("--- Đang kéo dữ liệu từ Yahoo Finance... ---")
df = yf.download(symbols, start="2024-04-10", end="2026-04-10")['Close']

# Tính Log-return (Chuẩn hóa Stationarity)
returns = np.log(df / df.shift(1)).dropna()
returns.columns = [s.replace('.VN', '') for s in symbols]

# --- 2. THỐNG KÊ ĐỊNH LƯỢNG ---
stats = pd.DataFrame({
    'Mean': returns.mean(),
    'SD': returns.std(),
    'Variance': returns.var(),
    'Skewness': returns.skew(),
    'Excess_Kurtosis': returns.kurtosis()
})

# Xuất CSV chuẩn cho báo cáo
stats.to_csv("Bao_cao_Thong_ke_Python.csv")
print("\n--- Bảng thống kê mô tả ---")
print(stats)

# --- 3. PHÂN TÍCH ĐỐI CHIẾU (SYSTEMIC ANALYSIS) ---
plt.style.use('seaborn-v0_8-whitegrid') # Dùng style chuyên nghiệp
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Subplot 1: Risk-Return Scatter Plot
annual_mean = stats['Mean'] * 250
annual_sd = stats['SD'] * np.sqrt(250)

ax[0].scatter(annual_sd, annual_mean, color='#1f77b4', s=150, edgecolors='black', alpha=0.8)
for i, txt in enumerate(stats.index):
    ax[0].annotate(txt, (annual_sd.iloc[i], annual_mean.iloc[i]), xytext=(8, 8), textcoords='offset points', fontsize=12, weight='bold')

ax[0].set_title("Ma trận Risk-Return (Annualized)", fontsize=14, weight='bold')
ax[0].set_xlabel("Rủi ro (Annualized Volatility)", fontsize=12)
ax[0].set_ylabel("Lợi nhuận kỳ vọng (Annualized Mean)", fontsize=12)

# Subplot 2: Correlation Heatmap (Khai thác ma trận tương quan)
sns.heatmap(returns.corr(), annot=True, cmap='RdYlGn', fmt=".2f", ax=ax[1], linewidths=0.5)
ax[1].set_title("Ma trận tương quan giữa các Node chiến lược", fontsize=14, weight='bold')

plt.tight_layout()
plt.savefig("Analysis_Python_Results.png", dpi=300)
plt.show()

print("\n--- Hoàn tất! Ảnh và file CSV đã sẵn sàng để dán vào luận văn. ---")