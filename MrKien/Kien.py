import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
import statsmodels.api as sm

# --- CONFIGURATION ---
plt.style.use('seaborn-v0_8-whitegrid')
symbols = ["TCB.VN", "MWG.VN", "REE.VN", "GAS.VN", "HPG.VN"]
start_date, end_date = "2024-04-10", "2026-04-10"

# --- 1. DATA INGESTION ---
print("--- Downloading Data from HOSE... ---")
df = yf.download(symbols, start=start_date, end=end_date)['Close']
returns = np.log(df / df.shift(1)).dropna()
returns.columns = [s.replace('.VN', '') for s in symbols]

# --- 2. CÂU 1: TECHNICAL ANALYSIS (TCB) ---
tcb = yf.download("TCB.VN", start=start_date, end=end_date).copy()
tcb['SMA5'] = tcb['Close'].rolling(5).mean()
tcb['SMA20'] = tcb['Close'].rolling(20).mean()
tcb['STD20'] = tcb['Close'].rolling(20).std()
tcb['Upper'] = tcb['SMA20'] + (tcb['STD20'] * 2)
tcb['Lower'] = tcb['SMA20'] - (tcb['STD20'] * 2)

# MACD
exp1 = tcb['Close'].ewm(span=12, adjust=False).mean()
exp2 = tcb['Close'].ewm(span=26, adjust=False).mean()
tcb['MACD'] = exp1 - exp2
tcb['Signal'] = tcb['MACD'].ewm(span=9, adjust=False).mean()

# RSI
delta = tcb['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
tcb['RSI'] = 100 - (100 / (1 + rs))

# Vẽ đồ thị Câu 1
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
ax1.plot(tcb.index, tcb['Close'], label='Price', color='black')
ax1.plot(tcb.index, tcb['SMA5'], label='SMA 5', ls='--')
ax1.plot(tcb.index, tcb['SMA20'], label='SMA 20', lw=2)
ax1.fill_between(tcb.index, tcb['Lower'], tcb['Upper'], alpha=0.1, label='BB (20,2)')
ax1.set_title("TCB Technical Analysis Profile", weight='bold')
ax1.legend()

ax2.plot(tcb.index, tcb['MACD'], label='MACD')
ax2.plot(tcb.index, tcb['Signal'], label='Signal')
ax2.axhline(0, color='gray', ls='--')
ax2.set_title("MACD (12,26,9)")

ax3.plot(tcb.index, tcb['RSI'], label='RSI', color='purple')
ax3.axhline(70, color='red', ls='--')
ax3.axhline(30, color='green', ls='--')
ax3.set_title("RSI (14)")
plt.tight_layout()
plt.savefig("Q1_PTKT_TCB.png", dpi=300)

# --- 3. CÂU 2A: THỐNG KÊ MÔ TẢ ---
stats = pd.DataFrame({
    'Mean': returns.mean(),
    'SD': returns.std(),
    'Variance': returns.var(),
    'Skewness': returns.apply(skew),
    'Kurtosis': returns.apply(kurtosis)
}).T

# Histogram TCB
plt.figure(figsize=(8,6))
sns.histplot(returns['TCB'], kde=True, color='orange')
plt.title("Histogram of TCB Returns")
plt.savefig("Q2A_Histogram.png", dpi=300)

# --- 4. CÂU 2B: MARKOWITZ ---
cov_mat = returns.cov()
# Danh mục 5 mã tỷ trọng bằng nhau (w=0.2)
w5 = np.array([0.2] * 5)
rp5 = np.sum(returns.mean() * w5)
sp5 = np.sqrt(np.dot(w5.T, np.dot(cov_mat, w5)))

# MVP 2 mã TCB-MWG
v1, v2 = cov_mat.loc['TCB','TCB'], cov_mat.loc['MWG','MWG']
c12 = cov_mat.loc['TCB','MWG']
w_tcb_mvp = (v2 - c12) / (v1 + v2 - 2*c12)

# --- 5. CÂU 2C: CAPM ---
rf_daily = 0.03 / 250
market = returns.mean(axis=1) # Market Proxy (VNIndex Proxy)
X = sm.add_constant(market - rf_daily)
model = sm.OLS(returns['TCB'] - rf_daily, X).fit()

# Dùng iloc để tránh KeyError
alpha = model.params.iloc[0]
beta_ols = model.params.iloc[1]
p_alpha = model.pvalues.iloc[0]

# Vẽ SML
betas = [np.cov(returns[s]-rf_daily, market-rf_daily)[0,1]/np.var(market-rf_daily) for s in returns.columns]
plt.figure(figsize=(10,6))
plt.scatter(betas, returns.mean()*250, color='blue', s=100)
for i, s in enumerate(returns.columns):
    plt.annotate(s, (betas[i], returns.mean().iloc[i]*250), xytext=(5,5), textcoords='offset points', weight='bold')
# Đường SML lý thuyết
x_range = np.linspace(0, 1.5, 100)
y_range = 0.03 + x_range * (market.mean()*250 - 0.03)
plt.plot(x_range, y_range, color='red', label='Security Market Line (SML)', lw=2)
plt.xlabel("Beta"); plt.ylabel("Expected Return (Annualized)")
plt.legend(); plt.savefig("Q2C_SML.png", dpi=300)

# EXPORT EXCEL
with pd.ExcelWriter("Bao_cao_MrKien.xlsx") as writer:
    returns.to_excel(writer, sheet_name='Log_Returns')
    stats.to_excel(writer, sheet_name='Stats')
    pd.DataFrame({
        'Metric': ['5-stock Port Return', '5-stock Port Risk', 'TCB-MWG MVP Weight (TCB)', 'TCB Beta (OLS)', 'TCB Alpha p-value'],
        'Value': [rp5, sp5, w_tcb_mvp, beta_ols, p_alpha]
    }).to_excel(writer, sheet_name='Summary_Results')

print("--- Pipeline Completed Successfully! ---")