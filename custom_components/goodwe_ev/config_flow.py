from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID, DEFAULT_PORT, DEFAULT_UNIT_ID
from .coordinator import GoodweEVCoordinator


async def _test_connection(hass: HomeAssistant, host: str, port: int, unit_id: int) -> str | None:
    """Return error key or None on success."""
    def _connect():
        from pymodbus.client import ModbusTcpClient
        client = ModbusTcpClient(host, port=port, timeout=5)
        if not client.connect():
            return "cannot_connect"
        resp = client.read_holding_registers(10017, count=1, device_id=unit_id)
        client.close()
        if resp.isError():
            return "invalid_response"
        return None

    return await hass.async_add_executor_job(_connect)


class GoodweEVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            error = await _test_connection(
                self.hass,
                user_input[CONF_HOST],
                user_input[CONF_PORT],
                user_input[CONF_UNIT_ID],
            )
            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"GoodWe EV ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): int,
                }
            ),
            errors=errors,
        )
