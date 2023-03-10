from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
from config import CAPMONSTER_API_KEY


client_options = ClientOptions(api_key=CAPMONSTER_API_KEY)
client = CapMonsterClient(options=client_options)


async def solve_by_capmonster(web_url: str = "https://consensys.net/shanghai-capella-upgrade/", site_key: str = "6Ld_ad8ZAAAAAAqr0ePo1dUfAi0m4KPkCMQYwPPm"):
    request = RecaptchaV2ProxylessRequest(websiteUrl=web_url, websiteKey=site_key)
    task = await client.solve_captcha(request)

    response =  task.get("gRecaptchaResponse")
    return response
