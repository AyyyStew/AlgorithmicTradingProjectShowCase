# Trading Bot

## Introduction

The bot started as a simple script by Jawwastar on a Linux VPS, designed to execute a single trade using an older Coinbase Python library and then shut down. When I joined, we upgraded the bot for continuous operation:

- **Transition to Web APIs**: We moved to Coinbase's current Web APIs for better support and functionality.
- **Automation**: Converted the bot to a cron job for regular, scheduled trading.
- **Enhanced Responsiveness**: As trading frequency increased, we integrated `asyncio` to manage trades more dynamically, allowing for continuous operation based on real-time data.

The bot ran effectively for 12 months, overcoming early setup challenges.

## Technology Stack

- **Python**: Used for scripting, handling web APIs, and asynchronous operations.
- **Coinbase Web APIs**: Facilitates direct market interaction.
- **Linux, CRON, VPS**: Initial setup for scheduled task management.
- **Asyncio**: Supports high-frequency, real-time trading.

## Future Enhancements

We're planning several upgrades to enhance functionality and reduce costs:

- **Migration to AWS Lambda**: This will help decrease operational costs.
- **Multi-Tenancy**: Enables trading on multiple accounts.
- **Status Monitoring**: Tools for uptime, trades, and bot status via CLI and a website.
- **Trading Product Switching**: Flexibility in selecting trading products.
- **API Agnosticism**: Reduce dependency on Coinbase, allowing for use with other trading platforms.
