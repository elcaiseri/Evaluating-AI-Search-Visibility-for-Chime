import json
import os
import re

import openai
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

urls = [
    "https://www.ally.com/stories/save/",
    "https://www.ally.com/stories/spend/",
    "https://www.ally.com/stories/invest/",
    "https://www.ally.com/stories/protect/",
    "https://www.ally.com/stories/borrow/",
    "https://www.ally.com/stories/inspire/",
]

urls += [
    "https://www.ally.com/help/credit-cards/",
    "https://www.ally.com/help/about-ally/",
    "https://www.ally.com/help/careers/",
    "https://www.ally.com/help/investor-relations/",
    "https://www.ally.com/help/demand-notes/",
    "https://www.ally.com/help/press-room/",
    "https://www.ally.com/help/grants/",
    "https://www.ally.com/help/privacy-security/",
    "https://www.ally.com/help/bank/cds/",
    "https://www.ally.com/help/bank/cd-ladders/",
    "https://www.ally.com/help/bank/raise-your-rate/",
    "https://www.ally.com/help/bank/no-penalty-cd/",
    "https://www.ally.com/help/bank/savings-money-market/",
    "https://www.ally.com/help/bank/interest-checking/",
    "https://www.ally.com/help/bank/accounts-trust/",
    "https://www.ally.com/help/bank/iras/",
    "https://www.ally.com/help/bank/ira-hycd/",
    "https://www.ally.com/help/bank/ira-ryr/",
    "https://www.ally.com/help/bank/ira-osa/",
    "https://www.ally.com/help/bank/opening-account/",
    "https://www.ally.com/help/bank/account-information/",
    "https://www.ally.com/help/bank/login/",
    "https://www.ally.com/help/bank/beneficiaries/",
    "https://www.ally.com/help/bank/alerts-notifications/",
    "https://www.ally.com/help/bank/deposits/",
    "https://www.ally.com/help/bank/direct-deposit/",
    "https://www.ally.com/help/bank/early-direct-deposit/",
    "https://www.ally.com/help/bank/transfers/",
    "https://www.ally.com/help/bank/atms-withdrawals/",
    "https://www.ally.com/help/bank/debit-cards-checks/",
    "https://www.ally.com/help/bank/overdraft-protection/",
    "https://www.ally.com/help/bank/bill-pay/",
    "https://www.ally.com/help/bank/zelle/",
    "https://www.ally.com/help/bank/tax-documents/",
    "https://www.ally.com/help/invest/self-directed/",
    "https://www.ally.com/help/invest/robo-portfolio/",
    "https://www.ally.com/help/invest/wealth-management/",
    "https://www.ally.com/help/bank/savings-money-market/",
    "https://www.ally.com/help/home-loans/mortgage-get-started/",
    "https://www.ally.com/help/home-loans/mortgage-options/",
    "https://www.ally.com/help/home-loans/mortgage-preapproval/",
    "https://www.ally.com/help/home-loans/mortgage-application/",
    "https://www.ally.com/help/home-loans/mortgage-rates/",
    "https://www.ally.com/help/home-loans/mortgage-closing/",
    "https://www.ally.com/help/home-loans/refinance-get-started/",
    "https://www.ally.com/help/home-loans/refinance-application/",
    "https://www.ally.com/help/home-loans/refinance-rates/",
    "https://www.ally.com/help/home-loans/refinance-options/",
    "https://www.ally.com/help/home-loans/refinance-closing/",
    "https://www.ally.com/help/home-loans/general-support/",
    "https://www.ally.com/help/home-loans/escrow/",
    "https://www.ally.com/help/home-loans/forms/",
    "https://www.ally.com/help/home-loans/payments/",
    "https://www.ally.com/help/home-loans/insurance/",
    "https://www.ally.com/help/home-loans/payoff/",
    "https://www.ally.com/help/auto/personal-auto/",
    "https://www.ally.com/help/auto/vehicle-protection/",
    "https://www.ally.com/help/auto/auto-payment/",
    "https://www.ally.com/help/auto/pay-by-text/",
    "https://www.ally.com/help/auto/auto-payment-extension/",
    "https://www.ally.com/help/auto/auto-pay/",
    "https://www.ally.com/help/auto/auto-statements/",
    "https://www.ally.com/help/auto/auto-modification/",
    "https://www.ally.com/help/auto/scra/",
    "https://www.ally.com/help/auto/lease-end/",
    "https://www.ally.com/help/auto/auto-login/",
    "https://www.ally.com/help/auto/account-information/",
    "https://www.ally.com/help/auto/auto-contracts/",
    "https://www.ally.com/help/auto/manage-profile/",
    "https://www.ally.com/help/auto/online-activity/",
    "https://www.ally.com/help/auto/alerts/",
    "https://www.ally.com/help/auto/auto-payoff/",
    "https://www.ally.com/help/auto/message-center/",
    "https://www.ally.com/help/auto/documents/",
    "https://www.ally.com/help/auto/privacy-preferences/",
    "https://www.ally.com/help/auto/special-handling/",
]

