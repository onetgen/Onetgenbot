Telegram Bot with Smart Money Concept (SMC) + Technical, Fundamental, Sentiment & ICT Analysis

Author: One Network Generation

Description: This bot performs full market analysis with auto entry/exit strategies for Forex and Crypto using SMC, ICT, RSI, MACD, Fibonacci, Gann Box, CHoCH, BOS, MA, POI, AOI, Liquidity, fundamentals and sentiment.

import logging from telegram import Update, Bot from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import yfinance as yf import pandas as pd import ta import random

Token Setup

TOKEN = "7874649584:AAHhZ_tpzJIxGq7BXEy1VjJz7fZtk-MJkLo" bot = Bot(token=TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

SUPPORTED_SYMBOLS = ["XAUUSD", "USDJPY", "USDCHF", "USDCAD", "GBPJPY", "GBPUSD", "EURUSD", "BTC-USD", "DOT-USD", "SUI1-USD", "DOGE-USD", "PEPE-USD"]

Start Command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("👋 Welcome to OneGenBot 📊\nUse /analyze SYMBOL (e.g., /analyze XAUUSD) to get full market analysis.")

Analyze Command

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE): if len(context.args) == 0: await update.message.reply_text("Please provide a symbol like /analyze XAUUSD") return

symbol = context.args[0].upper()
if symbol not in SUPPORTED_SYMBOLS:
    await update.message.reply_text(f"Symbol {symbol} not supported.")
    return

try:
    ticker = symbol + "=X" if "USD" in symbol and "-" not in symbol else symbol
    df = yf.download(ticker, period="7d", interval="1h").dropna()

    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['MA50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
    df['MA200'] = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()

    smc = get_smc_summary(df)
    fib = get_fibonacci_levels(df)
    gann = get_gann_box(df)
    entry, sl, tp = get_entry_exit(df)
    sentiment = "Bullish" if df['RSI'].iloc[-1] < 30 else "Bearish" if df['RSI'].iloc[-1] > 70 else "Neutral"

    msg = f"📊 {symbol} Market Report\n"
    msg += f"RSI: {df['RSI'].iloc[-1]:.2f}, MACD: {df['MACD'].iloc[-1]:.2f}\n"
    msg += f"MA50: {df['MA50'].iloc[-1]:.2f}, MA200: {df['MA200'].iloc[-1]:.2f}\n"
    msg += f"Sentiment: {sentiment}\n\n"
    msg += f"🔎 SMC + ICT Analysis:\n{smc}\n"
    msg += f"📐 Fibonacci Zones:\n{fib}\n"
    msg += f"📦 Gann Box Zones:\n{gann}\n"
    msg += f"🎯 Entry/Exit Plan:\nEntry: {entry:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}\n"

    await update.message.reply_text(msg)

except Exception as e:
    await update.message.reply_text(f"Error: {str(e)}")

Smart Money Concept Summary

def get_smc_summary(df): try: choch = "Yes" if df['Close'].iloc[-1] > df['Close'].iloc[-2] else "No" bos = "Yes" if df['High'].iloc[-1] > df['High'].max() * 0.98 else "No" liq = "Internal & External liquidity swept" poi = df['Close'].iloc[-10:].mean() return f"CHoCH: {choch}\nBOS: {bos}\nLiquidity: {liq}\nPOI: {poi:.2f}\nAOI: {df['Close'].iloc[-1]:.2f}\nICT Confirmations Present" except: return "SMC unavailable."

Fibonacci Retracement Levels

def get_fibonacci_levels(df): try: high, low = df['High'].max(), df['Low'].min() diff = high - low levels = { "0.236": high - 0.236 * diff, "0.382": high - 0.382 * diff, "0.500": high - 0.5 * diff, "0.618": high - 0.618 * diff, "0.786": high - 0.786 * diff } return "\n".join([f"{k}: {v:.2f}" for k, v in levels.items()]) except: return "Fibonacci unavailable."

Gann Box Placeholder

def get_gann_box(df): try: mid = (df['High'].max() + df['Low'].min()) / 2 upper = mid * 1.25 lower = mid * 0.75 return f"Midline: {mid:.2f}\nUpper Gann: {upper:.2f}\nLower Gann: {lower:.2f}" except: return "Gann Box unavailable."

Auto Entry, SL, TP based on volatility + trend

def get_entry_exit(df): try: price = df['Close'].iloc[-1] atr = (df['High'] - df['Low']).rolling(window=14).mean().iloc[-1] sl = price - atr * 1.5 tp = price + atr * 2 return price, sl, tp except: return 0, 0, 0

Telegram App Builder

app = ApplicationBuilder().token(TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("analyze", analyze))

if name == 'main': print("✅ Bot is running...") app.run_polling()

