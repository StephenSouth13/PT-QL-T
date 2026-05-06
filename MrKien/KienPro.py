import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# --- CẤU HÌNH HỆ THỐNG ---
plt.style.use('ggplot')
symbols = ["TCB.VN", "MWG.VN", "REE.VN", "GAS.VN", "HPG.VN"]
market_ticker = "^VNINDEX" 
start_date, end_date = "2024-04-10", "2026-04-10"

# --- 1. DOWNLOAD VÀ XỬ LÝ DỮ LIỆU ---
print("--- Đang tải dữ liệu từ HOSE... ---")
# Tải dữ liệu cổ phiếu
data = yf.download(symbols, start=start_date, end=end_date)['Close']
data = data.ffill().dropna()

# Tính Log Return cho 5 mã cổ phiếu
returns = np.log(data / data.shift(1)).dropna()
returns.columns = [s.replace('.VN', '') for s in symbols]

# --- XỬ LÝ LỖI VN-INDEX (MARKET PROXY) ---
print("--- Đang kiểm tra Market Proxy... ---")
try:
    vnindex = yf.download(market_ticker, start=start_date, end=end_date)['Close']
    if vnindex.empty or vnindex.isna().all().item():
        raise ValueError("VNINDEX rỗng")
    market_return = np.log(vnindex / vnindex.shift(1)).dropna()
    print(">>> Sử dụng dữ liệu VN-Index thực tế.")
except:
    print("!!! WARNING: ^VNINDEX không khả dụng. Đang tạo Market Proxy giả lập (Equally Weighted Index) !!!")
    # Tạo chỉ số thị trường bằng trung bình cộng log return của 5 mã
    market_return = returns.mean(axis=1)

# Đảm bảo index khớp nhau
common_index = returns.index.intersection(market_return.index)
returns = returns.loc[common_index]
market_return = market_return.loc[common_index]

# --- 2. CÂU 1: PHÂN TÍCH KỸ THUẬT (TCB) ---
tcb_raw = yf.download("TCB.VN", start=start_date, end=end_date)
tcb = tcb_raw.copy()
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
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
tcb['RSI'] = 100 - (100 / (1 + gain/loss))

fig, axes = plt.subplots(3, 1, figsize=(12, 15), gridspec_kw={'height_ratios': [3, 1, 1]})
axes[0].plot(tcb.index, tcb['Close'], color='black', label='Price')
axes[0].plot(tcb.index, tcb['SMA20'], label='SMA20', ls='--')
axes[0].fill_between(tcb.index, tcb['Lower'], tcb['Upper'], color='gray', alpha=0.2, label='Bollinger')
axes[0].set_title("TCB Technical Profile (SMA, BBands)", weight='bold'); axes[0].legend()
axes[1].plot(tcb.index, tcb['MACD'], label='MACD'); axes[1].plot(tcb.index, tcb['Signal'], label='Signal')
axes[1].set_title("MACD Momentum"); axes[1].legend()
axes[2].plot(tcb.index, tcb['RSI'], color='purple'); axes[2].axhline(70, color='red', ls='--')
axes[2].axhline(30, color='green', ls='--'); axes[2].set_title("RSI Strength")
plt.tight_layout(); plt.savefig("1_PTKT_TCB.png", dpi=300)

# --- 3. CÂU 2A: THỐNG KÊ & HISTOGRAM (SỬA LẠI ĐỂ KHÔNG BỊ KEYERROR) ---
stats_df = pd.DataFrame({
    'Mean': returns.mean(), 
    'SD': returns.std(), 
    'Variance': returns.var(),
    'Skewness': returns.skew(), 
    'Kurtosis': returns.kurt() # BỎ DẤU .T Ở ĐÂY
})
# Bây giờ Ticker sẽ là Index (hàng), còn các chỉ số sẽ là Columns (cột). Đúng chuẩn!

plt.figure(figsize=(15, 10))
for i, col in enumerate(returns.columns):
    plt.subplot(2, 3, i+1)
    sns.histplot(returns[col], kde=True, color='skyblue')
    plt.title(f"Distribution: {col}")
plt.tight_layout(); plt.savefig("2_Histograms.png", dpi=300)

# --- 4. CÂU 2B: MARKOWITZ ---
cov_matrix = returns.cov()
corr_matrix = returns.corr()
plt.figure(figsize=(10, 8)); sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn'); plt.title("Correlation Matrix")
plt.savefig("3_Correlation.png", dpi=300)

# MVP TCB & MWG
v1, v2 = cov_matrix.loc['TCB','TCB'], cov_matrix.loc['MWG','MWG']
c12 = cov_matrix.loc['TCB','MWG']
w_tcb_mvp = (v2 - c12) / (v1 + v2 - 2*c12)

# --- 5. CÂU 2C: CAPM ---
rf_daily = 0.03 / 250
capm_results = []
for col in returns.columns:
    X = sm.add_constant(market_return - rf_daily)
    model = sm.OLS(returns[col] - rf_daily, X).fit()
    # Beta Covariance (Cách 1)
    b_cov = np.cov(returns[col], market_return)[0,1] / np.var(market_return)
    capm_results.append([model.params.iloc[0], model.params.iloc[1], b_cov, model.pvalues.iloc[0]])

capm_df = pd.DataFrame(capm_results, index=returns.columns, 
                       columns=['Alpha', 'Beta_OLS', 'Beta_Cov', 'P_Value_Alpha'])

# Vẽ SML
plt.figure(figsize=(10, 6))
betas = capm_df['Beta_OLS']
rets = returns.mean() * 250
plt.scatter(betas, rets, color='red', s=100)
for i, txt in enumerate(returns.columns):
    plt.annotate(txt, (betas.iloc[i], rets.iloc[i]), xytext=(5,5), textcoords='offset points')
x_line = np.linspace(0, 2, 100)
y_line = 0.03 + x_line * (market_return.mean()*250 - 0.03)
plt.plot(x_line, y_line, color='blue', label='Security Market Line (SML)')
plt.xlabel("Beta"); plt.ylabel("Expected Return (Ann)"); plt.legend()
plt.savefig("4_SML.png", dpi=300)

# EXPORT EXCEL
with pd.ExcelWriter("Bao_cao_Kien_Pro.xlsx") as writer:
    returns.to_excel(writer, sheet_name='Log_Returns')
    stats_df.to_excel(writer, sheet_name='Summary_Stats')
    capm_df.to_excel(writer, sheet_name='CAPM_Analysis')
print("--- Pipeline HOÀN TẤT! ---")