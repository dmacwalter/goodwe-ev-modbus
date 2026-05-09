from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REG_PLUG_CHARGE, REG_EMS_DISPATCH, REG_CHARGE_CONTROL, REG_SINGLE_3PH
from .coordinator import GoodweEVCoordinator
from .sensor import _device_info


@dataclass(frozen=True, kw_only=True)
class GoodweSwitchDescription(SwitchEntityDescription):
    data_key: str = ""
    register: int = 0
    write_on: int = 1       # value sent to register on turn_on
    write_off: int = 0      # value sent to register on turn_off
    state_on: int | None = None  # if set, is_on = (data == state_on); else = (data == write_on)


SWITCHES: tuple[GoodweSwitchDescription, ...] = (
    GoodweSwitchDescription(
        key="plug_charge",
        data_key="plug_charge",
        name="Plug & Charge",
        register=REG_PLUG_CHARGE,
        write_on=1,
        write_off=0,
    ),
    GoodweSwitchDescription(
        key="ems_dispatch",
        data_key="ems_dispatch",
        name="EMS Dispatch (Reduce Power)",
        register=REG_EMS_DISPATCH,
        write_on=1,
        write_off=0,
    ),
    GoodweSwitchDescription(
        key="single_3ph",
        data_key="single_3ph",
        name="Single/Three-Phase Switching",
        register=REG_SINGLE_3PH,
        write_on=1,
        write_off=0,
    ),
    GoodweSwitchDescription(
        # 10060 is a command register — it does not retain its value after acting.
        # Read charging state from status (10017 == 3 means charging in progress).
        key="charge_control",
        data_key="status",
        name="Charging",
        register=REG_CHARGE_CONTROL,
        write_on=2,    # 2 = start
        write_off=1,   # 1 = stop
        state_on=3,    # status 3 = charging in progress
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GoodweEVCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GoodweSwitch(coordinator, entry, desc) for desc in SWITCHES
    )


class GoodweSwitch(CoordinatorEntity[GoodweEVCoordinator], SwitchEntity):
    entity_description: GoodweSwitchDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoodweEVCoordinator,
        entry: ConfigEntry,
        description: GoodweSwitchDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = _device_info(coordinator, entry)

    @property
    def is_on(self) -> bool:
        val = self.coordinator.data.get(self.entity_description.data_key, 0)
        check = self.entity_description.state_on
        return val == (check if check is not None else self.entity_description.write_on)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_write_register(
            self.entity_description.register,
            self.entity_description.write_on,
        )

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_write_register(
            self.entity_description.register,
            self.entity_description.write_off,
        )
