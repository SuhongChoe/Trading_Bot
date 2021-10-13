import numpy as np
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

predicted_close_price = 0
def predict_price(ticker, day):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60", to=day)
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
    return closeValue
predict_price("KRW-BTC",)

now = datetime.datetime.now()
start_time = get_start_time("KRW-BTC")
end_time = start_time + datetime.timedelta(days=1)
schedule.run_pending()
# 9:00 < 현재 < 8:59:50
if start_time < now < end_time - datetime.timedelta(seconds=10):
    target_price = get_target_price("KRW-BTC", 0.5)
    current_price = get_current_price("KRW-BTC")
    if target_price < current_price and current_price < predicted_close_price:
        krw = get_balance("KRW")
        if krw > 5000:
            upbit.buy_market_order("KRW-BTC", krw * 0.9995)
            post_message(myToken,"#crypto", "BTC buy : " +str(buy_result))
else:
    btc = get_balance("BTC")
    if btc > 0.00008:
        upbit.sell_market_order("KRW-BTC", btc*0.9995)
        post_message(myToken, "#crypto", "BTC buy : " + str(sell_result))








# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC", count=7)
print(df)

# 변동성 돌파 기준 범위 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

# range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# 수수료
fee = 0
# np.where(조건문, 참일떄 값, 거짓일떄 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 곱 계산(cumpord) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['dd'].max())
# 엑셀로 출력
df.to_csv("dd.csv")