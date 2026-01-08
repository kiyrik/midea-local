"""Midea local C3 message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

from .const import C3SilentLevel

TEMP_NEG_VALUE = 127


def s8(val: int) -> int:
    """Return signed int8 (-128..127) from a single byte value."""
    return ((val + 128) & 0xFF) - 128


class MessageC3Base(MessageRequest):
    """C3 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize C3 message base."""
        super().__init__(
            device_type=DeviceType.C3,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageC3Base):
    """C3 message query."""

    def __init__(self, protocol_version: int, body_type: ListTypes) -> None:
        """Initialize C3 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageQueryBasic(MessageQuery):
    """C3 Message query basic."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query basic."""
        super().__init__(protocol_version, ListTypes.X01)


class MessageQuerySilence(MessageQuery):
    """C3 Message query silence."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X05)


class MessageQueryECO(MessageQuery):
    """C3 Message query ECO."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X07)


class MessageQueryInstall(MessageQuery):
    """C3 Message query INSTALL."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X08)


class MessageQueryDisinfect(MessageQuery):
    """C3 Message query Disinfect."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X09)


class MessageQueryUnitPara(MessageQuery):
    """C3 Message query UNITPARA."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X10)


class MessageQueryHMIPara(MessageQuery):
    """C3 Message query HMIPARA."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message query silence."""
        super().__init__(protocol_version, ListTypes.X0A)


class MessageSet(MessageC3Base):
    """C3 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X01,
        )
        self.zone1_power = False
        self.zone2_power = False
        self.dhw_power = False
        self.mode = 0
        self.zone_target_temp = [25.0, 25.0]
        self.dhw_target_temp = 40.0
        self.room_target_temp = 25.0
        self.zone1_curve = False
        self.zone2_curve = False
        self.fast_dhw = False
        self.tbh = False
        # Optional extended fields
        self.zone1_curve_type: int | None = None
        self.zone2_curve_type: int | None = None

    @property
    def _body(self) -> bytearray:
        # Byte 1
        zone1_power = 0x01 if self.zone1_power else 0x00
        zone2_power = 0x02 if self.zone2_power else 0x00
        dhw_power = 0x04 if self.dhw_power else 0x00
        # Byte 7
        zone1_curve = 0x01 if self.zone1_curve else 0x00
        zone2_curve = 0x02 if self.zone2_curve else 0x00
        tbh = 0x04 if self.tbh else 0x00
        fast_dhw = 0x08 if self.fast_dhw else 0x00
        room_target_temp = int(self.room_target_temp * 2)
        zone1_target_temp = int(self.zone_target_temp[0])
        zone2_target_temp = int(self.zone_target_temp[1])
        dhw_target_temp = int(self.dhw_target_temp)
        parts = [
            zone1_power | zone2_power | dhw_power,
            self.mode,
            zone1_target_temp,
            zone2_target_temp,
            dhw_target_temp,
            room_target_temp,
            zone1_curve | zone2_curve | tbh | fast_dhw,
        ]
        # If curve types are provided, append them as extended bytes
        if self.zone1_curve_type is not None or self.zone2_curve_type is not None:
            parts.append(int(self.zone1_curve_type or 0) & 0xFF)
            parts.append(int(self.zone2_curve_type or 0) & 0xFF)
        return bytearray(parts)


class MessageSetSilent(MessageC3Base):
    """C3 message set silent."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message set silent."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X05,
        )
        self.silent_mode = False
        self.silent_level = C3SilentLevel.OFF

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                self.silent_level if self.silent_mode else C3SilentLevel.OFF,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )


class MessageSetECO(MessageC3Base):
    """C3 message set eco."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message set eco."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X07,
        )
        self.eco_mode = False

    @property
    def _body(self) -> bytearray:
        eco_mode = 0x01 if self.eco_mode else 0

        return bytearray([eco_mode, 0x00, 0x00, 0x00, 0x00, 0x00])


class MessageSetDisinfect(MessageC3Base):
    """C3 message set Disinfect."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize C3 message set eco."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X09,
        )
        self.disinfect = False

    @property
    def _body(self) -> bytearray:
        disinfect = 0x01 if self.disinfect else 0

        return bytearray([disinfect, 0x00, 0x00, 0x00])


