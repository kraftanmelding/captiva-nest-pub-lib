from tyde3pub import tyde3pub
from tyde3pub import converter

sensorids= ["brøådæv.tæsåt.Sænsør_3", "brøådæv.tæsåt.Sænsør_2", "brøådæv.tæsåt.Sænsør_8"]  # example of sensor ID that we can fetch

alarm_id= ["proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.KRITISK_XA", "proxima.Boge_T1.PLC.SCADA_MB.Boge_T1.DAM-D1.INNTAK.GRIND.NEDSTROMS.NIVAA_LL_XA"]


tydeclient= tyde3pub.TydeClient({"username": "devuser@broentech.no", "password": "testtest"})

b= tydeclient.get_sensor_info("proxima.Sevre_T2.PLC.SCADA_MB.Sevre_T2.MASKIN-G1.KONTROLL.REG.NIVAA.AUTOSTART_SP")
#a= tydeclient.get_sensor_for_powerplants("boge")

#sensor_data = tydeclient.read_data(sensorids, timefrom=1709251200, timeto=1709282118, granularity="HOURLY")
alarms_data = tydeclient.read_alarms(alarm_id, timefrom=1709288763, timeto=1710757565)



#tydeclient= tyde3pub.TydeClient({"username": "anders@broentech.no", "password": "Test"})
tydeclient.get_upstream_status()
tydeclient.print_role_info()
sensor_data = tydeclient.read_data(sensorids, timefrom=1709251200, timeto=1709282118, granularity="HOURLY")

#sensor_data = tydeclient.read_data(sensorids, timefrom=1705761964, timeto=1706193964, granularity="RAW", aligned=False)

#sensorlatest= tydeclient.get_latest_datapoint(sensorids)



tydeclient.delete_sensor_data(["broedev.test.sensor_3", "broedev.test.sensor_2"], 0, 0)
my = tydeclient.list_powerplants()
sensor_data = tydeclient.read_data(sensorids, timefrom=0, timeto=17053169110, granularity="HOURLY")


haveiaccess = tydeclient.has_access_to_hpp("65a7e01c67d38191ae1fd6df")

my = tydeclient.list_powerplants()
hppinfo = tydeclient.get_powerplant_info("65a7e01c67d38191ae1fd6df")

haveiaccess = tydeclient.has_access_to_hpp("65a7e01c67d38191ae1fd6df")
my_sensors = tydeclient.get_sensor_for_powerplants()
#my_sensors = tydeclient.get_sensor_for_powerplants("65a7e01c67d38191ae1fd6df")
my_sensor_info = tydeclient.get_sensor_info("broedev.test.sensor_1")
port_list = tydeclient.list_portfolios()
sensor_data = tydeclient.read_data(sensorids, timefrom=0, timeto=17053169110, granularity="HOURLY")

result= converter.convert("km", "m", 5)  # result is 5000
results2 = converter.convert("m^3", "l", 10) # result is 9999.999
print("done")




