Here is an updated `README.md` with all tools listed, API key setup instructions, and copyright/license section.

---

# FoxESS Inverter Data Retrieval MCP Server

This repository contains the files to build a Model Context Protocol (MCP) server that retrieves data from the FoxESS Cloud API. The server provides tools to fetch daily, monthly, and yearly reports for a specified inverter, as well as additional device and plant management functions.

## Tools Included

- `get_plant_list`: Retrieves the list of plants.
- `get_plant_detail`: Gets details for a specific plant.
- `get_device_list`: Lists all devices.
- `get_device_detail`: Gets details for a specific device.
- `get_device_variables`: Retrieves device variables.
- `query_device_history`: Queries historical device data.
- `get_device_generation`: Gets device generation statistics.
- `get_battery_soc`: Retrieves battery state of charge.
- `set_battery_soc`: Sets battery state of charge.
- `get_force_charge_time`: Gets force charge time settings.
- `set_force_charge_time`: Sets force charge time.
- `get_module_list`: Lists all modules.
- `get_access_count`: Gets user access count.

## How it Works

The `server.py` script uses the FastMCP framework to wrap functions that make authenticated requests to the FoxESS Cloud API. Your API key is securely loaded from an environment variable, preventing it from being exposed in the code.

## API Key Setup

1. Copy `env.example` to `.env`:
   ```
   cp env.example .env
   ```
2. Edit `.env` and add your FoxESS API key:
   ```
   FOXESS_API_KEY=your_actual_api_key_here
   ```

You will need a valid API key from your FoxESS Cloud account. 
The server provides a clean API for other services to request data.

## Docker Setup

1. **Build the Docker image:**
   ```
   docker build -t mcp-foxess-server .
   ```
2. **Now you can the docker image in any LLM:**
   
---

## Copyright and License

Copyright © 2025 asped

This project is licensed under the MIT License. See the `LICENSE` file for details.