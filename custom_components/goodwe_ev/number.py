from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REG_MAX_POWER, REG_BATTERY_SOC, REG_GRID_LIMIT
from .coordinator import GoodweEVCoordinator
from .sensor import _device_info


@dataclass(frozen=True, kw_only=True)
class GoodweNumberDescription(NumberEntityDescription):
    data_key: str = ""
    register: int = 0
    scale: float = 1.0   # multiply before writing, divide after reading


NUMBERS: tuple[GoodweNumberDescription, ...] = (
    GoodweNumberDescription(
        key="max_power",
        data_key="max_power",
        name="Max Charging Power",
        register=REG_MAX_POWER,
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        native_min_value=1.4,
        native_max_value=22.0,
        native_step=0.1,
        mode=NumberMode.BOX,
        scale=10.0,  # stored as ÷10 kW
    ),
    GoodweNumberDescription(
        key="battery_soc",
        data_key="battery_soc",
        name="Battery Discharge SOC Limit",
        register=REG_BATTERY_SOC,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        scale=1.0,
    ),
    GoodweNumberDescription(
        key="grid_limit",
        data_key="grid_limit",
        name="Grid Power Limit",
        register=REG_GRID_LIMIT,
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        native_min_value=1.4,
        native_max_value=22.0,
        native_step=0.1,
        mode=NumberMode.BOX,
        scale=10.0,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GoodweEVCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GoodweNumber(coordinator, entry, desc) for desc in NUMBERS
    )


class GoodweNumber(CoordinatorEntity[GoodweEVCoordinator], NumberEntity):
    entity_description: GoodweNumberDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoodweEVCoordinator,
        entry: ConfigEntry,
        description: GoodweNumberDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = _device_info(coordinator, entry)

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get(self.entity_description.data_key)

    async def async_set_native_value(self, value: float) -> None:
        raw = int(round(value * self.entity_description.scale))
        await self.coordinator.async_write_register(
            self.entity_description.register, raw
        )
