from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CHARGER_STATUS,
    CAR_STATUS,
    CP_STATE,
    CHARGING_MODE,
    CHARGER_TYPE,
)
from .coordinator import GoodweEVCoordinator


@dataclass(frozen=True, kw_only=True)
class GoodweSensorDescription(SensorEntityDescription):
    data_key: str = ""
    value_map: dict | None = None  # int → str translation


SENSORS: tuple[GoodweSensorDescription, ...] = (
    # ── Electrical ──────────────────────────────────────────────────────────
    GoodweSensorDescription(
        key="phase_a_voltage",
        data_key="phase_a_voltage",
        name="Phase A Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    GoodweSensorDescription(
        key="phase_b_voltage",
        data_key="phase_b_voltage",
        name="Phase B Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    GoodweSensorDescription(
        key="phase_c_voltage",
        data_key="phase_c_voltage",
        name="Phase C Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    GoodweSensorDescription(
        key="phase_a_current",
        data_key="phase_a_current",
        name="Phase A Current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    GoodweSensorDescription(
        key="phase_b_current",
        data_key="phase_b_current",
        name="Phase B Current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    GoodweSensorDescription(
        key="phase_c_current",
        data_key="phase_c_current",
        name="Phase C Current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    GoodweSensorDescription(
        key="charging_power",
        data_key="charging_power",
        name="Charging Power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
    ),
    # ── Energy ──────────────────────────────────────────────────────────────
    GoodweSensorDescription(
        key="session_energy",
        data_key="session_energy",
        name="Session Energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    GoodweSensorDescription(
        key="accumulated_energy",
        data_key="accumulated_energy",
        name="Total Energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    GoodweSensorDescription(
        key="green_energy",
        data_key="green_energy",
        name="Green Energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    GoodweSensorDescription(
        key="grid_energy",
        data_key="grid_energy",
        name="Grid Energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    # ── Status ──────────────────────────────────────────────────────────────
    GoodweSensorDescription(
        key="status",
        data_key="status",
        name="Charger Status",
        device_class=SensorDeviceClass.ENUM,
        options=list(CHARGER_STATUS.values()),
        value_map=CHARGER_STATUS,
    ),
    GoodweSensorDescription(
        key="car_status",
        data_key="car_status",
        name="Car Connection",
        device_class=SensorDeviceClass.ENUM,
        options=list(CAR_STATUS.values()),
        value_map=CAR_STATUS,
    ),
    GoodweSensorDescription(
        key="cp_state",
        data_key="cp_state",
        name="CP State",
        device_class=SensorDeviceClass.ENUM,
        options=list(CP_STATE.values()),
        value_map=CP_STATE,
    ),
    GoodweSensorDescription(
        key="charging_mode",
        data_key="charging_mode",
        name="Charging Mode",
        device_class=SensorDeviceClass.ENUM,
        options=list(CHARGING_MODE.values()),
        value_map=CHARGING_MODE,
    ),
    GoodweSensorDescription(
        key="charger_type",
        data_key="charger_type",
        name="Charger Type",
        device_class=SensorDeviceClass.ENUM,
        options=list(CHARGER_TYPE.values()),
        value_map=CHARGER_TYPE,
    ),
    # ── Config readback ─────────────────────────────────────────────────────
    GoodweSensorDescription(
        key="max_power",
        data_key="max_power",
        name="Max Charging Power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
    ),
    GoodweSensorDescription(
        key="grid_limit",
        data_key="grid_limit",
        name="Grid Power Limit",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GoodweEVCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GoodweSensor(coordinator, entry, desc) for desc in SENSORS
    )


class GoodweSensor(CoordinatorEntity[GoodweEVCoordinator], SensorEntity):
    entity_description: GoodweSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoodweEVCoordinator,
        entry: ConfigEntry,
        description: GoodweSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = _device_info(coordinator, entry)

    @property
    def native_value(self) -> Any:
        raw = self.coordinator.data.get(self.entity_description.data_key)
        if raw is None:
            return None
        if self.entity_description.value_map:
            return self.entity_description.value_map.get(raw, raw)
        return raw


def _device_info(coordinator: GoodweEVCoordinator, entry: ConfigEntry) -> dict:
    static = coordinator.device_info_static
    return {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": f"GoodWe EV Charger ({static.get('power_spec', '')})",
        "manufacturer": "GoodWe",
        "model": f"{static.get('power_spec', '')} {static.get('charger_type', '')}",
        "serial_number": static.get("serial"),
        "sw_version": static.get("sw_version"),
        "hw_version": static.get("hw_version"),
    }
