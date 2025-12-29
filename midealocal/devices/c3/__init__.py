"""Midea local C3 device."""

import json
import logging
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .const import C3DeviceMode, C3SilentLevel, DeviceAttributes
from .message import (
    MessageC3Response,
    MessageQuery,
    MessageQueryBasic,
    MessageQueryDisinfect,
    MessageQueryECO,
    MessageQuerySilence,
    MessageSet,
    MessageSetDisinfect,
    MessageSetECO,
    MessageSetSilent,
    MessageQueryUnitPara,
)

_LOGGER = logging.getLogger(__name__)


class MideaC3Device(MideaDevice):
    """Midea C3 device."""

    _silent_modes: ClassVar[list[str]] = [
        C3SilentLevel.OFF.name,
        C3SilentLevel.SILENT.name,
        C3SilentLevel.SUPER_SILENT.name,
    ]

    def __init__(
        self,
        name: str,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        device_protocol: ProtocolVersion,
        model: str,
        subtype: int,
        customize: str,
    ) -> None:
        """Initialize Midea C3 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.C3,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.zone1_power: False,
                DeviceAttributes.zone2_power: False,
                DeviceAttributes.dhw_power: False,
                DeviceAttributes.zone1_curve: False,
                DeviceAttributes.zone2_curve: False,
                DeviceAttributes.disinfect: False,
                DeviceAttributes.fast_dhw: False,
                DeviceAttributes.zone_temp_type: [False, False],
                DeviceAttributes.zone1_room_temp_mode: False,
                DeviceAttributes.zone2_room_temp_mode: False,
                DeviceAttributes.zone1_water_temp_mode: False,
                DeviceAttributes.zone2_water_temp_mode: False,
                DeviceAttributes.silent_mode: False,
                DeviceAttributes.SILENT_LEVEL: C3SilentLevel.OFF.name,
                DeviceAttributes.eco_mode: False,
                DeviceAttributes.tbh: False,
                DeviceAttributes.mode: 1,
                DeviceAttributes.mode_auto: 1,
                DeviceAttributes.zone_target_temp: [25.0, 25.0],
                DeviceAttributes.dhw_target_temp: 25.0,
                DeviceAttributes.room_target_temp: 30.0,
                DeviceAttributes.zone_heating_temp_max: [55.0, 55.0],
                DeviceAttributes.zone_heating_temp_min: [25.0, 25.0],
                DeviceAttributes.zone_cooling_temp_max: [25.0, 25.0],
                DeviceAttributes.zone_cooling_temp_min: [5.0, 5.0],
                DeviceAttributes.room_temp_max: 60.0,
                DeviceAttributes.room_temp_min: 34.0,
                DeviceAttributes.dhw_temp_max: 60.0,
                DeviceAttributes.dhw_temp_min: 20.0,
                DeviceAttributes.tank_actual_temperature: None,
                DeviceAttributes.target_temperature: [25.0, 25.0],
                DeviceAttributes.temperature_max: [0.0, 0.0],
                DeviceAttributes.temperature_min: [0.0, 0.0],
                DeviceAttributes.total_energy_consumption: None,
                DeviceAttributes.status_heating: None,
                DeviceAttributes.status_dhw: None,
                DeviceAttributes.status_tbh: None,
                DeviceAttributes.status_ibh: None,
                DeviceAttributes.total_produced_energy: None,
                DeviceAttributes.outdoor_temperature: None,
                DeviceAttributes.zone1_curve_type: None,
                DeviceAttributes.zone2_curve_type: None,
                DeviceAttributes.error_code: 0,
                DeviceAttributes.defrosting_status: False,
                DeviceAttributes.unit_mode_run: None,
                DeviceAttributes.comp_run_freq: None,
                DeviceAttributes.exv_steps: None,
                DeviceAttributes.pressure_high: None,
                DeviceAttributes.pressure_low: None,
                DeviceAttributes.water_flow_m3h: None,
                DeviceAttributes.water_pressure: None,
                DeviceAttributes.fan_speed: None,
                DeviceAttributes.supply_voltage: None,
                DeviceAttributes.dc_current: None,
                DeviceAttributes.odu_comp_current: None,
                DeviceAttributes.dc_bus_voltage: None,
                DeviceAttributes.current_unit_capacity: None,
                DeviceAttributes.current_unit_capacity_kw: None,
                DeviceAttributes.temp_t4: None,
                DeviceAttributes.temp_t5: None,
                DeviceAttributes.temp_tw_in: None,
                DeviceAttributes.temp_tw_out: None,
                DeviceAttributes.temp_t1: None,
                DeviceAttributes.temp_t2: None,
                DeviceAttributes.temp_t2b: None,
                DeviceAttributes.temp_t3: None,
                DeviceAttributes.temp_ta: None,
                DeviceAttributes.temp_th: None,
                DeviceAttributes.temp_tp: None,
                DeviceAttributes.temp_tf: None,
                DeviceAttributes.running_mode_text: None,
                DeviceAttributes.instant_power0: None,
                DeviceAttributes.instant_renew_power0: None,
                DeviceAttributes.back_oil: False,
                DeviceAttributes.tbh_enable: False,
                DeviceAttributes.ibh1_enable: False,
                DeviceAttributes.dhw_run: False,
                DeviceAttributes.heat_run: False,
                DeviceAttributes.cool_run: False,
                DeviceAttributes.tbh_output: False,
                DeviceAttributes.ibh2_output: False,
                DeviceAttributes.ibh1_output: False
            },
        )
        self._default_temperature_step: float = 0.5
        self._temperature_step: float = 0.5
        # Optional extra queries toggle (disabled by default)
        # Use a generic name to allow more advanced blocks later.
        self._enable_advanced_params: bool = False
        self.set_customize(customize)

    @property
    def temperature_step(self) -> float | None:
        """Midea C3 device temperature step."""
        return self._temperature_step

    @property
    def silent_modes(self) -> list[str]:
        """Midea C3 device silent modes."""
        return MideaC3Device._silent_modes

    def build_query(self) -> list[MessageQuery]:
        """Midea C3 device build query."""
        queries: list[MessageQuery] = [
            MessageQueryBasic(self._message_protocol_version),
            MessageQueryDisinfect(self._message_protocol_version),
            MessageQuerySilence(self._message_protocol_version),
            MessageQueryECO(self._message_protocol_version),
        ]
        if self._enable_advanced_params:
            queries.append(MessageQueryUnitPara(self._message_protocol_version))
        return queries

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea C3 device process message."""
        message = MessageC3Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = getattr(message, str(status))
        # Derive running mode text from basic flags when present
        try:
            heat = bool(getattr(message, "heat"))
            dhw = bool(getattr(message, "dhw"))
            cool = bool(getattr(message, "cool"))
            if dhw and heat:
                mode_txt = "DHW+HEAT"
            elif dhw:
                mode_txt = "DHW"
            elif heat:
                mode_txt = "HEAT"
            elif cool:
                mode_txt = "COOL"
            else:
                mode_txt = "IDLE"
            self._attributes[DeviceAttributes.running_mode_text] = mode_txt
            new_status[DeviceAttributes.running_mode_text.value] = mode_txt
        except Exception:
            pass
        # Fallback: if Energy body didn't provide outdoor_temperature this cycle,
        # derive from UnitPara outdoor sensor when available. Prefer T4 here,
        # as Lua maps Energy outdoor temp to T4.
        if (
            DeviceAttributes.outdoor_temperature.value not in new_status
            and hasattr(message, "temp_t4")
        ):
            self._attributes[DeviceAttributes.outdoor_temperature] = getattr(
                message, "temp_t4"
            )
            new_status[DeviceAttributes.outdoor_temperature.value] = getattr(
                message, "temp_t4"
            )
        if "zone_temp_type" in new_status:
            for zone in [0, 1]:
                if self._attributes[DeviceAttributes.zone_temp_type][
                    zone
                ]:  # Water temp mode
                    self._attributes[DeviceAttributes.target_temperature][zone] = (
                        self._attributes[DeviceAttributes.zone_target_temp][zone]
                    )
                    if (
                        self._attributes[DeviceAttributes.mode_auto]
                        == C3DeviceMode.COOL
                    ):  # cooling mode
                        self._attributes[DeviceAttributes.temperature_max][zone] = (
                            self._attributes[
                                DeviceAttributes.zone_cooling_temp_max
                            ][zone]
                        )
                        self._attributes[DeviceAttributes.temperature_min][zone] = (
                            self._attributes[
                                DeviceAttributes.zone_cooling_temp_min
                            ][zone]
                        )
                    elif (
                        self._attributes[DeviceAttributes.mode] == C3DeviceMode.HEAT
                    ):  # heating mode
                        self._attributes[DeviceAttributes.temperature_max][zone] = (
                            self._attributes[
                                DeviceAttributes.zone_heating_temp_max
                            ][zone]
                        )
                        self._attributes[DeviceAttributes.temperature_min][zone] = (
                            self._attributes[
                                DeviceAttributes.zone_heating_temp_min
                            ][zone]
                        )
                else:  # Room temp mode
                    self._attributes[DeviceAttributes.target_temperature][zone] = (
                        self._attributes[DeviceAttributes.room_target_temp]
                    )
                    self._attributes[DeviceAttributes.temperature_max][zone] = (
                        self._attributes[DeviceAttributes.room_temp_max]
                    )
                    self._attributes[DeviceAttributes.temperature_min][zone] = (
                        self._attributes[DeviceAttributes.room_temp_min]
                    )
            if self._attributes[DeviceAttributes.zone1_power]:
                if self._attributes[DeviceAttributes.zone_temp_type][zone]:
                    self._attributes[DeviceAttributes.zone1_water_temp_mode] = True
                    self._attributes[DeviceAttributes.zone1_room_temp_mode] = False
                else:
                    self._attributes[DeviceAttributes.zone1_water_temp_mode] = False
                    self._attributes[DeviceAttributes.zone1_room_temp_mode] = True
            else:
                self._attributes[DeviceAttributes.zone1_water_temp_mode] = False
                self._attributes[DeviceAttributes.zone1_room_temp_mode] = False
            if self._attributes[DeviceAttributes.zone2_power]:
                if self._attributes[DeviceAttributes.zone_temp_type][zone]:
                    self._attributes[DeviceAttributes.zone2_water_temp_mode] = True
                    self._attributes[DeviceAttributes.zone2_room_temp_mode] = False
                else:
                    self._attributes[DeviceAttributes.zone2_water_temp_mode] = False
                    self._attributes[DeviceAttributes.zone2_room_temp_mode] = True
            else:
                self._attributes[DeviceAttributes.zone2_water_temp_mode] = False
                self._attributes[DeviceAttributes.zone2_room_temp_mode] = False
            new_status[DeviceAttributes.zone1_water_temp_mode.value] = self._attributes[
                DeviceAttributes.zone1_water_temp_mode
            ]
            new_status[DeviceAttributes.zone2_water_temp_mode.value] = self._attributes[
                DeviceAttributes.zone2_water_temp_mode
            ]
            new_status[DeviceAttributes.zone1_room_temp_mode.value] = self._attributes[
                DeviceAttributes.zone1_room_temp_mode
            ]
            new_status[DeviceAttributes.zone2_room_temp_mode.value] = self._attributes[
                DeviceAttributes.zone2_room_temp_mode
            ]

        return new_status

    def make_message_set(self) -> MessageSet:
        """Midea C3 device make message set."""
        message = MessageSet(self._message_protocol_version)
        message.zone1_power = self._attributes[DeviceAttributes.zone1_power]
        message.zone2_power = self._attributes[DeviceAttributes.zone2_power]
        message.dhw_power = self._attributes[DeviceAttributes.dhw_power]
        message.mode = self._attributes[DeviceAttributes.mode]
        message.zone_target_temp = self._attributes[DeviceAttributes.zone_target_temp]
        message.dhw_target_temp = self._attributes[DeviceAttributes.dhw_target_temp]
        message.room_target_temp = self._attributes[DeviceAttributes.room_target_temp]
        message.zone1_curve = self._attributes[DeviceAttributes.zone1_curve]
        message.zone2_curve = self._attributes[DeviceAttributes.zone2_curve]
        message.tbh = self._attributes[DeviceAttributes.tbh]
        message.fast_dhw = self._attributes[DeviceAttributes.fast_dhw]
        return message

    def set_attribute(self, attr: str, value: bool | float | str) -> None:
        """Midea C3 device set attribute."""
        message: (
            MessageSet | MessageSetECO | MessageSetSilent | MessageSetDisinfect | None
        ) = None
        if attr in [
            DeviceAttributes.zone1_power,
            DeviceAttributes.zone2_power,
            DeviceAttributes.dhw_power,
            DeviceAttributes.zone1_curve,
            DeviceAttributes.zone2_curve,
            DeviceAttributes.tbh,
            DeviceAttributes.fast_dhw,
            DeviceAttributes.dhw_target_temp,
        ]:
            message = self.make_message_set()
            setattr(message, str(attr), value)
        elif attr == DeviceAttributes.eco_mode:
            message = MessageSetECO(self._message_protocol_version)
            setattr(message, str(attr), value)
        elif attr == DeviceAttributes.disinfect:
            message = MessageSetDisinfect(self._message_protocol_version)
            setattr(message, str(attr), value)
        # Extended: set curve types. Preserve the other type from current attributes.
        elif attr in [
            DeviceAttributes.zone1_curve_type.value,
            DeviceAttributes.zone2_curve_type.value,
        ]:
            message = self.make_message_set()
            z1 = (
                int(value)
                if attr == DeviceAttributes.zone1_curve_type.value
                else self._attributes.get(DeviceAttributes.zone1_curve_type)
            )
            z2 = (
                int(value)
                if attr == DeviceAttributes.zone2_curve_type.value
                else self._attributes.get(DeviceAttributes.zone2_curve_type)
            )
            message.zone1_curve_type = z1 if z1 is not None else 0
            message.zone2_curve_type = z2 if z2 is not None else 0
        elif attr in [
            DeviceAttributes.silent_mode.value,
            DeviceAttributes.SILENT_LEVEL.value,
        ]:
            message = MessageSetSilent(self._message_protocol_version)
            if attr == DeviceAttributes.silent_mode.value and isinstance(value, bool):
                message.silent_mode = bool(value)
                message.silent_level = (
                    C3SilentLevel.SILENT
                    if value
                    and self._attributes[DeviceAttributes.SILENT_LEVEL]
                    == C3SilentLevel.OFF.name
                    else C3SilentLevel[self._attributes[DeviceAttributes.SILENT_LEVEL]]
                )
            elif attr == DeviceAttributes.SILENT_LEVEL.value and isinstance(value, str):
                message.silent_level = C3SilentLevel[value]
                message.silent_mode = value != C3SilentLevel.OFF.name
        if message is not None:
            self.build_send(message)

    def set_mode(self, zone: int, mode: int) -> None:
        """Midea C3 device set mode."""
        message = self.make_message_set()
        if zone == 0:
            message.zone1_power = True
        else:
            message.zone2_power = True
        message.mode = mode
        self.build_send(message)

    def set_target_temperature(
        self,
        target_temperature: float,
        mode: int | None,
        zone: int | None = None,
    ) -> None:
        """Midea C3 device set target temperature."""
        if zone is None:
            raise ValueError("[C3] Parameter `zone` must be set")

        message = self.make_message_set()
        if self._attributes[DeviceAttributes.zone_temp_type][zone]:
            message.zone_target_temp[zone] = target_temperature
        else:
            message.room_target_temp = target_temperature
        if mode is not None:
            if zone == 0:
                message.zone1_power = True
            else:
                message.zone2_power = True
            message.mode = mode
        self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea C3 device set customize.

        Supports keys:
        - temperature_step: number
        - enable_advanced_params: bool (optionally nested under key "c3")
        """
        self._temperature_step = self._default_temperature_step
        self._enable_advanced_params = False
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if isinstance(params, dict):
                    # temperature step
                    if "temperature_step" in params:
                        temp_step = params.get("temperature_step")
                        if isinstance(temp_step, (float, int)):
                            self._temperature_step = float(temp_step)
                        else:
                            _LOGGER.error(
                                "[%s] Invalid type for temperature_step: %s",
                                self.device_id,
                                temp_step,
                            )
                    # optional advanced params toggle (enables UnitPara now)
                    adv_val = None
                    c3_cfg = params.get("c3")
                    if isinstance(c3_cfg, dict):
                        adv_val = c3_cfg.get("enable_advanced_params")
                    if adv_val is None:
                        adv_val = params.get("enable_advanced_params")
                    self._enable_advanced_params = bool(adv_val)
            except json.JSONDecodeError:
                _LOGGER.exception(
                    "[%s] JSON decode error in set_customize",
                    self.device_id,
                )
            # reflect configured step in attributes
            self.update_all({"temperature_step": self._temperature_step})


class MideaAppliance(MideaC3Device):
    """Midea C3 appliance."""
