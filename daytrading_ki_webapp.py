import streamlit as st
import pandas as pd
import yfinance as yf
import ta

# Seite konfigurieren
st.set_page_config(page_title="Krypto Daytrading KI", layout="centered")

# Titel und Beschreibung
st.title("📉 Krypto Daytrading KI – 5-Minuten Signale")
st.markdown("Dieses Tool zeigt dir Kauf-/Verkaufssignale für BTC/USD basierend auf RSI und EMA.")

# Daten abrufen
df = yf.download("BTC-USD", interval="5m", period="1d")
df.dropna(inplace=True)

# Spalte "Close" extrahieren
close = df['Close']

# Indikatoren berechnen
df['rsi'] = ta.momentum.RSIIndicator(close).rsi()
df['ema_fast'] = ta.trend.EMAIndicator(close, window=9).ema_indicator()
df['ema_slow'] = ta.trend.EMAIndicator(close, window=21).ema_indicator()

# Handelssignal basierend auf RSI & EMA
def generate_signal(row):
    if row['rsi'] < 30 and row['ema_fast'] > row['ema_slow']:
        return 'BUY'
    elif row['rsi'] > 70 and row['ema_fast'] < row['ema_slow']:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(generate_signal, axis=1)

# Letztes Signal anzeigen
last_signal = df['signal'].iloc[-1]
st.subheader("Aktuelles Signal:")
st.markdown(f"### 🟢 {last_signal}" if last_signal == "BUY" else f"### 🔴 {last_signal}" if last_signal == "SELL" else "### ⚪️ HOLD")

# Vorschau anzeigen
st.line_chart(df[['Close', 'ema_fast', 'ema_slow']])
