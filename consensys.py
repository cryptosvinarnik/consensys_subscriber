from asyncio import Queue
from random import choice, choices
from string import ascii_letters

from anti_useragent import UserAgent
from httpx import AsyncClient, Response
from httpx._exceptions import (ConnectError, ConnectTimeout, ProxyError,
                               ReadTimeout)
from loguru import logger
from urllib3 import encode_multipart_formdata

from utils.captcha import solve_by_capmonster
from utils.consensys_data import ConsensysForms, get_consensys_json
from utils.user_data import UserData


class HSFormError(Exception):
    pass


HEADERS = {
    "User-Agent": "",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}


def get_modified_headers(user_agent: str) -> dict:
    headers = HEADERS.copy()
    headers["User-Agent"] = user_agent

    return headers


class HSFormClient:
    def __init__(self, proxy: str | None, user_agent: str) -> None:
        self.client = AsyncClient(
            proxies={"all://": proxy} if proxy else None,
            headers=get_modified_headers(user_agent)
        )

    async def _request(self, url: str, method: str, **kwargs) -> dict:
        response = await self.client.request(method, url, **kwargs)
        return self._validate_response(response)

    def _validate_response(self, response: Response) -> bool:
        if response.json().get("success") or response.json().get("accepted"):
            return True
        raise HSFormError(response.text)


class Consensys(HSFormClient):
    def __init__(self, proxy: str | None) -> None:
        self.ua = UserAgent().random
        self.user = UserData()

        super().__init__(proxy, self.ua)

    async def submit_newsletter_form(self, email: str, g_recaptcha_response: str) -> bool:
        data = {
            "hs_context": get_consensys_json(self.ua, email, self.user.COUNTRY_CODE),
            "g-recaptcha-response": g_recaptcha_response,
            "email": email,
            "firstname": self.user.FIRSTNAME,
            "lastname": self.user.LASTNAME,
            "company": "".join(choices(ascii_letters, k=10)),
            "type_of_lead": "ConsenSys Newsletter",
            "lead_source": "ConsenSys Homepage",
            "manage_your_subscriptions_": choice(["STATE CHANGE:", "SIGNAL:", "ENTERPRISE:"]),
            "consensys_newsletter_sign_up": "Yes",
            "form_name": "Homepage Newsletter Subscription",
            "LEGAL_CONSENT.subscription_type_5257326": "true"
        }

        body, header = encode_multipart_formdata(data)

        self.client.headers.update({
            "Referer": "https://consensys.net/",
            "Origin": "https://consensys.net",
            "Content-Type": header}
        )

        return await self._request(
            ConsensysForms.NEWSLETER_URL.value,
            "POST",
            data=body.decode("utf-8")
        )

    async def submit_nft_form(self, email: str) -> bool:
        self.client.headers.update({
            "Referer": "https://share.hsforms.com",
            "Origin": "https://share.hsforms.com",
            "Content-Type": "text/plain"}
        )

        return await self._request(
            ConsensysForms.NFT_URL.value,
            "POST",
            data=email
        )


async def worker(worker_num: int, q: Queue):
    while not q.empty():
        email, proxy = await q.get()
        consensys = Consensys(proxy)

        logger.info(f"{worker_num} | {email} - solving captcha...")
        captcha_token = await solve_by_capmonster()

        try:
            await consensys.submit_newsletter_form(email, captcha_token)
            logger.success(
                f"{worker_num} | {email} submitted to newsletter form")
        except HSFormError as e:
            logger.error(
                f"{worker_num} | {email} failed to submit to newsletter form: {e}")
        except (ConnectError, ConnectTimeout, ReadTimeout, ProxyError):
            logger.error(f"{worker_num} | {email} failed connecting, maybe proxy is dead")
            continue

        try:
            await consensys.submit_nft_form(email)
            logger.success(f"{worker_num} | {email} submitted to NFT form")
        except HSFormError as e:
            logger.error(
                f"{worker_num} | {email} failed to submit to NFT form: {e}")
        except (ConnectError, ConnectTimeout, ReadTimeout, ProxyError):
            logger.error(f"{worker_num} | {email} failed connecting, maybe proxy is dead")
            continue
            
        await consensys.client.aclose()