class C3BasicBody(MessageBody):
    """C3 Basic message body."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 message body."""
        super().__init__(body)
        # BodyBytes 1
        self.zone1_power = body[data_offset + 0] & 0x01 > 0
        self.zone2_power = body[data_offset + 0] & 0x02 > 0
        self.dhw_power = body[data_offset + 0] & 0x04 > 0
        self.zone1_curve = body[data_offset + 0] & 0x08 > 0
        self.zone2_curve = body[data_offset + 0] & 0x10 > 0
        self.tbh = body[data_offset + 0] & 0x20 > 0
        self.fast_dhw = body[data_offset + 0] & 0x40 > 0
        self.remote_onoff = body[data_offset + 0] & 0x80 > 0
        # BodyBytes 2
        self.heat = body[data_offset + 1] & 0x01 > 0
        self.cool = body[data_offset + 1] & 0x02 > 0
        self.dhw = body[data_offset + 1] & 0x04 > 0
        self.double_zone = body[data_offset + 1] & 0x08 > 0
        self.zone_temp_type = [
            body[data_offset + 1] & 0x10 > 0,
            body[data_offset + 1] & 0x20 > 0,
        ]
        self.room_thermal_support = body[data_offset + 1] & 0x40 > 0
        self.room_thermal_state = body[data_offset + 1] & 0x80 > 0
        # BodyBytes 3
        self.time_set = body[data_offset + 2] & 0x01 > 0
        self.silent_mode = body[data_offset + 2] & 0x02 > 0
        self.holiday_on = body[data_offset + 2] & 0x04 > 0
        self.eco_mode = body[data_offset + 2] & 0x08 > 0
        self.zone_terminal_type = body[data_offset + 2]
        # BodyBytes 4
        self.mode = body[data_offset + 3]
        self.mode_auto = body[data_offset + 4]
        # zone1, zone2
        self.zone_target_temp = [
            float(body[data_offset + 5]),
            float(body[data_offset + 6]),
        ]
        self.dhw_target_temp = float(body[data_offset + 7])
        self.room_target_temp = float(body[data_offset + 8] / 2)
        # zone1, zone2
        self.zone_heating_temp_max = [
            float(body[data_offset + 9]),
            float(body[data_offset + 13]),
        ]
        self.zone_heating_temp_min = [
            float(body[data_offset + 10]),
            float(body[data_offset + 14]),
        ]
        self.zone_cooling_temp_max = [
            float(body[data_offset + 11]),
            float(body[data_offset + 15]),
        ]
        self.zone_cooling_temp_min = [
            float(body[data_offset + 12]),
            float(body[data_offset + 16]),
        ]
        self.room_temp_max = float(body[data_offset + 17] / 2)
        self.room_temp_min = float(body[data_offset + 18] / 2)
        self.dhw_temp_max = float(body[data_offset + 19])
        self.dhw_temp_min = float(body[data_offset + 20])
        self.tank_actual_temperature = float(body[data_offset + 21])
        self.error_code = body[data_offset + 22]
        self.tbh_control = body[data_offset + 23] & 0x80 > 0
        self.SysEnergyAnaEN = body[data_offset + 23] & 0x20 > 0
        self.HMIEnergyAnaSetEN = body[data_offset + 23] & 0x40 > 0
        # Optional extended curve type fields if present (Lua: [25], [26])
        try:
            if len(body) >= (data_offset + 26):
                self.zone1_curve_type = body[data_offset + 24]
                self.zone2_curve_type = body[data_offset + 25]
        except Exception:
            pass


class C3EnergyBody(MessageBody):
    """C3 Energy MSG_TYPE_UP_POWER4 message body."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 notify1 message body."""
        super().__init__(body)
        status_byte = body[data_offset]
        # bit0
        self.status_heating = (status_byte & 0x01) > 0
        # bit1
        self.status_cool = (status_byte & 0x02) > 0
        # bit2
        self.status_dhw = (status_byte & 0x04) > 0
        # bit3
        self.status_tbh = (status_byte & 0x08) > 0
        # bit4
        self.status_ibh = (status_byte & 0x10) > 0
        # total_energy_consumption
        self.total_energy_consumption = (
            (body[data_offset + 1] << 32)
            + (body[data_offset + 2] << 16)
            + (body[data_offset + 3] << 8)
            + (body[data_offset + 4])
        )
        # total_produced_energy
        self.total_produced_energy = (
            (body[data_offset + 5] << 32)
            + (body[data_offset + 6] << 16)
            + (body[data_offset + 7] << 8)
            + (body[data_offset + 8])
        )

        self.outdoor_temperature = float(s8(body[data_offset + 9]))
        self.zone1_temp_set = float(body[data_offset + 10])
        self.zone2_temp_set = float(body[data_offset + 11])
        self.t5s = body[data_offset + 12]
        self.tas = body[data_offset + 13]


