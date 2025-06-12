import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Krypto Daytrading KI", layout="centered")

st.title("📉 Krypto Daytrading KI – 5-Minuten Signale")
st.markdown("Dieses Tool zeigt dir Kauf-/Verkaufssignale für BTC/USD basierend auf RSI und EMA.")

# Daten abrufen
df = yf.download("BTC-USD", interval="5m", period="1d")
df.dropna(inplace=True)

# Indikatoren berechnen
df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
df['ema_fast'] = ta.trend.EMAIndicator(df['Close'], window=12).ema_indicator()
df['ema_slow'] = ta.trend.EMAIndicator(df['Close'], window=26).ema_indicator()
df['macd'] = ta.trend.MACD(df['Close']).macd_diff()

# Handelssignal generieren
def signal(row):
    if row['rsi'] < 30 and row['ema_fast'] > row['ema_slow']:
        return "KAUF"
    elif row['rsi'] > 70 and row['ema_fast'] < row['ema_slow']:
        return "VERKAUF"
    else:
        return "HALTEN"

df['Signal'] = df.apply(signal, axis=1)

# Letztes Signal anzeigen
st.subheader("Letztes Signal:")
st.metric(label="Signal", value=df['Signal'].iloc[-1])

# Chart anzeigen
st.line_chart(df[['Close', 'ema_fast', 'ema_slow']])
