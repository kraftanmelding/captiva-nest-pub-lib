# Tyde3pub

This library encompasses essential functionalities required by Python services in Tyde3. It specifically provides functions 
for managing Authentication, Token verification, Token retrieval, as well as handling the reading Timeseries data and powerplants data.


## Description 
This library serves as a wrapper of essential functions required by multiple services within Tyde3.
Tyde3's package structure is organized into two modules. Here's a brief overview of each module:

```bash
tyde3pub/
├── converter
└── tyde3pub

 ```

## module **tyde3pub**
This subpackage serves as an abstraction layer that simplifies the intricacies of interfacing with Keycloak and managing tokens and interfacing with tyde apis. 
It consists of two submodules designed to cater to different use cases:
example of usage is like this: 

    from tyde3pub import tyde3pub
    tydeclient = tyde3pub.TydeClient({"username": "myusername@example.com", "password":"mystrongpasswd"})
    tydeclient.get_upstream_status()
    tydeclient.print_role_info()
    my_plants = tydeclient.list_powerplants()
    my_sensors= tydeclient.get_sensor_for_powerplants() # if we pass a hppid we get the sensor associated with a specific hppid
    sensor_info = tydeclient.get_sensor_info(sensorids)  # get the info for a specific sensorid
    sensor_data = tydeclient.read_data(["sensorId_1", "sensorId_2"], timefrom=1704107311, timeto=1705316911, granularity="HOURLY", aligned= False) 
    # DELETE Sensors. if you set timefrom=0 and timeto=0 it will completely delete the sensor including sensor metadata. 
    delete = tydeclient.delete_sensor_data(sensorids= ["sensorId_1", "sensorId_2"], timefrom=1704107311, timeto=1705316911)


TydeClient also accept more advanced parameters, such as audience, authorization endpoints etc. The default one should just work fine!
Look at the example in the example.py file

## Module **converter**
This module is dedicated to the unit conversion. It accept a wide range of string as unit representation. in case value int or float as input, return a float.
in case of value is a list or an ndarray, it returns a ndarray. 

    from tyde3.utils import converter
    result= converter.convert("km", "m")  # result is 1000, because value is defaulted to 1
    result= converter.convert("km", "meters")  # this is also accepted
    result= converter.convert("km", "m", 5)  # result is 5000
    result= converter.convert("", "", 5)  # result is 5. "" is used for dimensionless
    # list are also a valid value inputs:
    results2 = converter.convert("m^3", "l", [10, 323, 0.3])  # result is a ndarray of the converted values eg [1.00e+04 3.23e+05 3.00e+02]

In case an invalid unit or conversion called, an exception rises:
    
    results2 = converter.convert("squaredmeters", "km^2"])  # exception
    # 'squaredmeters' is not defined in the unit registry
    results2 = converter.convert("m^2", "l"])  # exception
    # Cannot convert from 'meter ** 2' ([length] ** 2) to 'liter' ([length] ** 3)


# Developers setup
You can donwload the tar.gz file in this repo and then pip install the package with this:

*  pip install -e /PATH/tyde3pub_v0.0.1.tar.gz

It will also install the following packages: 

    'PyJWT',
    'cryptography',
    'requests',
    'rauth',
    'pint',


## Building package:
Before to start make sure that you set the correct name/version on the setup.py file. 
 
Install the setuptools and wheel and twine:

* pip install --user --upgrade setuptools wheel twine

Build the package. 

* python3 setup.py sdist

The package format tar.gz is now available under dist/ foder

You can then upload the tar.gz file to your private repo with: 

* python3 -m twine upload --repository-url $PIPYURL -u $USERNAME -p $PASSWORS dist/*.tar.gz --verbose

## DevOps Info
This is not meant to be used as stand alone service.


## Versions
 
* V0.0.1 : Basic functionalities

## Note
This is a Alpha version of the Library

## Info and Support
Luca Petricca @ Broentech Solutions 
Team: Broentech Solutions 

