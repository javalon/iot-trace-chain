from persistence_worker.utils.logger_config import setup_logger
from deltalake.writer import write_deltalake
import pandas as pd
import os
import json

class DeltaWriter:
    def __init__(self, aws_access_key, aws_secret_key, aws_s3_endpoint_url, aws_s3_secure, delta_path):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_s3_endpoint_url = aws_s3_endpoint_url
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_s3_secure = aws_s3_secure
        self.delta_path = delta_path
        self.logger = setup_logger(__name__)

    def start(self):
        pass

    def stop(self):
        pass

    def save_data(self, device_id, iot_data):
        if not isinstance(iot_data, list):
            iot_data = [iot_data]

        for data in iot_data:
            data["device_id"] = device_id

        df = pd.DataFrame(iot_data)
        df = self.__clean_up_df(df)

        storage_options = {
            "AWS_ACCESS_KEY_ID": self.aws_access_key,
            "AWS_SECRET_ACCESS_KEY": self.aws_secret_key,
            "AWS_REGION": self.aws_region,
            "AWS_ENDPOINT_URL": self.aws_s3_endpoint_url,
            "USE_DELTA_LAKE_UNSAFE_RENAME": "true",
            "AWS_ALLOW_HTTP": "true" if not self.aws_s3_secure else "false",
        }
        try:
            write_deltalake(
                self.delta_path,
                df,
                mode="append",
                partition_by=["device_id", "date"],
                storage_options=storage_options,
            )
            self.logger.info("✅ Data saved in Delta Lake.")
        except Exception as e:
            self.logger.error("❌ Error saving data to Delta Lake: %s", e)
            raise

    def __clean_up_df(self, df):
        df = df[df["timestamp"].notna()]

        def cast_timestamp(ts):
            try:
                ts_int = int(ts)
                if len(str(ts_int)) >= 10:
                    dt = pd.to_datetime(ts_int, unit="s", errors="coerce")
                else:
                    dt = pd.to_datetime(ts, errors="coerce")
            except Exception:
                return pd.NaT

            # Asegura que esté en UTC
            if dt.tzinfo is None:
                return dt.tz_localize("UTC")
            else:
                return dt.tz_convert("UTC")

        df["ts_cast"] = df["timestamp"].apply(cast_timestamp)
        df["date_raw"] = df["ts_cast"]

        failed_cast_count = df["date_raw"].isna().sum()
        if failed_cast_count > 0:
            self.logger.warning(f"⚠️ {failed_cast_count} record(s) failed to cast timestamp to date.")

        df = df[df["date_raw"].notna()].copy()
        df["date"] = df["date_raw"].dt.date
        df.drop(columns=["date_raw"], inplace=True)

        df['merkle_proof'] = df['merkle_proof'].apply(json.dumps)
        # Print first 5 rows for debugging
        self.logger.debug("First 5 rows of cleaned DataFrame:\n%s", df.head())

        self.logger.info(f"📦 Saving {len(df)} valid record(s) to Delta Lake.")

        return df

    
            
    