urls += [
    "https://www.capitalone.com/about/our-commitments/",
    "https://www.capitalone.com/about/newsroom/",
    "https://www.capitalone.com/about/insights-center/",
    "https://www.capitalone.com/tech/",
]

urls += [
    "https://www.capitalone.com/credit-cards/faq/",
    "https://www.capitalone.com/auto-financing/faq/",
]

urls += [
    "https://www.chime.com/blog/category/banking-basics/",
    "https://www.chime.com/blog/category/payday/",
    "https://www.chime.com/blog/category/loans/",
    "https://www.chime.com/blog/category/money-habits/",
    "https://www.chime.com/blog/category/credit/",
    "https://www.chime.com/blog/category/safety-and-security/",
    "https://www.chime.com/blog/category/managing-debt/",
    "https://www.chime.com/blog/category/taxes/",
    "https://www.chime.com/blog/category/chime-guides/",
    "https://www.chime.com/blog/category/calculators/",
]

urls += ["https://www.chime.com/faq/"]

urls += [
    "https://help.chime.com/hc/en-us/articles/5438300132631-What-is-SpotMe",
    "https://help.chime.com/hc/en-us/articles/17193149287063-What-is-Safer-Credit-Building",
    "https://help.chime.com/hc/en-us/articles/17192694520983-What-is-Credit-Builder-and-how-can-I-enroll",
    "https://help.chime.com/hc/en-us/articles/20824325253655-What-is-Chime-s-Virtual-Card",
    "https://help.chime.com/hc/en-us/articles/23317674703511-What-s-MyPay",
    "https://help.chime.com/hc/en-us/articles/1500011981082-What-s-a-temporary-credit",
    "https://help.chime.com/hc/en-us/articles/221487887-What-is-the-Chime-Savings-Account",
]

urls += ["https://www.sofi.com/blog/"]

urls += ["https://www.sofi.com/faq/"]

urls += ["https://www.varomoney.com/blog/"]

#############################################


def scrap(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\n+", "\n", text)

    return text


def collect_avilable_information(url):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for a person who cannot search and read from a browser.",
            },
            {
                "role": "user",
                "content": f"Please provide a detailed information available at the following URL: {url}. Include key features, benefits, and any important considerations. (no bold)",
            },
        ],
        temperature=0.1,
        max_tokens=5000,
    )

    text = response["choices"][0]["message"]["content"]
    lines = text.split("\n")
    return "\n".join(lines[1:-1])


def main(urls, data_dir):
    # Create a directory to save the text files
    os.makedirs(data_dir, exist_ok=True)
    file2url = {}

    for i, url in tqdm(enumerate(sorted(urls)), total=len(urls)):
        file_path = f"{data_dir}/page_{i + 1}.txt"
        file2url[file_path] = url

        try:
            text = scrap(url)
        except Exception as e:
            text = collect_avilable_information(url)
            print(f"Failed to scrape: {url} with error {e}")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

    # Save the mapping of file to URL
    with open(f"{data_dir}/file2url.json", "w") as file:
        json.dump(file2url, file)
    print("Scraping complete.")


if __name__ == "__main__":
    main(urls, "../backend/data")
