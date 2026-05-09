from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID
from .coordinator import GoodweEVCoordinator

PLATFORMS = ["sensor", "switch", "number", "select"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    # Serve icon.png and icon@2x.png from this directory so HA's frontend
    # can display the brand icon on the integrations and devices pages.
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            f"/api/custom_components/{DOMAIN}",
            str(Path(__file__).parent),
            cache_headers=True,
        )
    ])
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = GoodweEVCoordinator(
        hass,
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
        entry.data[CONF_UNIT_ID],
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        coordinator: GoodweEVCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        coordinator.close()
    return unloaded
