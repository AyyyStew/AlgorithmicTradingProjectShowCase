# Backtester Lib

## Overview

Backtester Lib is a Python-based library designed for the rigorous backtesting of trading strategies. It offers a flexible framework that allows for custom strategy implementation, adjustable trading fees, and compatibility with various datasets.

## Features

- **Robust Backtesting**: Evaluate trading strategies with a comprehensive suite of tools.
- **Custom Strategy Definition**: Implement and test your own trading strategies.
- **Adjustable Parameters**: Set trading fees and adapt to different datasets easily.
- **Performance Metrics**: Efficiently extract key metrics from your backtest results.

## Technology Stack

- **Python**: Primary programming language.
- **Libraries**: Utilizes Pandas, Numpy, Scipy, Dask, and Matplotlib for data handling and visualization.
- **Tools**: Developed and tested within Jupyter Notebooks.

## Quickstart

To start using Backtester Lib, refer to our detailed guide in [HowToUse.ipynb](./HowToUse.ipynb). Here’s a brief example to set up a backtest:

```python
# Example of initializing and running a backtest
from datetime import datetime
from backtester_lib.strategies.buy_and_hold import BuyAndHold
from backtester_lib.strategy_tester import StrategyTester
from backtester_lib.assets.holding import Holding
from backtester_lib.utils import open_pricing
from backtester_lib.ticker import Ticker

# Setup data and parameters
data_csv = "./data/btcData1d.csv"
ticker = Ticker("ticker", data_csv, "4hr")
holding = Holding(ticker)

# Create or use your strategy
test_strat = BuyAndHold()

# Run your backtest
dataframe and TestResult Object
test_name = "buy_and_hold_test"
test, test_result = StrategyTester(
    "buy_and_hold", test_strat, holding
).run_test(
    name=test_name,
    start_date=datetime(2022, 9, 1),
    end_date=datetime(2024, 11, 1),
    buy_pricing_function=open_pricing,
    sell_pricing_function=open_pricing,
)
```

## Planned Enhancements

- **Computational Efficiency**: Further optimize backtesting algorithms for speed and larger data handling.
- **Parallel Testing**: Integrate native support for parallel testing to shorten backtesting times on multi-core systems.
- **Historical Database**: Build a database for storing test strategies, parameters, and results to facilitate detailed analysis.
- **User Interface**: Develop a simple GUI to make the library more accessible to those less familiar with programming.

## Diagrams

Below is the class diagram of Backtester Lib, showing its structure and relationships between classes.

![Class Diagram](./documentation/images/class_diagram.png)
