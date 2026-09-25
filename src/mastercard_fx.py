import os
import json
import csv
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
import oauth1.authenticationutils as authenticationutils
from oauth1.oauth_ext import OAuth1RSA


# =====================================================
# CONFIG
# =====================================================

load_dotenv(dotenv_path=".env", override=True)

CONSUMER_KEY = os.getenv("MASTERCARD_CONSUMER_KEY")
KEYSTORE_PATH = os.getenv("MASTERCARD_KEYSTORE_PATH")
KEYSTORE_PASSWORD = os.getenv("MASTERCARD_KEYSTORE_PASSWORD")

BASE_URL = os.getenv(
    "MASTERCARD_BASE_URL",
    "https://sandbox.api.mastercard.com"
)

ENDPOINT = (
    f"{BASE_URL}"
    "/settlement/currencyrate/conversion-rate"
)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# VALIDATION
# =====================================================

def validate_config():

    required = {
        "MASTERCARD_CONSUMER_KEY": CONSUMER_KEY,
        "MASTERCARD_KEYSTORE_PATH": KEYSTORE_PATH,
        "MASTERCARD_KEYSTORE_PASSWORD": KEYSTORE_PASSWORD,
    }

    missing = [
        name
        for name, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing configuration: "
            + ", ".join(missing)
        )

    if not Path(KEYSTORE_PATH).is_file():
        raise FileNotFoundError(
            f"Signing key not found: {KEYSTORE_PATH}"
        )


# =====================================================
# AUTHENTICATION
# =====================================================

def create_oauth():

    signing_key = authenticationutils.load_signing_key(
        KEYSTORE_PATH,
        KEYSTORE_PASSWORD
    )

    return OAuth1RSA(
        CONSUMER_KEY,
        signing_key
    )


# =====================================================
# MASTERCARD API
# =====================================================

def get_fx_rate(
    transaction_currency="USD",
    billing_currency="BRL",
    amount=1,
    bank_fee=0,
    fx_date=None
):

    if fx_date is None:
        fx_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "fxDate": fx_date,
        "transCurr": transaction_currency,
        "crdhldBillCurr": billing_currency,
        "bankFee": bank_fee,
        "transAmt": amount,
    }

    oauth = create_oauth()

    print()
    print("=" * 60)
    print("MASTERCARD FX MONITOR")
    print("=" * 60)
    print(f"Environment : {BASE_URL}")
    print(
        f"Currency    : "
        f"{transaction_currency}/{billing_currency}"
    )
    print(f"FX date     : {fx_date}")
    print(f"Amount      : {amount}")
    print("-" * 60)

    response = requests.get(
        ENDPOINT,
        params=params,
        auth=oauth,
        headers={
            "Accept": "application/json"
        },
        timeout=30
    )

    print(
        f"HTTP status : {response.status_code}"
    )

    if response.status_code != 200:
        print()
        print("MASTERCARD RESPONSE:")
        print(response.text)
        response.raise_for_status()

    result = response.json()

    save_raw(
        result,
        transaction_currency,
        billing_currency
    )

    data = result.get("data", result)

    error_code = data.get("errorCode")
    error_message = data.get("errorMessage")

    if error_code:
        print()
        print("Mastercard API returned an error:")
        print("Code   :", error_code)
        print("Message:", error_message)

        return result

    conversion_rate = data.get("conversionRate")
    converted_amount = data.get("crdhldBillAmt")

    print()
    print("RESULT")
    print("-" * 60)
    print(
        f"1 {transaction_currency} = "
        f"{conversion_rate} {billing_currency}"
    )

    print(
        f"{amount} {transaction_currency} = "
        f"{converted_amount} {billing_currency}"
    )

    save_history(
        data,
        transaction_currency,
        billing_currency
    )

    print()
    print("Historical data saved.")

    return result


# =====================================================
# RAW JSON
# =====================================================

def save_raw(
    result,
    transaction_currency,
    billing_currency
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = RAW_DIR / (
        f"mastercard_"
        f"{transaction_currency}_"
        f"{billing_currency}_"
        f"{timestamp}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# HISTORICAL CSV
# =====================================================

def save_history(
    data,
    transaction_currency,
    billing_currency
):

    file_path = (
        PROCESSED_DIR
        / "mastercard_fx_history.csv"
    )

    row = {
        "collected_at_utc":
            datetime.now(timezone.utc).isoformat(),

        "fx_date":
            data.get("fxDate"),

        "transaction_currency":
            transaction_currency,

        "billing_currency":
            billing_currency,

        "conversion_rate":
            data.get("conversionRate"),

        "transaction_amount":
            data.get("transAmt"),

        "billing_amount":
            data.get("crdhldBillAmt"),

        "bank_fee":
            data.get("bankFee"),
    }

    file_exists = file_path.exists()

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=row.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    try:

        validate_config()

        get_fx_rate(
            transaction_currency="USD",
            billing_currency="BRL",
            amount=1,
            bank_fee=0
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