class C3SilenceBody(MessageBody):
    """C3 Silence message body."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 query silence message body."""
        super().__init__(body)
        self.silent_mode = body[data_offset] & 0x1 > 0
        self.silent_level = C3SilentLevel(
            (body[data_offset] & 0x1) + ((body[data_offset] & 0x8) >> 2)
            if self.silent_mode
            else C3SilentLevel.OFF.value,
        ).name
        # Message protocol information:
        # silence_function_state: Byte 1, BIT 0
        # silence_timer1_state: Byte 1, BIT 1
        # silence_timer2_state: Byte 1, BIT 2
        # silence_function_level: Byte 1, BIT 3
        # silence_timer1_starthour: Byte 2
        # silence_timer1_startmin: Byte 3
        # silence_timer1_endhour: Byte 4
        # silence_timer1_endmin: Byte 5
        # silence_timer2_starthour: Byte 6
        # silence_timer2_startmin: Byte 7
        # silence_timer2_endhour: Byte 8
        # silence_timer2_endmin: Byte 9


class C3ECOBody(MessageBody):
    """C3 ECO message body."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 ECO message body."""
        super().__init__(body)
        self.eco_function_state = body[data_offset] & 0x01 > 0
        self.eco_timer_state = body[data_offset] & 0x02 > 0


class C3DisinfectBody(MessageBody):
    """C3 Disinfect message body."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 Disinfect message body."""
        super().__init__(body)
        self.disinfect = body[data_offset] & 0x01 > 0
        self.disinfect_run = body[data_offset] & 0x02 > 0
        self.disinfect_set_weekday = body[data_offset + 1]
        self.disinfect_start_hour = body[data_offset + 2]
        self.disinfect_start_minutes = body[data_offset + 3]


