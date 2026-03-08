import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from vnstock import Vnstock
from scipy.stats import skew, kurtosis, jarque_bera

# 1. THIẾT LẬP THÔNG SỐ
SYMBOL = "HPG"
MARKET = "VNINDEX"
START = "2020-01-01"
END = "2025-03-08"

def run_ueh_project():
    try:
        # Khởi tạo Vnstock V3
        stock_api = Vnstock().stock(symbol=SYMBOL, source="VCI")
        market_api = Vnstock().stock(symbol=MARKET, source="VCI")

        print(f"--- Đang tải dữ liệu {SYMBOL} và {MARKET} từ {START} ---")
        
        # Tải dữ liệu
        df_hpg = stock_api.quote.history(start=START, end=END, interval="1D")
        df_vni = market_api.quote.history(start=START, end=END, interval="1D")

        # 2. MERGE DỮ LIỆU & TÍNH RETURN (Xử lý lỗi lệch ngày)
        df_hpg = df_hpg[['time', 'close']].rename(columns={'close': 'close_hpg'})
        df_vni = df_vni[['time', 'close']].rename(columns={'close': 'close_vni'})
        
        df_final = pd.merge(df_hpg, df_vni, on='time', how='inner').sort_values('time')
        
        # TSL Log (UEH thường yêu cầu Log Return)
        df_final['R_hpg'] = np.log(df_final['close_hpg'] / df_final['close_hpg'].shift(1))
        df_final['R_vni'] = np.log(df_final['close_vni'] / df_final['close_vni'].shift(1))
        df_final = df_final.dropna()

        # 3. THỐNG KÊ MÔ TẢ (Mean, Sigma, Skew, Kurt, JB)
        R = df_final['R_hpg']
        mu = R.mean()
        sigma = R.std()
        sk = skew(R)
        kur = kurtosis(R)
        jb_stat, p_val = jarque_bera(R)

        # 4. TÍNH BETA (Regression)
        beta = df_final['R_hpg'].cov(df_final['R_vni']) / df_final['R_vni'].var()

        # In kết quả cho Báo cáo Word
        print("\n" + "="*40)
        print(f"KẾT QUẢ PHÂN TÍCH ĐỊNH LƯỢNG HPG")
        print("="*40)
        print(f"1. TSL Trung bình (Mean): {mu:.6f}")
        print(f"2. Rủi ro (Sigma):        {sigma:.6f}")
        print(f"3. Hệ số Beta:           {beta:.4f}")
        print(f"4. Độ xiên (Skewness):    {sk:.4f}")
        print(f"5. Độ nhọn (Kurtosis):    {kur:.4f}")
        print(f"6. Kiểm định JB (p-val):  {p_val:.6f}")
        print("="*40)

        # 5. XUẤT FILE BIỂU ĐỒ (PNG)
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Biểu đồ 1: Giá và TSL
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(df_final['time'], df_final['close_hpg'], color='#005595', label='Giá HPG')
        ax1.set_ylabel('Giá (VNĐ)', fontweight='bold')
        ax2 = ax1.twinx()
        ax2.bar(df_final['time'], df_final['R_hpg'], color='red', alpha=0.3, label='Log Return')
        plt.title(f'BIẾN ĐỘNG GIÁ VÀ TSL HPG (GIAI ĐOẠN 2020-2025)', fontsize=14, fontweight='bold')
        plt.savefig('HPG_Price_Return.png', dpi=300)

        # Biểu đồ 2: Histogram & QQ
        plt.figure(figsize=(10, 6))
        sns.histplot(R, kde=True, color='#005595', bins=50)
        plt.title('PHÂN PHỐI TỶ SUẤT SINH LỜI HPG', fontweight='bold')
        plt.savefig('HPG_Distribution.png', dpi=300)

        # Biểu đồ 3: Hồi quy CAPM (SML)
        plt.figure(figsize=(8, 6))
        sns.regplot(x='R_vni', y='R_hpg', data=df_final, scatter_kws={'alpha':0.3, 's':10}, line_kws={'color':'red'})
        plt.title(f'HỒI QUY TUYẾN TÍNH HPG vs VN-INDEX (BETA = {beta:.2f})', fontweight='bold')
        plt.savefig('HPG_CAPM_Regression.png', dpi=300)

        # 6. XUẤT DATABASE CSV
        df_final.to_csv("Database_HPG_UEH.csv", index=False)
        print("\n--> ĐÃ XUẤT THÀNH CÔNG DATABASE VÀ 3 BIỂU ĐỒ PNG.")

    except Exception as e:
        print(f"Lỗi: {e}. Hãy thử lệnh 'pip install -U vnstock' trước khi chạy lại.")

if __name__ == "__main__":
    run_ueh_project()