import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Krypto Daytrading KI", layout="wide")
st.title("📉 Krypto Daytrading KI – 5-Minuten Signale")
st.markdown("Dieses Tool zeigt dir Kauf-/Verkaufssignale für BTC/USD basierend auf RSI und EMA.")

# Daten laden
df = yf.download("BTC-USD", interval="5m", period="1d")
df.dropna(inplace=True)

# Technische Indikatoren berechnen
df['rsi'] = ta.momentum.RSIIndicator(close=df['Close']).rsi()
df['ema_fast'] = ta.trend.EMAIndicator(close=df['Close'], window=9).ema_indicator()
df['ema_slow'] = ta.trend.EMAIndicator(close=df['Close'], window=21).ema_indicator()

# Signal erzeugen
def generate_signal(row):
    if row['rsi'] < 30 and row['ema_fast'] > row['ema_slow']:
        return 'BUY'
    elif row['rsi'] > 70 and row['ema_fast'] < row['ema_slow']:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(generate_signal, axis=1)

# Anzeige
st.dataframe(df[['Close', 'rsi', 'ema_fast', 'ema_slow', 'signal']].tail(20))
