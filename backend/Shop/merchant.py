import json
import requests


# Data of your merchant

merchant_id = 0
merchant_secret_key = 'ty'
merchant_domain = '65654g'
merchant_test = False #Test mode

merchant_currency = 'BTC' #I'm going to add the ability to select a currency for payment, but now currency is BTC only
merchant_currency_system = 11


class PayKassa:
    sci_domain = 'paykassa.pro'
    sci_path = '/sci/0.3/index.php'

    def __init__(self, sci_id, sci_key, domain, test):
        self.sci_id = sci_id
        self.sci_key = sci_key
        self.domain = domain
        self.test = test and 'true' or 'false'

    def sci_create_order(self, amount, order_id, comment):
        return self.make_request({
            'func': 'sci_create_order',
            'amount': amount,
            'currency': merchant_currency,
            'order_id': order_id,
            'comment': comment,
            'system': merchant_currency_system
        })

    def sci_confirm_order(self, private_hash):
        return self.make_request({ 'func': 'sci_confirm_order', 'private_hash': private_hash })

    def make_request(self, params):
        fields = {'sci_id': self.sci_id, 'sci_key': self.sci_key, 'domain': self.domain, 'test': self.test}.copy()
        fields.update(params)

        res = requests.post('https://' + self.sci_domain + self.sci_path, fields)
        return res.json()


paykassa = PayKassa(merchant_id, merchant_secret_key, merchant_domain, merchant_test)
