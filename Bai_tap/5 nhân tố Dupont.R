# Nhập số liệu thực tế bạn vừa nhặt (Ví dụ số giả định dưới đây)
tax_burden <- 12100 / 13500      # Net Income / EBT
interest_burden <- 13500 / 18000 # EBT / EBIT
ebit_margin <- 18000 / 120000    # EBIT / Revenue
asset_turnover <- 120000 / 180000 # Revenue / Total Assets
leverage <- 180000 / 100000      # Total Assets / Equity

roe <- tax_burden * interest_burden * ebit_margin * asset_turnover * leverage
cat("ROE tính theo Dupont 5 nhân tố là:", round(roe * 100, 2), "%")