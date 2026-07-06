import yfinance as yf
import pandas as pd
import numpy as np

def export_full_data_for_submission():
    print("--- Đang kéo dữ liệu gốc 2024-2026 cho anh Phú... ---")
    
    # 1. THIẾT LẬP DANH MỤC
    tickers = ["MBB.VN", "VNM.VN", "FPT.VN", "VIC.VN", "PLX.VN"]
    
    # 2. TẢI DỮ LIỆU GỐC (DAILY CLOSE)
    try:
        # Tải giá đóng cửa
        data = yf.download(tickers, start="2024-04-10", end="2026-04-10")['Close']
        
        # 3. TÍNH LOG RETURN (THEO YÊU CẦU CỦA ĐỀ)
        returns = np.log(data / data.shift(1)).dropna()
        
        # 4. XUẤT FILE EXCEL 2 SHEET (ĐÚNG CHUẨN THẦY LÂM)
        # Sheet 1: Giá đóng cửa hằng ngày (Raw Data)
        # Sheet 2: Tỷ suất sinh lời Log (Calculated Returns)
        file_name = "Du_Lieu_Goc_Phu_2024_2026.xlsx"
        
        with pd.ExcelWriter(file_name) as writer:
            data.to_excel(writer, sheet_name='1.Gia_Dong_Cua_Raw')
            returns.to_excel(writer, sheet_name='2.Log_Returns_Calculated')
            
        print(f"--- THÀNH CÔNG! Đã xuất file: {file_name} ---")
        print("Mày gửi file này kèm file Word cho anh Phú là đủ bộ nộp bài.")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    export_full_data_for_submission()