"""Midea local C3 device const."""

from enum import IntEnum, StrEnum


class DeviceAttributes(StrEnum):
    """Midea C3 device attributes."""

    zone1_power = "zone1_power"
    zone2_power = "zone2_power"
    dhw_power = "dhw_power"
    zone1_curve = "zone1_curve"
    zone2_curve = "zone2_curve"
    disinfect = "disinfect"
    fast_dhw = "fast_dhw"
    zone_temp_type = "zone_temp_type"
    zone1_room_temp_mode = "zone1_room_temp_mode"
    zone2_room_temp_mode = "zone2_room_temp_mode"
    zone1_water_temp_mode = "zone1_water_temp_mode"
    zone2_water_temp_mode = "zone2_water_temp_mode"
    mode = "mode"
    mode_auto = "mode_auto"
    zone_target_temp = "zone_target_temp"
    dhw_target_temp = "dhw_target_temp"
    room_target_temp = "room_target_temp"
    zone_heating_temp_max = "zone_heating_temp_max"
    zone_heating_temp_min = "zone_heating_temp_min"
    zone_cooling_temp_max = "zone_cooling_temp_max"
    zone_cooling_temp_min = "zone_cooling_temp_min"
    tank_actual_temperature = "tank_actual_temperature"
    room_temp_max = "room_temp_max"
    room_temp_min = "room_temp_min"
    dhw_temp_max = "dhw_temp_max"
    dhw_temp_min = "dhw_temp_min"
    target_temperature = "target_temperature"
    temperature_max = "temperature_max"
    temperature_min = "temperature_min"
    status_heating = "status_heating"
    status_dhw = "status_dhw"
    status_tbh = "status_tbh"
    status_ibh = "status_ibh"
    total_energy_consumption = "total_energy_consumption"
    total_produced_energy = "total_produced_energy"
    outdoor_temperature = "outdoor_temperature"
    silent_mode = "silent_mode"
    SILENT_LEVEL = "silent_level"
    eco_mode = "eco_mode"
    tbh = "tbh"
    error_code = "error_code"
    defrosting_status = "defrosting_status"
    unit_mode_run = "unit_mode_run"
    comp_run_freq = "comp_run_freq"
    exv_steps = "exv_steps"
    pressure_high = "pressure_high"
    pressure_low = "pressure_low"
    water_flower = "water_flower"
    water_flow_m3h = "water_flow_m3h"
    water_pressure = "water_pressure"
    fan_speed = "fan_speed"
    supply_voltage = "supply_voltage"
    dc_current = "dc_current"
    odu_comp_current = "odu_comp_current"
    current_unit_capacity_kw = "current_unit_capacity_kw"
    dc_bus_voltage = "dc_bus_voltage"
    current_unit_capacity = "current_unit_capacity"
    # Capacity demand from UNITPARA (byte 5)
    fg_capacity_need = "fg_capacity_need"
    temp_t4_outdoor_air = "temp_t4_outdoor_air"
    temp_t5_tank = "temp_t5_tank"
    temp_tw_in = "temp_tw_in"
    temp_tw_out = "temp_tw_out"
    temp_t1_leaving_water = "temp_t1_leaving_water"
    temp_t2_plate_f_out = "temp_t2_plate_f_out"
    temp_t2b_plate_f_in = "temp_t2b_plate_f_in"
    temp_t3_outdoor_exchanger = "temp_t3_outdoor_exchanger"
    # TA is room temperature when room thermostat is enabled
    temp_ta_room = "temp_ta_room"
    temp_th_comp_suction = "temp_th_comp_suction"
    temp_tp_comp_discharge = "temp_tp_comp_discharge"
    temp_tf_sensor = "temp_tf_sensor"
    # Averaged outdoor air (T4) value reported by UNITPARA
    temp_t4_average = "temp_t4_average"
    # IDU curve-derived setpoint (from UNITPARA X10)
    idu_t1s1 = "idu_t1s1"
    # running mode as human readable text derived from flags
    running_mode_text = "running_mode_text"
    instant_power0 = "instant_power0"
    instant_renew_power0 = "instant_renew_power0"
    total_renew_power0 = "total_renew_power0"
    # Curve settings (when extended basic body is present)
    zone1_curve_type = "zone1_curve_type"
    zone2_curve_type = "zone2_curve_type"
    # Additional flags and outputs from UNITPARA
    back_oil = "back_oil"
    tbh_enable = "tbh_enable"
    ibh1_enable = "ibh1_enable"
    dhw_run = "dhw_run"
    heat_run = "heat_run"
    cool_run = "cool_run"
    tbh_output = "tbh_output"
    ibh2_output = "ibh2_output"
    ibh1_output = "ibh1_output"


class C3SilentLevel(IntEnum):
    """C3 Silent Level."""

    OFF = 0x0
    SILENT = 0x1
    SUPER_SILENT = 0x3


class C3DeviceMode(IntEnum):
    """C3 Device Mode."""

    COOL = 2
    HEAT = 3
