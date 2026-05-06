import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập phong cách hiển thị chuyên nghiệp
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def run_quantitative_analysis():
    print("--- Đang khởi tạo Pipeline phân tích cho khách hàng Phú... ---")
    
    # 1. DANH MỤC CỔ PHIẾU (Đã đổi mã so với bài cũ)
    tickers = ["MBB.VN", "VNM.VN", "FPT.VN", "VIC.VN", "PLX.VN"]
    names = ["MBB", "VNM", "FPT", "VIC", "PLX"]
    
    # 2. TẢI DỮ LIỆU THỰC TẾ TỪ YAHOO FINANCE
    # Lấy dữ liệu 2 năm gần nhất để tính toán Beta và lợi nhuận kỳ vọng
    try:
        raw_data = yf.download(tickers, start="2024-04-10", end="2026-04-10")['Close']
        returns = np.log(raw_data / raw_data.shift(1)).dropna()
        print("--- Tải dữ liệu thành công! ---")
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu: {e}")
        return

    # 3. TÍNH TOÁN MARKET PROXY (Equally Weighted Index)
    # Vì VNINDEX hay lỗi, ta dùng trung bình danh mục làm benchmark
    market_return = returns.mean(axis=1)

    # 4. XUẤT FILE EXCEL SỐ LIỆU (BẰNG CHỨNG ĐỊNH LƯỢNG)
    stats = pd.DataFrame({
        'Lợi nhuận TB năm': returns.mean() * 250,
        'Rủi ro (Độ lệch chuẩn)': returns.std() * np.sqrt(250),
        'Hệ số nhọn (Kurtosis)': returns.kurt(),
        'Hệ số bất đối xứng (Skewness)': returns.skew()
    })
    
    with pd.ExcelWriter("Ket_Qua_Dinh_Luong_Phu.xlsx") as writer:
        stats.to_excel(writer, sheet_name='ThongKe_MoTa')
        returns.corr().to_excel(writer, sheet_name='MaTran_TuongQuan')
    print("--- Đã xuất file: Ket_Qua_Dinh_Luong_Phu.xlsx ---")

    # 5. VẼ BIỂU ĐỒ PHỤ LỤC
    
    # Hình 1: Diễn biến giá MBB (Đại diện PTKT)
    plt.figure()
    raw_data['MBB.VN'].plot(color='#1f77b4', lw=2)
    plt.title("HÌNH 1: DIỄN BIẾN GIÁ CỔ PHIẾU MBB (2024-2026)", fontsize=14)
    plt.ylabel("Giá đóng cửa (VND)")
    plt.savefig("Hinh1_PTKT_MBB.png")
    
    # Hình 2: Phân phối lợi nhuận FPT (Kiểm định tính chuẩn)
    plt.figure()
    sns.histplot(returns['FPT.VN'], kde=True, color='#2ca02c', bins=50)
    plt.title("HÌNH 2: PHÂN PHỐI LỢI NHUẬN CỔ PHIẾU FPT", fontsize=14)
    plt.xlabel("Tỷ suất sinh lời ngày")
    plt.savefig("Hinh2_Dist_FPT.png")
    
    # Hình 3: Ma trận tương quan (Hiệu ứng Markowitz)
    plt.figure(figsize=(10, 8))
    sns.heatmap(returns.corr(), annot=True, cmap='RdYlGn', fmt=".2f", center=0)
    plt.title("HÌNH 3: MA TRẬN TƯƠNG QUAN DANH MỤC", fontsize=14)
    plt.savefig("Hinh3_Heatmap.png")
    
    # Hình 4: Đường biên SML (Mô hình CAPM)
    betas = []
    for ticker in raw_data.columns:
        cov_matrix = np.cov(returns[ticker], market_return)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1]
        betas.append(beta)
    
    exp_ret = returns.mean() * 250
    plt.figure()
    plt.scatter(betas, exp_ret, color='red', s=100)
    
    # Fix lỗi annotate dùng Label thay vì Index
    for i, ticker in enumerate(raw_data.columns):
        plt.annotate(ticker.replace('.VN',''), (betas[i], exp_ret.iloc[i]), 
                     xytext=(5,5), textcoords='offset points', fontsize=12)
    
    # Vẽ đường SML giả định (Rf = 3%, Rm = Lợi nhuận TB thị trường)
    rf = 0.03
    rm = market_return.mean() * 250
    x_sml = np.array([0, 2])
    y_sml = rf + x_sml * (rm - rf)
    plt.plot(x_sml, y_sml, color='black', linestyle='--', label='Security Market Line (SML)')
    
    plt.title("HÌNH 4: ĐƯỜNG BIÊN THỊ TRƯỜNG CHỨNG KHOÁN SML", fontsize=14)
    plt.xlabel("Hệ số Beta (Rủi ro hệ thống)")
    plt.ylabel("Lợi nhuận kỳ vọng (Năm)")
    plt.legend()
    plt.savefig("Hinh4_CAPM_SML.png")
    
    print("--- HOÀN TẤT! 4 ẢNH VÀ 1 FILE EXCEL ĐÃ SẴN SÀNG ---")

if __name__ == "__main__":
    run_quantitative_analysis()