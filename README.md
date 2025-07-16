# Wheel Strategy Simulator (v2)

This project simulates the Wheel Options Strategy in Python using historical OHLC data, monthly contributions, and realistic assignment logic.

## 🔧 Features

- Weekly PUT/CALL cycles
- Capital + position tracking
- Income simulation
- Rolling volatility
- Basic Greeks: Delta (approx), Theta (est.)

## 📁 Structure

- `main.py`: basic simulation
- `source/engine/`: backtest engines
- `source/data/`: contribution generator

## ▶️ How to run

```bash
pip install -r requirements.txt
python main_v2.py
