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


tydeclient = tyde3pub.TydeClient({"username": "devuser@broentech.no", "password": "testtest"})

tydeclient.get_upstream_status()
# tydeclient.print_role_info()

my = tydeclient.list_powerplants()
print("My plants:", my)

# Test for Hån power plant
pp_id = "660e967dbfe96ecfe47033f6"

hppinfo = tydeclient.get_powerplant_info(pp_id)

haveiaccess = tydeclient.has_access_to_hpp(pp_id)

my_sensors = tydeclient.get_sensor_for_powerplants(pp_id)

my_sensor_info = tydeclient.get_sensor_info("stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg")
print("My sensors:", my_sensor_info)

# portfolio_list = tydeclient.list_portfolios()

sensor_ids = ["stepsolutions.Haan.t_h01_10mindata_Grd_Prod_Pwr_Avg"]

# Get data between timestamps. Timestamps are in ISO 8601 format
from_time = "2024-04-01T00:00:00Z"
to_time = "2024-04-02T00:00:00Z"

# Get alarm

alarm_id = "proxima.Omron-Fins-Ethernet.Madland.SCADA_Omron.Madland.MASKIN-G1.VV.HOVEDVENTIL.AAPEN_STS"
alarms_data = tydeclient.get_alarms(alarm_id, from_time=from_time, to_time=to_time)
print("Alarms data:", alarms_data)

raw_sensor_data = tydeclient.get_raw_data(sensor_ids, from_time=from_time, to_time=to_time)
print("Raw sensor data:", raw_sensor_data)

sensor_data = tydeclient.get_aggregated_data(sensor_ids, from_time=from_time, to_time=to_time, aggregation="HOURLY")
print("Aggregated sensor data", sensor_data)

# Disabled converter as of now
# result= converter.convert("km", "m", 5)  # result is 5000
# results2 = converter.convert("m^3", "l", 10) # result is 9999.999
print("Done")
