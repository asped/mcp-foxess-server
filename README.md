# FoxESS Inverter Data Retrieval MCP Server

This repository contains the files to build a Model Context Protocol (MCP) server that retrieves data from the FoxESS Cloud API. The server provides tools to fetch daily, monthly, and yearly reports for a specified inverter.

### Tools Included:
- `get_daily_report`: Fetches the daily energy report for a specific inverter.
- `get_monthly_report`: Fetches the monthly energy report.
- `get_yearly_report`: Fetches the yearly energy report.

### How it Works
The `server.py` script uses the FastMCP framework to wrap functions that make authenticated requests to the FoxESS Cloud API. Your API key is securely loaded from an environment variable, preventing it from being exposed in the code.

### Usage
Follow the installation instructions to build and run the Docker container. You will need a valid API key from your FoxESS Cloud account. The server provides a clean API for other services to request data.

