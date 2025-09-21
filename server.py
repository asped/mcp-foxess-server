import os
import logging
import dotenv
import requests
import time
import hashlib
import json
from typing import Optional, Dict, Any

from fastmcp import FastMCP

# Load environment variables from .env file
dotenv.load_dotenv()

# Configure logging to stderr
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=os.getenv('LOG_FILE', '/dev/stderr'))
logging.getLogger("fastmcp").setLevel(logging.INFO)

app = FastMCP()

API_KEY = os.getenv("FOXESS_API_KEY")
DOMAIN = "https://www.foxesscloud.com"

if not API_KEY:
    logging.error("FOXESS_API_KEY environment variable not set. The server may not function correctly.")

def generate_signature(path: str, token: str, timestamp: int) -> str:
    """Generate signature for FoxESS API authentication."""
    # Create signature string as per API docs
    signature = fr"{path}\r\n{token}\r\n{timestamp}"
    # Generate MD5 hash
    return hashlib.md5(signature.encode('UTF-8')).hexdigest().lower()

def make_api_request(method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Makes a request to the FoxESS API and returns the response."""
    if not API_KEY:
        return {"error": "API credentials are not configured."}

    url = DOMAIN + path
    timestamp = round(time.time() * 1000)

    headers = {
        'token': API_KEY,
        'timestamp': str(timestamp),
        'signature': generate_signature(path, API_KEY, timestamp),
        'lang': 'en',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    try:
        if method.lower() == 'get':
            response = requests.get(url=url, params=params, headers=headers, verify=True)
        elif method.lower() == 'post':
            response = requests.post(url=url, json=params, headers=headers, verify=True)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        logging.error(f"An unexpected error occurred: {err}")
        return {"error": f"An unexpected error occurred: {err}"}

# Plant endpoints
@app.tool()
def get_plant_list(current_page: int = 1, page_size: int = 10):
    """Get list of plants."""
    path = '/op/v0/plant/list'
    params = {'currentPage': current_page, 'pageSize': page_size}
    return make_api_request('post', path, params)

@app.tool()
def get_plant_detail(plant_id: str):
    """Get details of a specific plant."""
    path = '/op/v0/plant/detail'
    params = {'id': plant_id}
    return make_api_request('get', path, params)

# Device endpoints
@app.tool()
def get_device_list(current_page: int = 1, page_size: int = 500):
    """Get list of devices."""
    path = '/op/v0/device/list'
    params = {'currentPage': current_page, 'pageSize': page_size}
    return make_api_request('post', path, params)

@app.tool()
def get_device_detail(sn: str):
    """Get details of a specific device."""
    path = '/op/v0/device/detail'
    params = {'sn': sn}
    return make_api_request('get', path, params)

@app.tool()
def get_device_variables():
    """Get available device variables."""
    path = '/op/v0/device/variable/get'
    return make_api_request('get', path)

@app.tool()
def query_device_real_time(sn: str, variables: list):
    """Query real-time device data."""
    path = '/op/v0/device/real/query'
    params = {'sn': sn, 'variables': variables}
    return make_api_request('post', path, params)

@app.tool()
def query_device_history(sn: str, variables: list, hours: int = 24):
    """Query historical device data."""
    path = '/op/v0/device/history/query'
    end_time = int(time.time() * 1000)
    begin_time = end_time - (hours * 3600000)
    params = {
        'sn': sn,
        'variables': variables,
        'begin': begin_time,
        'end': end_time
    }
    return make_api_request('post', path, params)

@app.tool()
def get_device_generation(sn: str):
    """Get device generation data."""
    path = '/op/v0/device/generation'
    params = {'sn': sn}
    return make_api_request('get', path, params)

# Battery management endpoints
@app.tool()
def get_battery_soc(sn: str):
    """Get battery state of charge."""
    path = '/op/v0/device/battery/soc/get'
    params = {'sn': sn}
    return make_api_request('get', path, params)

@app.tool()
def set_battery_soc(sn: str, min_soc: int, min_soc_on_grid: int):
    """Set battery state of charge parameters."""
    path = '/op/v0/device/battery/soc/set'
    params = {
        'sn': sn,
        'minSoc': min_soc,
        'minSocOnGrid': min_soc_on_grid
    }
    return make_api_request('post', path, params)

@app.tool()
def get_force_charge_time(sn: str):
    """Get battery force charge time settings."""
    path = '/op/v0/device/battery/forceChargeTime/get'
    params = {'sn': sn}
    return make_api_request('get', path, params)

@app.tool()
def set_force_charge_time(sn: str, config: dict):
    """Set battery force charge time settings."""
    path = '/op/v0/device/battery/forceChargeTime/set'
    params = {"sn": sn, **config}
    return make_api_request('post', path, params)

# Module endpoints
@app.tool()
def get_module_list(current_page: int = 1, page_size: int = 10):
    """Get list of modules."""
    path = '/op/v0/module/list'
    params = {'currentPage': current_page, 'pageSize': page_size}
    return make_api_request('post', path, params)

# User endpoints
@app.tool()
def get_access_count():
    """Get user access count."""
    path = '/op/v0/user/getAccessCount'
    return make_api_request('get', path)

if __name__ == '__main__':
    logging.info("Starting the FastMCP server...")
    try:
        app.run()
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
