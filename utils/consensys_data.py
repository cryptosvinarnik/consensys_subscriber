import time
from enum import Enum


class ConsensysForms(Enum):
    PORTAL_ID = 4795067

    NEWSLETER_MAIL_URL = "https://forms.hsforms.com/emailcheck/v1/json-ext?hs_static_app=forms-embed&hs_static_app_version=1.2802&X-HubSpot-Static-App-Info=forms-embed-1.2802&portalId=4795067&formId=1e2170b1-be79-4b91-947f-e10e7b428ff1&includeFreemailSuggestions=true"
    NEWSLETER_URL = "https://forms.hsforms.com/submissions/v3/public/submit/formsnext/multipart/4795067/1e2170b1-be79-4b91-947f-e10e7b428ff1/json?hs_static_app=forms-embed&hs_static_app_version=1.2802&X-HubSpot-Static-App-Info=forms-embed-1.2802"
    NFT_URL = "https://forms.hsforms.com/emailcheck/v1/json-ext?hs_static_app=forms-embed&hs_static_app_version=1.2802&X-HubSpot-Static-App-Info=forms-embed-1.2802&portalId=4795067&formId=1e2170b1-be79-4b91-947f-e10e7b428ff1&includeFreemailSuggestions=true"

    NEWSLETTER_FORM_ID = "1e2170b1-be79-4b91-947f-e10e7b428ff1"
    NFT_FORM_ID = "38705ada-7aca-4178-a8ba-7de502a2229a"

    TEMPLATE_NEWSLETTER_JSON: str


with open("data/newsletter.json", "r") as f:
    ConsensysForms.TEMPLATE_NEWSLETTER_JSON = f.read()


def get_consensys_json(user_agent: str, email: str, country_code: str) -> str:
    a = ConsensysForms.TEMPLATE_NEWSLETTER_JSON \
        .replace("{useragent}", user_agent) \
        .replace("{email}", email) \
        .replace("{timestamp}", str(int(time.time()))) \
        .replace("{country_code}", country_code)

    return a