class C3UnitParaBody(MessageBody):
    """C3 UnitPara message body for QUERY responses (X10)."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 UnitPara message body."""
        super().__init__(body)
        self.comp_run_freq = body[data_offset]
        self.unit_mode_run = body[data_offset + 1]
        self.fan_speed = body[data_offset + 2] * 10
        self.fg_capacity_need = body[data_offset + 5]
        self.temp_t3_outdoor_exchanger = s8(body[data_offset + 6])
        self.temp_t4_outdoor_air = s8(body[data_offset + 7])
        self.temp_tp_comp_discharge = s8(body[data_offset + 8])
        self.temp_tw_in = s8(body[data_offset + 9])
        self.temp_tw_out = s8(body[data_offset + 10])
        self.temp_tsolar = body[data_offset + 11]
        self.hydbox_subtype = body[data_offset + 12]
        self.fg_usb_info_connect = body[data_offset + 13]
        # self.usb_index_max  body[data_offset + 14]
        self.odu_comp_current = body[data_offset + 16]
        self.odu_voltage = body[data_offset + 17] * 256 + body[data_offset + 18]
        self.exv_steps = body[data_offset + 19] * 256 + body[data_offset + 20]
        self.odu_model = body[data_offset + 21]
        # self.unit_online_num  body[data_offset + 22]
        # self.current_code  body[data_offset + 23]
        self.temp_t1_leaving_water = s8(body[data_offset + 33])
        self.temp_tw2 = s8(body[data_offset + 34])
        self.temp_t2_plate_f_out = s8(body[data_offset + 35])
        self.temp_t2b_plate_f_in = s8(body[data_offset + 36])
        self.temp_t5_tank = s8(body[data_offset + 37])
        self.temp_ta_room = s8(body[data_offset + 38])
        self.temp_tb_t1 = body[data_offset + 39]
        self.temp_tb_t2 = body[data_offset + 40]
        self.hydrobox_capacity = body[data_offset + 41]
        self.pressure_high = body[data_offset + 42] * 256 + body[data_offset + 43]
        self.pressure_low = body[data_offset + 44] * 256 + body[data_offset + 45]
        self.temp_th_comp_suction = s8(body[data_offset + 46])
        self.machine_type = body[data_offset + 47]
        self.odu_target_fre = body[data_offset + 48]
        self.dc_current = body[data_offset + 49]
        self.dc_bus_voltage = int(body[data_offset + 50]) * 10
        self.temp_tf_sensor = s8(body[data_offset + 51])
        self.idu_t1s1 = body[data_offset + 52]
        self.idu_t1s2 = body[data_offset + 53]
        # Water flow raw counter; use water_flow_m3h for scaled value (m3/h)
        self.water_flower = body[data_offset + 54] * 256 + body[data_offset + 55]
        self.odu_plan_vol_lmt = body[data_offset + 56]
        self.current_unit_capacity = (
            (body[data_offset + 57] << 8) + body[data_offset + 58]
        )
        self.sphera_ahs_voltage = body[data_offset + 59]
        self.temp_t4_average = body[data_offset + 60]
        self.water_pressure = body[data_offset + 61] * 256 + body[data_offset + 62]
        self.room_rel_hum = body[data_offset + 63]
        self.pwm_pump_out = body[data_offset + 63]
        self.total_electricity0 = (
            (body[data_offset + 66] << 32)
            + (body[data_offset + 67] << 16)
            + (body[data_offset + 68] << 8)
            + (body[data_offset + 69])
        )
        self.total_thermal0 = (
            (body[data_offset + 70] << 32)
            + (body[data_offset + 71] << 16)
            + (body[data_offset + 72] << 8)
            + (body[data_offset + 73])
        )
        self.heat_elec_total_consum0 = (
            (body[data_offset + 74] << 32)
            + (body[data_offset + 75] << 16)
            + (body[data_offset + 76] << 8)
            + (body[data_offset + 77])
        )
        self.heat_elec_total_capacity0 = (
            (body[data_offset + 78] << 32)
            + (body[data_offset + 79] << 16)
            + (body[data_offset + 80] << 8)
            + (body[data_offset + 81])
        )
        self.instant_power0 = ((body[data_offset + 82] << 8) + (body[data_offset + 83])) * 10
        self.instant_renew_power0 = ((body[data_offset + 84] << 8) + (
            body[data_offset + 85]
        )) * 10
        self.total_renew_power0 = (
            body[data_offset + 86] * 16777216
            + body[data_offset + 87] * 65536
            + body[data_offset + 88] * 256
            + body[data_offset + 89]
        ) * 10
        # Additional flags decoded from UnitPara (per Lua mapping)
        try:
            self.defrosting_status = (body[data_offset + 28] & 0x02) > 0
            self.back_oil = (body[data_offset + 28] & 0x08) > 0  # fgBackOil, BIT3
            self.tbh_enable = (body[data_offset + 29] & 0x80) > 0  # fgTBHEnable, BIT7
            self.ibh1_enable = (body[data_offset + 29] & 0x04) > 0  # fgIBH1Enable, BIT2
            self.dhw_run = (body[data_offset + 30] & 0x20) > 0  # fgDHWRun, BIT5
            self.heat_run = (body[data_offset + 30] & 0x10) > 0  # fgHeatRun, BIT4
            self.cool_run = (body[data_offset + 30] & 0x08) > 0  # fgCoolRun, BIT3
            self.tbh_output = (body[data_offset + 32] & 0x04) > 0  # fgTBHOutput, BIT2
            self.ibh2_output = (body[data_offset + 32] & 0x02) > 0  # fgIBH2Output, BIT1
            self.ibh1_output = (body[data_offset + 32] & 0x01) > 0  # fgIBH1Output, BIT0
        except Exception:
            pass

        # Scale some fields for easier use
        self.water_flow_m3h = float(self.water_flower) / 100.0
        self.current_unit_capacity_kw = float(self.current_unit_capacity) / 100.0


