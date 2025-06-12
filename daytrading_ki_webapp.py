import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Krypto Daytrading KI", layout="centered")

st.title("📈 Krypto Daytrading KI – 5-Minuten Signale")
st.markdown("Dieses Tool zeigt dir die aktuellen **Kauf-/Verkaufssignale** mit Hebel, Stop-Loss und Take-Profit für BTC/USD.")

df = yf.download("BTC-USD", interval="5m", period="5d")
df.dropna(inplace=True)

rsi = ta.momentum.RSIIndicator(close=df['Close'], window=14)
df['rsi'] = rsi.rsi().fillna(0)
df['ema_fast'] = ta.trend.EMAIndicator(close=df['Close'], window=9).ema_indicator()
df['ema_slow'] = ta.trend.EMAIndicator(close=df['Close'], window=21).ema_indicator()
macd = ta.trend.MACD(close=df['Close'])
df['macd'] = macd.macd_diff()

def generate_signal(row):
    if row['rsi'] < 30 and row['ema_fast'] > row['ema_slow'] and row['macd'] > 0:
        return 'BUY'
    elif row['rsi'] > 70 and row['ema_fast'] < row['ema_slow'] and row['macd'] < 0:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(generate_signal, axis=1)

def get_trade_info(signal):
    if signal in ['BUY', 'SELL']:
        return {'Leverage': '5x', 'Stop-Loss': '-1.5%', 'Take-Profit': '+3%'}
    return {'Leverage': '-', 'Stop-Loss': '-', 'Take-Profit': '-'}

last = df.iloc[-1]
info = get_trade_info(last['signal'])

st.subheader("📊 Letztes Signal:")
st.metric("Signal", last['signal'])
st.metric("Kurs", f"${last['Close']:.2f}")
st.metric("Hebel", info['Leverage'])
st.metric("Stop-Loss", info['Stop-Loss'])
st.metric("Take-Profit", info['Take-Profit'])

st.caption("BTC/USD – 5-Minuten-Kerzen – nur Demo")
