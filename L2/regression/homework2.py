import matplotlib.pyplot as plt
import pandas as pd
import datetime, os, warnings
from pandas_datareader.data import DataReader
# warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #可以显示负号
# 设置起始时间
start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,12,31)


def load_data(*func_codes):
    datas=[]
    for code in func_codes:
        if os.path.exists(f"{code}.csv"):
            data=pd.read_csv(f"{code}.csv")
        else:
            data = DataReader(f"{code}.SZ", "yahoo", start, end)
            data.to_csv(f'{code}.csv')
        datas.append(data)

    return datas

datas=load_data("000001", "300005")

data_ss, data_tlz = datas[0], datas[1]

print(data_ss.head())
print(data_tlz.head())

# 探路者与上证综指
close_ss = data_ss["Close"]
close_tlz = data_tlz["Close"]

# 将探路者与上证综指进行数据合并
stock = pd.merge(data_ss, data_tlz, left_index = True, right_index = True)
stock = stock[["Close_x","Close_y"]]
stock.columns = ["上证综指","探路者"]

# 统计每日收益率
daily_return = (stock.diff()/stock.shift(periods = 1)).dropna()
print(daily_return.head())


# 每日收益率可视化
fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(15,6))
daily_return["上证综指"].plot(ax=ax[0])
ax[0].set_title("上证综指")
daily_return["探路者"].plot(ax=ax[1])
ax[1].set_title("探路者")
plt.show()


# 散点图
fig,ax = plt.subplots(nrows=1,ncols=1,figsize=(12,6))
plt.scatter(daily_return["探路者"],daily_return["上证综指"])
plt.title("每日收益率散点图 from 探路者 & 上证综指")
plt.show()

# 回归分析
import statsmodels.api as sm
# 加入截距项
daily_return["intercept"]=1.0
model = sm.OLS(daily_return["探路者"],daily_return[["上证综指","intercept"]])
results = model.fit()
print(results.summary())