class C3UnitParaBodyNotify(MessageBody):
    """C3 UnitPara body for UP/notify frames (same body type 0x10, message_type notify1)."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 UnitPara notify body."""
        super().__init__(body)
        # Core runtime fields (same layout as Lua UP UNITPARA)
        self.comp_run_freq = body[data_offset + 0]
        self.fan_speed = body[data_offset + 1] * 10
        self.temp_t3_outdoor_exchanger = s8(body[data_offset + 2])
        self.temp_t4_outdoor_air = s8(body[data_offset + 3])
        self.temp_tp_comp_discharge = s8(body[data_offset + 4])
        self.temp_tw_in = s8(body[data_offset + 5])
        self.temp_tw_out = s8(body[data_offset + 6])
        self.odu_comp_current = body[data_offset + 7]
        self.odu_voltage = body[data_offset + 8] * 256 + body[data_offset + 9]
        self.temp_t1_leaving_water = s8(body[data_offset + 10])
        # self.temp_tw2 = s8(body[data_offset + 11])  # not exposed
        self.temp_t2_plate_f_out = s8(body[data_offset + 12])
        self.temp_t2b_plate_f_in = s8(body[data_offset + 13])
        self.temp_t5_tank = s8(body[data_offset + 14])
        self.temp_ta_room = s8(body[data_offset + 15])
        self.pressure_high = body[data_offset + 16] * 256 + body[data_offset + 17]
        self.pressure_low = body[data_offset + 18] * 256 + body[data_offset + 19]
        self.temp_th_comp_suction = s8(body[data_offset + 20])
        self.odu_target_fre = body[data_offset + 21]
        self.temp_tf_sensor = s8(body[data_offset + 22])
        self.idu_t1s1 = body[data_offset + 23]
        self.idu_t1s2 = body[data_offset + 24]
        self.water_flower = body[data_offset + 25] * 256 + body[data_offset + 26]
        self.water_flow_m3h = float(self.water_flower) / 100.0
        self.current_unit_capacity = (
            (body[data_offset + 27] << 8) + body[data_offset + 28]
        )
        self.current_unit_capacity_kw = float(self.current_unit_capacity) / 100.0
        self.water_pressure = body[data_offset + 29] * 256 + body[data_offset + 30]
        self.room_rel_hum = body[data_offset + 31]
        self.total_electricity0 = (
            (body[data_offset + 32] << 24)
            + (body[data_offset + 33] << 16)
            + (body[data_offset + 34] << 8)
            + (body[data_offset + 35])
        )
        self.total_thermal0 = (
            (body[data_offset + 36] << 24)
            + (body[data_offset + 37] << 16)
            + (body[data_offset + 38] << 8)
            + (body[data_offset + 39])
        )
        # self.sys_heat_day_capacity = (body[data_offset + 40] << 8) + body[data_offset + 41]
        self.sys_heat_day_renew_power = (
            (body[data_offset + 42] << 8) + body[data_offset + 43]
        )
        self.sys_heat_day_elec_consum = (
            (body[data_offset + 44] << 8) + body[data_offset + 45]
        )
        self.sys_heat_day_copeer = (
            (body[data_offset + 46] << 8) + body[data_offset + 47]
        )
        self.instant_power0 = (
            (body[data_offset + 48] << 8) + body[data_offset + 49]
        ) * 10
        self.instant_renew_power0 = (
            (body[data_offset + 50] << 8) + body[data_offset + 51]
        ) * 10
        self.total_renew_power0 = (
            body[data_offset + 52] * 16777216
            + body[data_offset + 53] * 65536
            + body[data_offset + 54] * 256
            + body[data_offset + 55]
        ) * 10
        self.comp_run_total_time0 = (
            (body[data_offset + 56] << 8) + body[data_offset + 57]
        )
        # self.pwm_pump_out = body[data_offset + 58]  # not exposed
        self.unit_mode_run = body[data_offset + 59]
        # self.sys_instant_hp_capacity = (body[data_offset + 60] << 8) + body[data_offset + 61]
        self.sys_instant_renew_power = (
            (body[data_offset + 62] << 8) + body[data_offset + 63]
        )
        self.sys_instant_power = (
            (body[data_offset + 64] << 8) + body[data_offset + 65]
        )
        self.sys_instant_copeer = (
            (body[data_offset + 66] << 8) + body[data_offset + 67]
        )
        # self.sys_total_hp_capacity = (
        #     body[data_offset + 68] * 16777216
        #     + body[data_offset + 69] * 65536
        #     + body[data_offset + 70] * 256
        #     + body[data_offset + 71]
        # )
        # self.sys_total_heat_capacity = (
        #     body[data_offset + 72] * 16777216
        #     + body[data_offset + 73] * 65536
        #     + body[data_offset + 74] * 256
        #     + body[data_offset + 75]
        # )
        # self.sys_total_power_consum = (
        #     body[data_offset + 76] * 16777216
        #     + body[data_offset + 77] * 65536
        #     + body[data_offset + 78] * 256
        #     + body[data_offset + 79]
        # )
        self.sys_total_copeer = (
            (body[data_offset + 80] << 8) + body[data_offset + 81]
        )
        self.sys_heat_ins_hp_capacity = (body[data_offset + 82] << 8) + body[data_offset + 83]
        self.sys_heat_ins_renew_power = (body[data_offset + 84] << 8) + body[data_offset + 85]
        self.sys_heat_ins_power = (body[data_offset + 86] << 8) + body[data_offset + 87]
        self.sys_heat_ins_copeer = (body[data_offset + 88] << 8) + body[data_offset + 89]
        self.sys_heat_capacity = (
            body[data_offset + 90] * 16777216
            + body[data_offset + 91] * 65536
            + body[data_offset + 92] * 256
            + body[data_offset + 93]
        )
        self.sys_heat_renew_power = (
            body[data_offset + 94] * 16777216
            + body[data_offset + 95] * 65536
            + body[data_offset + 96] * 256
            + body[data_offset + 97]
        )
        self.sys_heat_elec_consum = (
            body[data_offset + 98] * 16777216
            + body[data_offset + 99] * 65536
            + body[data_offset + 100] * 256
            + body[data_offset + 101]
        )
        self.sys_heat_copeer = (body[data_offset + 102] << 8) + body[data_offset + 103]
        # self.sys_cool_ins_hp_capacity = (body[data_offset + 104] << 8) + body[data_offset + 105]
        # self.sys_cool_ins_renew_power = (body[data_offset + 106] << 8) + body[data_offset + 107]
        # self.sys_cool_ins_power = (body[data_offset + 108] << 8) + body[data_offset + 109]
        # self.sys_cool_ins_copeer = (body[data_offset + 110] << 8) + body[data_offset + 111]
        # self.sys_cool_capacity = (
        #     body[data_offset + 112] * 16777216
        #     + body[data_offset + 113] * 65536
        #     + body[data_offset + 114] * 256
        #     + body[data_offset + 115]
        # )
        # self.sys_cool_renew_power = (
        #     body[data_offset + 116] * 16777216
        #     + body[data_offset + 117] * 65536
        #     + body[data_offset + 118] * 256
        #     + body[data_offset + 119]
        # )
        # self.sys_cool_elec_consum = (
        #     body[data_offset + 120] * 16777216
        #     + body[data_offset + 121] * 65536
        #     + body[data_offset + 122] * 256
        #     + body[data_offset + 123]
        # )
        # self.sys_cool_copeer = (body[data_offset + 124] << 8) + body[data_offset + 125]
        # self.sys_dhw_ins_hp_capacity = (body[data_offset + 126] << 8) + body[data_offset + 127]
        # self.sys_dhw_ins_renew_power = (body[data_offset + 128] << 8) + body[data_offset + 129]
        # self.sys_dhw_ins_power = (body[data_offset + 130] << 8) + body[data_offset + 131]
        # self.sys_dhw_ins_copeer = (body[data_offset + 132] << 8) + body[data_offset + 133]
        # self.sys_dhw_capacity = (
        #     body[data_offset + 134] * 16777216
        #     + body[data_offset + 135] * 65536
        #     + body[data_offset + 136] * 256
        #     + body[data_offset + 137]
        # )
        # self.sys_dhw_renew_power = (
        #     body[data_offset + 138] * 16777216
        #     + body[data_offset + 139] * 65536
        #     + body[data_offset + 140] * 256
        #     + body[data_offset + 141]
        # )
        # self.sys_dhw_elec_consum = (
        #     body[data_offset + 142] * 16777216
        #     + body[data_offset + 143] * 65536
        #     + body[data_offset + 144] * 256
        #     + body[data_offset + 145]
        # )
        # self.sys_dhw_copeer = (body[data_offset + 146] << 8) + body[data_offset + 147]
        # self.sys_energy_ana_en = body[data_offset + 148] & 0x01
        # self.hmi_energy_ana_set_en = body[data_offset + 148] & 0x02
        # self.sys_heat_week_capacity = (body[data_offset + 149] << 8) + body[data_offset + 150]
        # self.sys_heat_week_renew_power = (body[data_offset + 151] << 8) + body[data_offset + 152]
        # self.sys_heat_week_elec_consum = (body[data_offset + 153] << 8) + body[data_offset + 154]
        # self.sys_heat_week_copeer = (body[data_offset + 155] << 8) + body[data_offset + 156]
        # self.sys_heat_month_capacity = (body[data_offset + 157] << 8) + body[data_offset + 158]
        # self.sys_heat_month_renew_power = (body[data_offset + 159] << 8) + body[data_offset + 160]
        # self.sys_heat_month_elec_consum = (body[data_offset + 161] << 8) + body[data_offset + 162]
        # self.sys_heat_month_copeer = (body[data_offset + 163] << 8) + body[data_offset + 164]
        # self.sys_heat_year_capacity = (body[data_offset + 165] << 8) + body[data_offset + 166]
        # self.sys_heat_year_renew_power = (body[data_offset + 167] << 8) + body[data_offset + 168]
        # self.sys_heat_year_elec_consum = (body[data_offset + 169] << 8) + body[data_offset + 170]
        # self.sys_heat_year_copeer = (body[data_offset + 171] << 8) + body[data_offset + 172]
        # self.sys_cool_day_capacity = (body[data_offset + 173] << 8) + body[data_offset + 174]
        # self.sys_cool_day_renew_power = (body[data_offset + 175] << 8) + body[data_offset + 176]
        # self.sys_cool_day_elec_consum = (body[data_offset + 177] << 8) + body[data_offset + 178]
        # self.sys_cool_day_copeer = (body[data_offset + 179] << 8) + body[data_offset + 180]
        # self.sys_cool_week_capacity = (body[data_offset + 181] << 8) + body[data_offset + 182]
        # self.sys_cool_week_renew_power = (body[data_offset + 183] << 8) + body[data_offset + 184]
        # self.sys_cool_week_elec_consum = (body[data_offset + 185] << 8) + body[data_offset + 186]
        # self.sys_cool_week_copeer = (body[data_offset + 187] << 8) + body[data_offset + 188]
        # self.sys_cool_month_capacity = (body[data_offset + 189] << 8) + body[data_offset + 190]
        # self.sys_cool_month_renew_power = (body[data_offset + 191] << 8) + body[data_offset + 192]
        # self.sys_cool_month_elec_consum = (body[data_offset + 193] << 8) + body[data_offset + 194]
        # self.sys_cool_month_copeer = (body[data_offset + 195] << 8) + body[data_offset + 196]
        # self.sys_cool_year_capacity = (body[data_offset + 197] << 8) + body[data_offset + 198]
        # self.sys_cool_year_renew_power = (body[data_offset + 199] << 8) + body[data_offset + 200]
        # self.sys_cool_year_elec_consum = (body[data_offset + 201] << 8) + body[data_offset + 202]
        # self.sys_cool_year_copeer = (body[data_offset + 203] << 8) + body[data_offset + 204]
        # self.sys_dhw_day_capacity = (body[data_offset + 205] << 8) + body[data_offset + 206]
        # self.sys_dhw_day_renew_power = (body[data_offset + 207] << 8) + body[data_offset + 208]
        # self.sys_dhw_day_elec_consum = (body[data_offset + 209] << 8) + body[data_offset + 210]
        # self.sys_dhw_day_copeer = (body[data_offset + 211] << 8) + body[data_offset + 212]
        # self.sys_dhw_week_capacity = (body[data_offset + 213] << 8) + body[data_offset + 214]
        # self.sys_dhw_week_renew_power = (body[data_offset + 215] << 8) + body[data_offset + 216]
        # self.sys_dhw_week_elec_consum = (body[data_offset + 217] << 8) + body[data_offset + 218]
        # self.sys_dhw_week_copeer = (body[data_offset + 219] << 8) + body[data_offset + 220]
        # self.sys_dhw_month_capacity = (body[data_offset + 221] << 8) + body[data_offset + 222]
        # self.sys_dhw_month_renew_power = (body[data_offset + 223] << 8) + body[data_offset + 224]
        # self.sys_dhw_month_elec_consum = (body[data_offset + 225] << 8) + body[data_offset + 226]
        # self.sys_dhw_month_copeer = (body[data_offset + 227] << 8) + body[data_offset + 228]
        # self.sys_dhw_year_capacity = (body[data_offset + 229] << 8) + body[data_offset + 230]
        # self.sys_dhw_year_renew_power = (body[data_offset + 231] << 8) + body[data_offset + 232]
        # self.sys_dhw_year_elec_consum = (body[data_offset + 233] << 8) + body[data_offset + 234]
        # self.sys_dhw_year_copeer = (body[data_offset + 235] << 8) + body[data_offset + 236]


