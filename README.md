# Algorithmic Trading Project Showcase

Welcome to our showcase of the Algorithmic Trading Project, which started from a conversation during a Brazilian Jiu Jitsu class. This repository holds a cleaned-up version of our trading strategy backtesting library and a Coinbase trading bot. We've kept some of our more detailed research and strategies private for potential future use.

## Project Overview

### Origins and Evolution

The project kicked off with Ryan's R script for trading strategy verification. I joined in to transition the work into Python, leading to a more robust development phase.

- **Transition from R to Python**: We moved from Ryan's initial R scripts to Python, extensively using Jupyter Notebooks for strategy testing and development.
- **Development of backtester_lib**: We created `backtester_lib`, a Python library that allowed us to test and execute strategies efficiently.
- **Bot Deployment and Results**: We launched our trading bot on a Linux VPS, automated with cron, achieving a 43% return on investment from October 2023 to September 2024.

### Technical Milestones

- **Mixed Development Environments**: Ryan worked on strategies with paper and R, while I focused on Python for extensive backtesting.
- **Building a Scalable System**: We developed a modular, class-based system to handle more complex strategy tests, improving maintenance and scalability.
- **Enhanced Testing with Parallelization**: Using Dask, we parallelized our tests, allowing us to manage large datasets and multiple strategies efficiently.

### Pausing and Learning

Despite good returns, we paused to evaluate the project's scalability and market fit. This break taught us valuable lessons about the importance of organization and adaptability, especially as project demands increased.

### Skills and Technologies

- **Math and Finance**: We used time series analysis, statistical testing, and technical analysis to develop and manage our strategies.
- **Programming**: Our toolkit included Python, Pandas, Matplotlib, Dask, asyncio, and Requests.
- **Systems and APIs**: We operated on a Linux system, using cron for automation and Coinbase's REST API for transactions.

## Explore the Project

Check out the following directories for more on our tools and results:

- **[Backtesting](./Backtesting/)**: Includes `backtester_lib` and its documentation.
- **[TradingBot](./TradingBot/)**: Contains the trading bot and deployment scripts.

For more details or questions, please reach out through GitHub.
