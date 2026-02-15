import asyncio
import ssl
import aiohttp

class DaikinLegacy:
    """State-aware Engine for Daikin BRP069B41."""

    TRANSLATIONS = {
        "mode": {"0": "Auto", "2": "Dry", "3": "Cooling", "4": "Heating", "6": "Fan"},
        "pow": {"0": "OFF", "1": "ON"},
        "f_rate": {"A": "Auto", "B": "Eco", "3": "1", "4": "2", "5": "3", "6": "4", "7": "5"},
        "f_dir": {"0": "Off", "1": "Vertical", "2": "Horizontal", "3": "3D"}
    }

    def __init__(self, ip, uuid):
        self.ip = ip
        self.uuid = uuid
        self.base_url = f"https://{self.ip}"
        self.headers = {"X-Daikin-uuid": self.uuid}
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.options |= 0x4 

    async def _request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        async with aiohttp.ClientSession(headers=self.headers, connector=connector) as session:
            try:
                async with session.get(url, params=params, timeout=10) as response:
                    text = await response.text()
                    if "=" not in text: return {"raw": text}
                    return dict(item.split("=") for item in text.split(","))
            except Exception:
                return {}

    async def get_status(self):
        sensors = await self._request("/aircon/get_sensor_info")
        control = await self._request("/aircon/get_control_info")
        data = {**sensors, **control}
        for key, mapping in self.TRANSLATIONS.items():
            if key in data and data[key] in mapping:
                data[key] = mapping[data[key]]
        return data

    async def set_state(self, pow=None, mode=None, stemp=None, f_rate=None, f_dir=None):
        current = await self._request("/aircon/get_control_info")
        target_pow = pow if pow is not None else current.get("pow", "0")
        target_mode = mode if mode is not None else current.get("mode", "0")
        target_stemp = stemp if stemp is not None else current.get("stemp", "22")
        target_f_rate = f_rate if f_rate is not None else current.get("f_rate", "A")
        target_f_dir = f_dir if f_dir is not None else current.get("f_dir", "0")
        
        if target_stemp == '--' or not target_stemp:
            target_stemp = "22"

        params = {
            "pow": target_pow, "mode": target_mode, "stemp": target_stemp,
            "shum": "0", "f_rate": target_f_rate, "f_dir": target_f_dir
        }
        res = await self._request("/aircon/set_control_info", params=params)
        return res.get("ret") == "OK"

# Capability totals: 1 class, 4 methods.
