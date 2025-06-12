import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Krypto Daytrading KI – 5-Minuten Signale")

st.title("📉 Krypto Daytrading KI – 5-Minuten Signale")
st.markdown("Dieses Tool zeigt dir Kauf-/Verkaufssignale für BTC/USD basierend auf RSI und EMA.")

# Daten abrufen
df = yf.download("BTC-USD", interval="5m", period="1d")
df.dropna(inplace=True)

# RSI & EMA berechnen
df['rsi'] = ta.momentum.RSIIndicator(close=df['Close']).rsi()
df['ema_fast'] = ta.trend.EMAIndicator(close=df['Close'], window=9).ema_indicator()
df['ema_slow'] = ta.trend.EMAIndicator(close=df['Close'], window=21).ema_indicator()

# Signal-Logik
def generate_signal(row):
    if row['rsi'] < 30 and row['ema_fast'] > row['ema_slow']:
        return 'BUY'
    elif row['rsi'] > 70 and row['ema_fast'] < row['ema_slow']:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(generate_signal, axis=1)

# Letztes Signal anzeigen
st.subheader("Aktuelles Signal")
st.write(df[['Close', 'rsi', 'ema_fast', 'ema_slow', 'signal']].tail(1))

# Chart anzeigen
st.line_chart(df[['Close', 'ema_fast', 'ema_slow']])
