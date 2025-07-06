import requests
from typing import Optional
from back_api.settings.config import DEVICE_DATA_SERVICE_URL
from back_api.utils.date_parser import parse_device_data_times

class DeviceService:
    BASE_URL = DEVICE_DATA_SERVICE_URL

    @staticmethod
    def get_device_data(device_id: str, to: Optional[int] = None, front: Optional[int] = None):
        url = f"{DeviceService.BASE_URL}/device/{device_id}"
        params = {}
        if to:
            params['to'] = to
        if front:
            params['front'] = front

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return parse_device_data_times(response.json())
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as err:
            return {"error": f"Request error occurred: {err}"}
        except Exception as exc:
            return {"error": f"An unexpected error occurred: {exc}"}
        
    @staticmethod
    def get_device_times(device_id: str):
        url = f"{DeviceService.BASE_URL}/times/{device_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as err:
            return {"error": f"Request error occurred: {err}"}
        except Exception as exc:
            return {"error": f"An unexpected error occurred: {exc}"}