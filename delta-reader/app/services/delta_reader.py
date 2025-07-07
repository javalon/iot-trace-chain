from deltalake import DeltaTable
from deltalake._internal import TableNotFoundError
import pandas as pd
from datetime import datetime, timedelta
from app.models.device_data import DeviceData
from app.config.settings import DELTA_S3_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, AWS_ENDPOINT_URL, AWS_S3_SECURE

storage_options = {
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_KEY,
        "AWS_REGION": AWS_REGION,
        "AWS_ENDPOINT_URL": AWS_ENDPOINT_URL,
        "USE_DELTA_LAKE_UNSAFE_RENAME": "true",
        "AWS_ALLOW_HTTP": "true" if not AWS_S3_SECURE else "false",
    }


def get_device_data(device_id: str, start_date: str = None, end_date: str = None) -> list[DeviceData]:
    if end_date is None:
        end_date = datetime.utcnow().date()
    else:
        end_date = pd.to_datetime(end_date).date()

    if start_date is None:
        start_date = end_date - timedelta(days=1)
    else:
        start_date = pd.to_datetime(start_date).date()

    dt = DeltaTable(DELTA_S3_PATH, storage_options=storage_options)
    df = dt.to_pandas()
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"]).dt.date

    filtered_df = df[
        (df["device_id"] == device_id) &
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ]

    return [DeviceData(**row) for row in filtered_df.to_dict(orient="records")]

def get_device_times(device_id: str) -> dict:
    try:
        dt = DeltaTable(DELTA_S3_PATH, storage_options=storage_options)
        df = dt.to_pandas()
    except TableNotFoundError:
        # No Delta log files found, return None or a custom response
        return {
            "min_date": None,
            "max_date": None,
            "error": "Delta table not found"
        }
    except Exception as e:
        # Log or handle other unexpected errors
        return {
            "min_date": None,
            "max_date": None,
            "error": f"Unexpected error: {str(e)}"
        }

    filtered_df = df[df["device_id"] == device_id]

    if filtered_df.empty:
        return {
            "min_date": None,
            "max_date": None
        }

    if not pd.api.types.is_datetime64_any_dtype(filtered_df["timestamp"]):
        filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"].astype(float), errors="coerce", unit="s")

    min_date = int(filtered_df["timestamp"].min().timestamp()) if not pd.isna(filtered_df["timestamp"].min()) else None
    max_date = int(filtered_df["timestamp"].max().timestamp()) if not pd.isna(filtered_df["timestamp"].max()) else None

    return {
        "min_date": min_date,
        "max_date": max_date
    }