class C3HMIParaBody(MessageBody):
    """C3 HMIPara message body (QUERY HMIPARA, body type 0x0A)."""

    def __init__(self, body: bytearray, data_offset: int = 0) -> None:
        """Initialize C3 HMIPara message body."""
        super().__init__(body)
        self.hmi_version_num = body[data_offset + 0]
        self.comp_run_cur_time0 = (body[data_offset + 1] << 8) + body[data_offset + 2]
        self.comp_run_total_time0 = (body[data_offset + 3] << 8) + body[data_offset + 4]
        self.fan_run_total_time0 = (body[data_offset + 5] << 8) + body[data_offset + 6]
        self.pumpi_run_total_time0 = (body[data_offset + 7] << 8) + body[data_offset + 8]
        self.ibh1_run_total_time0 = (body[data_offset + 9] << 8) + body[data_offset + 10]
        self.ibh2_run_total_time0 = (body[data_offset + 11] << 8) + body[data_offset + 12]
        self.tbh_run_total_time0 = (body[data_offset + 13] << 8) + body[data_offset + 14]
        self.ahs_run_total_time0 = (body[data_offset + 15] << 8) + body[data_offset + 16]
        # Phone/service arrays and warning history follow; keep as reference only
        # self.array_service_tel0 = body[data_offset + 17]
        # self.array_service_tel1 = body[data_offset + 18]
        # ...
        # self.array_service_tel12 = body[data_offset + 29]
        # self.array_service_cel0 = body[data_offset + 30]
        # self.array_service_cel1 = body[data_offset + 31]
        # ...
        # self.array_service_cel12 = body[data_offset + 42]
        # self.u8_warn_total = body[data_offset + 43]
        # self.code_err_prot1 = body[data_offset + 44]
        # self.warn_address1 = body[data_offset + 45]
        # self.warn_hour1 = body[data_offset + 46]
        # self.warn_min1 = body[data_offset + 47]
        # self.warn_year1 = body[data_offset + 48]
        # self.warn_month1 = body[data_offset + 49]
        # self.warn_date1 = body[data_offset + 50]
        # self.code_err_prot2 = body[data_offset + 51]
        # self.warn_address2 = body[data_offset + 52]
        # self.warn_hour2 = body[data_offset + 53]
        # self.warn_min2 = body[data_offset + 54]
        # self.warn_year2 = body[data_offset + 55]
        # self.warn_month2 = body[data_offset + 56]
        # self.warn_date2 = body[data_offset + 57]
        # self.code_err_prot3 = body[data_offset + 58]
        # self.warn_address3 = body[data_offset + 59]
        # self.warn_hour3 = body[data_offset + 60]
        # self.warn_min3 = body[data_offset + 61]
        # self.warn_year3 = body[data_offset + 62]
        # self.warn_month3 = body[data_offset + 63]
        # self.warn_date3 = body[data_offset + 64]
        # self.code_err_prot4 = body[data_offset + 65]
        # self.warn_address4 = body[data_offset + 66]
        # self.warn_hour4 = body[data_offset + 67]
        # self.warn_min4 = body[data_offset + 68]
        # self.warn_year4 = body[data_offset + 69]
        # self.warn_month4 = body[data_offset + 70]
        # self.warn_date4 = body[data_offset + 71]
        # self.code_err_prot5 = body[data_offset + 72]
        # self.warn_address5 = body[data_offset + 73]
        # self.warn_hour5 = body[data_offset + 74]
        # self.warn_min5 = body[data_offset + 75]
        # self.warn_year5 = body[data_offset + 76]
        # self.warn_month5 = body[data_offset + 77]
        # self.warn_date5 = body[data_offset + 78]
        # self.code_err_prot6 = body[data_offset + 79]
        # self.warn_address6 = body[data_offset + 80]
        # self.warn_hour6 = body[data_offset + 81]
        # self.warn_min6 = body[data_offset + 82]
        # self.warn_year6 = body[data_offset + 83]
        # self.warn_month6 = body[data_offset + 84]
        # self.warn_date6 = body[data_offset + 85]
        # self.code_err_prot7 = body[data_offset + 86]
        # self.warn_address7 = body[data_offset + 87]
        # self.warn_hour7 = body[data_offset + 88]
        # self.warn_min7 = body[data_offset + 89]
        # self.warn_year7 = body[data_offset + 90]
        # self.warn_month7 = body[data_offset + 91]
        # self.warn_date7 = body[data_offset + 92]
        # self.code_err_prot8 = body[data_offset + 93]
        # self.warn_address8 = body[data_offset + 94]
        # self.warn_hour8 = body[data_offset + 95]
        # self.warn_min8 = body[data_offset + 96]
        # self.warn_year8 = body[data_offset + 97]
        # self.warn_month8 = body[data_offset + 98]
        # self.warn_date8 = body[data_offset + 99]


