library(readxl)
library(dplyr)

# Thử với .xlsx
df <- read_excel("D:/UEH/PT-QL-T/Buoi_2/stock_prices.xlsx", sheet = "Prices")
# 2) Đảm bảo Date là Date và sắp theo thời gian
df <- df %>%
  mutate(Date = as.Date(Date)) %>%
  arrange(Date)

# 3) Tính return từ Close
df <- df %>%
  mutate(
    ret_close = Close / lag(Close) - 1,          # simple return
    logret_close = log(Close / lag(Close))       # log return
  )

# 4) Xem kết quả
head(df, 10)
summary(df$ret_close)

