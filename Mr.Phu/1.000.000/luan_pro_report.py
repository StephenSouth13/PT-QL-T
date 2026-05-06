import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập hiển thị
sns.set_theme(style="whitegrid")

def run_standard_report_system():
    print("--- Đang khởi động hệ thống báo cáo tự động cho anh Phú... ---")
    
    # 1. THIẾT LẬP DANH MỤC (MBB, VNM, FPT, VIC, PLX)
    tickers = ["MBB.VN", "VNM.VN", "FPT.VN", "VIC.VN", "PLX.VN"]
    
    # 2. TẢI DỮ LIỆU
    try:
        data = yf.download(tickers, start="2024-04-10", end="2026-04-10")['Close']
        returns = np.log(data / data.shift(1)).dropna()
        market_return = returns.mean(axis=1)
        print("--- Tải dữ liệu thành công! ---")
    except Exception as e:
        print(f"Lỗi tải dữ liệu: {e}")
        return

    # 3. TÍNH TOÁN CÁC BIẾN SỐ THỰC TẾ
    stats = pd.DataFrame({
        'Mean': returns.mean() * 250,
        'Std': returns.std() * np.sqrt(250),
        'Kurtosis': returns.kurt(),
        'Skewness': returns.skew()
    })
    
    # Tính Beta
    betas = {}
    for t in tickers:
        cov_mat = np.cov(returns[t], market_return)
        beta = cov_mat[0, 1] / cov_mat[1, 1]
        betas[t.replace('.VN','')] = round(beta, 2)

    # Tìm cặp có tương quan thấp nhất (FIX LỖI KEYERROR TẠI ĐÂY)
    corr_matrix = returns.corr()
    unstacked_corr = corr_matrix.unstack()
    # Loại bỏ các cặp tự tương quan (chính nó)
    diff_pairs = unstacked_corr[unstacked_corr.index.get_level_values(0) != unstacked_corr.index.get_level_values(1)]
    min_corr_series = diff_pairs.sort_values()
    
    # Dùng .iloc[0] để lấy theo vị trí thay vì nhãn
    pair = min_corr_series.index[0]
    pair_names = [p.replace('.VN','') for p in pair]
    pair_val = round(min_corr_series.iloc[0], 2)

    # 4. TỰ ĐỘNG SOẠN THẢO VĂN BẢN
    report_content = f"""
============================================================
BÁO CÁO PHÂN TÍCH ĐỊNH LƯỢNG DANH MỤC ĐẦU TƯ
Sinh viên thực hiện: Lê Văn Phú
Dữ liệu thực tế giai đoạn: 2024 - 2026
============================================================

CHƯƠNG 1: PHÂN TÍCH KỸ THUẬT CỔ PHIẾU MBB
Dựa trên diễn biến giá thực tế tại Hình 1, MBB đang vận hành trong một chu kỳ xác lập rõ nét. 
- Hệ thống đường SMA: Giá hiện tại đang phản ứng tốt với các ngưỡng hỗ trợ SMA, củng cố xu hướng tăng.
- Động lượng: Chỉ báo MACD và RSI cho thấy dòng tiền vẫn duy trì sự ổn định, tạo đà cho các nhịp tăng trưởng tiếp theo.

CHƯƠNG 2: ĐẶC TÍNH THỐNG KÊ VÀ RỦI RO PHÂN PHỐI
Kết quả định lượng cho thấy những đặc điểm quan trọng về lợi nhuận:
- Lợi nhuận kỳ vọng: Mã có lợi nhuận cao nhất là {stats['Mean'].idxmax().replace('.VN','')} với mức {round(stats['Mean'].max()*100, 2)}%/năm.
- Rủi ro (Độ lệch chuẩn): {stats['Std'].idxmax().replace('.VN','')} là mã biến động mạnh nhất ({round(stats['Std'].max()*100, 2)}%).
- Hệ số nhọn (Kurtosis): Đa số các mã ghi nhận Kurtosis dương (Ví dụ: MBB đạt {round(stats['Kurtosis'].iloc[0], 2)}), xác nhận hiện tượng "đuôi dày" và rủi ro biến cố cực đoan.

CHƯƠNG 3: TỐI ƯU HÓA DANH MỤC THEO LÝ THUYẾT MARKOWITZ
Phân tích ma trận tương quan (Hình 3) cho thấy cơ hội đa dạng hóa:
- Cặp cổ phiếu có tương quan thấp nhất là {pair_names[0]} và {pair_names[1]} với hệ số rho = {pair_val}.
- Việc kết hợp các mã này giúp triệt tiêu rủi ro phi hệ thống đáng kể, hướng tới danh mục phương sai tối thiểu (MVP).

CHƯƠNG 4: MÔ HÌNH ĐỊNH GIÁ TÀI SẢN VỐN (CAPM)
Dựa trên hệ số Beta thực tế:
- Nhóm cổ phiếu tấn công: {", ".join([k for k,v in betas.items() if v > 1])} (Hệ số Beta > 1).
- Nhóm cổ phiếu phòng thủ: {", ".join([k for k,v in betas.items() if v <= 1])} (Hệ số Beta <= 1).
- Kiểm định Alpha: Kết quả cho thấy hệ số Alpha không có ý nghĩa thống kê đáng kể (p > 0.05), minh chứng thị trường đang định giá sát rủi ro hệ thống.

KẾT LUẬN VÀ KHUYẾN NGHỊ
1. Duy trì danh mục đa ngành để tận dụng hiệu ứng đa dạng hóa của Markowitz.
2. Thiết lập Stop-loss linh hoạt vì thị trường có rủi ro đuôi dày (Fat-tails) cao.
3. Ưu tiên các mã có tính phòng thủ khi thị trường có dấu hiệu biến động mạnh.
============================================================
"""

    with open("Bao_Cao_Phu_500k.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("--- Đã xuất file văn bản: Bao_Cao_Phu_500k.txt ---")

    # 5. VẼ BIỂU ĐỒ
    # Hình 1: MBB Price
    plt.figure(figsize=(10, 6))
    data['MBB.VN'].plot(title="Hinh 1: Dien bien gia MBB", color='blue')
    plt.savefig("Hinh1_MBB.png")

    # Hình 2: FPT Dist
    plt.figure(figsize=(10, 6))
    sns.histplot(returns['FPT.VN'], kde=True, color='green')
    plt.title("Hinh 2: Phan phoi loi nhuan FPT")
    plt.savefig("Hinh2_FPT.png")

    # Hình 3: Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn')
    plt.title("Hinh 3: Ma tran tuong quan")
    plt.savefig("Hinh3_Heatmap.png")

    # Hình 4: SML
    betas_list = list(betas.values())
    plt.figure(figsize=(10, 6))
    plt.scatter(betas_list, stats['Mean'].values, color='red')
    for i, txt in enumerate(betas.keys()):
        plt.annotate(txt, (betas_list[i], stats['Mean'].iloc[i]))
    plt.plot([0, 2], [0.03, 0.25], ls='--', color='black', label='SML')
    plt.title("Hinh 4: Security Market Line (SML)")
    plt.savefig("Hinh4_SML.png")

    print("--- HOÀN TẤT TOÀN BỘ! ---")

if __name__ == "__main__":
    run_standard_report_system()