class MessageC3Response(MessageResponse):
    """C3 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize C3 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type
            in [MessageType.set, MessageType.notify1, MessageType.query]
            and self.body_type == ListTypes.X01
        ) or self.message_type == MessageType.notify2:
            self.set_body(C3BasicBody(super().body, data_offset=1))
        elif (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.X04
        ):
            self.set_body(C3EnergyBody(super().body, data_offset=1))
        elif self.message_type == MessageType.query and self.body_type == ListTypes.X05:
            self.set_body(C3SilenceBody(super().body, data_offset=1))
        elif self.body_type == ListTypes.X07:
            self.set_body(C3ECOBody(super().body, data_offset=1))
        elif self.body_type == ListTypes.X09:
            self.set_body(C3DisinfectBody(super().body, data_offset=1))
        elif self.message_type == MessageType.query and self.body_type == ListTypes.X0A:
            self.set_body(C3HMIParaBody(super().body, data_offset=1))
        elif self.body_type == ListTypes.X05 and self.message_type == MessageType.notify1:
            self.set_body(C3UnitParaBodyNotify(super().body, data_offset=1))
        elif self.body_type == ListTypes.X10 and self.message_type == MessageType.query:
            self.set_body(C3UnitParaBody(super().body, data_offset=1))
        self.set_attr()
