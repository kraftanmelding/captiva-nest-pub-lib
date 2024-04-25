__author__ = 'Luca'
"""
    >File : converter.py

    >Date of creation : 22.01.2023

    >Copyrights : Broentech Solutions AS

    >Project : Next-Gen Tyde

    >Author : Luca Petricca (lucap@broentech.no)

    Description :

        This is a library that contains functions for unit conversion

"""

import pint
UREG = pint.UnitRegistry()  # let's make it global to speed it up


def convert(from_unit, to_unit, value=1):
    """ Convert the value from_unit to to_unit. dimensionless is ""

    Args:
        from_unit (string): A string representation of the current unit of measurement eg "m" or "meters"
        to_unit (string): A string representation of the desired unit of measurement eg "km" or "kilometers"
        value (number, list or ndarray): The value to be converted. if none is passed, then value=1

    Returns:
        value (number or ndarray) if conversion is valid, otherwise raise exception.
    """
    # this we handle it in another function because pint does not support mWc
    if is_meter_water_column(from_unit) or is_meter_water_column(to_unit):
        return convert_meters_h20(from_unit, to_unit, value)
    converted_value = value * UREG(from_unit).to(to_unit)
    return converted_value.magnitude


def convert_meters_h20(from_unit, to_unit, value=1):
    # mWc is not definied in the library, but cm_h2o is defined
    if is_meter_water_column(from_unit):
        value = 100 * value
        from_unit = "cm_H2O"
    if is_meter_water_column(to_unit):
        converted_value = value * UREG(from_unit).to("cm_H2O")
        return converted_value.magnitude / 100
    return value * UREG(from_unit).to(to_unit).magnitude


def is_meter_water_column(unit):
    unit = unit.lower()
    if unit == "mwc" or unit == "m_h2o" or unit == "mh2o" or unit == "meter_h20":
        return True
    return False
