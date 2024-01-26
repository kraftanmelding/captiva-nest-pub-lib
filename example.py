from tyde3pub import tyde3pub
from tyde3pub import converter

sensorids= ["broedev.test.sensor_1", "broedev.test.sensor_3", "broedev.test.sensor_10"]  # example of sensor ID that we can fetch
tydeclient= tyde3pub.TydeClient({"username": "EXAMPLE@broentech.no", "password": "MYPASSWD"})

tydeclient.get_upstream_status()
tydeclient.print_role_info()


my = tydeclient.list_powerplants()
hppinfo = tydeclient.get_powerplant_info("65a7e01c67d38191ae1fd6df")

haveiaccess = tydeclient.has_access_to_hpp("65a7e01c67d38191ae1fd6df")

my_sensors = tydeclient.get_sensor_for_powerplants()
my_sensor_info = tydeclient.get_sensor_info("broedev.test.sensor_1")
port_list = tydeclient.list_portfolios()
sensor_data = tydeclient.read_data(sensorids, timefrom=1704107311, timeto=1705316911, granularity="RAW")

result= converter.convert("km", "m", 5)  # result is 5000
results2 = converter.convert("m^3", "l", 10) # result is 9999.999
print("done")




