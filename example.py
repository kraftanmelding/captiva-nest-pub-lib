from tyde3pub import tyde3pub
# from tyde3pub import converter

# sensor_ids = [
#     "stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg",
#     "stepsolutions.Haan.t_h02_10mindata_Grd_Prod_Pwr_Avg",
#     "stepsolutions.Haan.t_h03_10mindata_Grd_Prod_Pwr_Avg"
# ]  # example of sensor ID that we can fetch

# alarm_id= [
#     "proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.KRITISK_XA",
#     "proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.NIVAA_LL_XA"
# ]


tyde_client = tyde3pub.TydeClient({"username": "devuser@broentech.no", "password": "testtest"})

tyde_client.get_upstream_status()
# tyde_client.print_role_info()

my = tyde_client.list_powerplants()
print("My plants:", my)

# Test for Hån power plant
pp_id = "660e967dbfe96ecfe47033f6"

pp_info = tyde_client.get_powerplant_info(pp_id)

have_access = tyde_client.has_access_to_pp(pp_id)

pp_sensors = tyde_client.get_sensors_for_powerplant(pp_id)
print("Power plant sensors:", pp_sensors)

sensor_human_name = "stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg"
sensor_id = "66126091bfe96ecfe47041f9"

my_sensor_info = tyde_client.get_sensor_info(sensor_id)
print("My sensors:", my_sensor_info)

# portfolio_list = tyde_client.list_portfolios()

sensor_ids = ["stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg"]

# Get data between timestamps. Timestamps are in ISO 8601 format
from_time = "2024-04-01T00:00:00Z"
to_time = "2024-04-02T00:00:00Z"

# Get alarm

alarm_id = "proxima.Omron-Fins-Ethernet.Madland.SCADA_Omron.Madland.MASKIN-G1.VV.HOVEDVENTIL.AAPEN_STS"
alarms_data = tyde_client.get_alarms(alarm_id, from_time=from_time, to_time=to_time)
print("Alarms data:", alarms_data)

raw_sensor_data = tyde_client.get_raw_data(sensor_ids, from_time=from_time, to_time=to_time)
print("Raw sensor data:", raw_sensor_data)

sensor_data = tyde_client.get_aggregated_data(sensor_ids, from_time=from_time, to_time=to_time, aggregation="HOURLY")
print("Aggregated sensor data", sensor_data)

# Disabled converter as of now
# result= converter.convert("km", "m", 5)  # result is 5000
# results2 = converter.convert("m^3", "l", 10) # result is 9999.999
print("Done")
