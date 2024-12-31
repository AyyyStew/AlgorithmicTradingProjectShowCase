import hmac, hashlib, time
from requests.auth import AuthBase

from secret_config import COINBASE_API_KEY, COINBASE_API_SECRET

# Before implementation, set environmental variables with the names API_KEY and API_SECRET
API_KEY = COINBASE_API_KEY
API_SECRET = COINBASE_API_SECRET


# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))

        # requests library turns json to bytes before it gets here this turns it back into a string.
        body = request.body
        if type(body) == bytes:
            body = str(body, "utf-8")

        # if we are using the advanced trade v3 api, we need to remove the query parameters for authentication to work
        # https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-auth
        version = self.get_api_version(request.path_url)
        path = request.path_url
        if version == "v3":
            path = path.split("?")[0]

        message = timestamp + request.method + path + (body or "")
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        request.headers.update(
            {
                "CB-ACCESS-SIGN": signature,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-ACCESS-KEY": self.api_key,
            }
        )
        return request

    @staticmethod
    def get_api_version(path):
        # figure out what api version we are using.
        chunks = path.split("/")
        if "api" in chunks and "v3" in chunks:
            return "v3"
        elif "v2" in chunks:
            return "v2"
        else:
            return ValueError("Unsupported API version")


auth = CoinbaseWalletAuth(COINBASE_API_KEY, COINBASE_API_SECRET)
