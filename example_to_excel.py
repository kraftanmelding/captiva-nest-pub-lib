from tyde3pub import tyde3pub
import pandas as pd
from datetime import datetime, timedelta

# sensor_ids = [
#     "stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg",
#     "stepsolutions.Haan.t_h02_10mindata_Grd_Prod_Pwr_Avg",
#     "stepsolutions.Haan.t_h03_10mindata_Grd_Prod_Pwr_Avg"
# ]  # example of sensor ID that we can fetch

# alarm_id= [
#     "proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.KRITISK_XA",
#     "proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.NIVAA_LL_XA"
# ]


tyde_client = tyde3pub.TydeClient({"username": "mo@captiva.no", "password": "lWRlunyNcM$A2e7GaSgR"})

tyde_client.get_upstream_status()
# tyde_client.print_role_info()

my = tyde_client.list_powerplants()
print("My plants:", my)

# Test for Dyrstad power plant
pp_id = "660e9677bfe96ecfe47033e6"

pp_info = tyde_client.get_powerplant_info(pp_id)

have_access = tyde_client.has_access_to_pp(pp_id)

pp_sensors = tyde_client.get_powerplant_sensors(pp_id)
print("Power plant sensors:", pp_sensors)

sensor_human_name = "proxima.NVK-Omron.Dyrstad.SCADA_Omron.Dyrstad.MASKIN-G1.GEN.VIBR_PV"
sensor_id = "66126077bfe96ecfe4703889"

my_sensor_info = tyde_client.get_sensor_info(sensor_id)
print("My sensors:", my_sensor_info)

# portfolio_list = tyde_client.list_portfolios()

# Function to split the date range into intervals of less than 30 days for raw data
def split_into_intervals(from_time, to_time, max_days=28):
    from_time_dt = datetime.fromisoformat(from_time[:-1])  # Remove 'Z' for parsing
    to_time_dt = datetime.fromisoformat(to_time[:-1])  # Remove 'Z' for parsing
    delta = timedelta(days=max_days)

    intervals = []
    current_time = from_time_dt

    while current_time < to_time_dt:
        end_time = min(current_time + delta, to_time_dt)
        intervals.append((current_time.isoformat() + "Z", end_time.isoformat() + "Z"))
        current_time = end_time

    return intervals

# Function to export data to Excel
def export_to_excel(data, file_name="sensor_data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Data exported to {file_name}")

# Function to convert ISO 8601 timestamp to Excel-friendly format
def convert_to_excel_friendly_timestamp(iso_timestamp):
    try:
        # Try parsing timestamp with microseconds
        dt_object = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # If parsing with microseconds fails, try without microseconds
        dt_object = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Format it to 'YYYY-MM-DD HH:MM:SS' which is Excel-friendly (discard microseconds)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

# Initialize Tyde Client
tyde_client = tyde3pub.TydeClient({"username": "mo@captiva.no", "password": "lWRlunyNcM$A2e7GaSgR"})

# Define sensor IDs
sensor_ids = ["proxima.NVK-Omron.Dyrstad.SCADA_Omron.Dyrstad.MASKIN-G1.GEN.VIBR_PV"]

# Define time range
from_time = "2024-04-01T00:00:00Z"
to_time = "2024-09-10T00:00:00Z"

# Get intervals of less than 30 days
intervals = split_into_intervals(from_time, to_time)

# Initialize list to collect timestamp and value data
all_sensor_data = []

# Loop through intervals and fetch raw data for each
for start, end in intervals:
    print(f"Fetching data from {start} to {end}")
    raw_sensor_data = tyde_client.get_raw_data(sensor_ids, from_time=start, to_time=end)

    if raw_sensor_data and 'data' in raw_sensor_data:
        for entry in raw_sensor_data['data']:
            timestamp = entry.get('timestamp')
            value = entry.get('value')
            formatted_timestamp = convert_to_excel_friendly_timestamp(timestamp)
            all_sensor_data.append({'timestamp': formatted_timestamp, 'value': value})
    else:
        print(f"No data returned for interval {start} to {end}")

if all_sensor_data:
    export_to_excel(all_sensor_data, "sensor_raw_data.xlsx")
    print("Data exported to Excel.")
else:
    print("No data to export.")

print("Done")

# Get alarms

#alarm_id = "proxima.Omron-Fins-Ethernet.Madland.SCADA_Omron.Madland.MASKIN-G1.VV.HOVEDVENTIL.AAPEN_STS"
#alarms_data = tyde_client.get_alarms(alarm_id, from_time=from_time, to_time=to_time)
#print("Alarms data:", alarms_data)

raw_sensor_data = tyde_client.get_raw_data(sensor_ids, from_time=from_time, to_time=to_time)
print("Raw sensor data:", raw_sensor_data)

#sensor_data = tyde_client.get_aggregated_data(sensor_ids, from_time=from_time, to_time=to_time, aggregation="HOURLY")
#print("Aggregated sensor data", sensor_data)
