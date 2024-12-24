import json
import base64
import requests
import datetime

from django.conf import settings
from base.const import CONTENT_TYPE_JSON
from django.core.cache import cache
from django.core.cache import caches



# "/v2/merchant/company"

# "/v2/merchant/person"

# "/v2/invoice"

def qpay_get_token(invoice_no):
    terminal_id = "91909029"
    
    try:
        data = settings.QPAY_USERNAME + ':' + settings.QPAY_PASSWORD
        auth_b64 = base64.b64encode(data.encode('utf-8')).decode()
        
        print("QPay access token: {}-{}-{}".format(settings.QPAY_TOKEN_URL, auth_b64, terminal_id))

        response = requests.post(
            settings.QPAY_TOKEN_URL,
            headers={'Authorization': 'Basic ' + auth_b64}, 
            json={'terminal_id': terminal_id}
        )
        print("qpay_get_token response : ", response)
 
        response.raise_for_status()
        resp = response.json()
        print("expires_in : " , resp['expires_in'])
        
        cache = caches['default']
        cache.set(invoice_no, resp)

        token = resp.get("access_token")
        return token
    except Exception as e:
        print('QPay token авахад алдаа гарлаа. ', str(e))
        raise Exception("API Response Problem [%s]." % (str(e)))


def create_invoice_simple(data):
    amount = data.get('amount')
    if amount <= 0:
        raise 
    url = settings.QPAY_URL + "/v2/invoice"
        
    invoice_no = "%s" % (datetime.datetime.now().strftime("%Y%m%d%H%M%S").zfill(10))
    print("invoice_no : ", invoice_no)

    bearer_token = qpay_get_token(invoice_no)

    token = cache.get(invoice_no)
    print("token : \n%s\n%s" % (token, bearer_token))

    payload = json.dumps({
        "invoice_code": "TEST_INVOICE",
        "sender_invoice_no": invoice_no,
        "invoice_receiver_code": "91909029",
        "invoice_description": "test",
        "amount": amount,
        "callback_url": "https://bd5492c3ee85.ngrok.io/payments?payment_id=91909029"
    })
    print("payload : ", payload)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % bearer_token
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload
    )

    if response.status_code == requests.codes.OK:
        ret = response.json()
        response_data = {
            "invoice_id": ret.get("invoice_id"),
            "qr_image": ret.get("qr_image"),
            "qr_short_url": ret.get("qPay_shortUrl"),
            "qr_text": ret.get("qr_text"),
        }
    return response_data


def create_invoice(request_id, invoice_id, amount, pos_terminal):
    bank_list = []
    bank_corp_code = None
    company = pos_terminal.company
    response = None
 
    bearer_token = qpay_get_token(pos_terminal.company_brc)
 
    payment_method = InventoryPOSTransactionPaymentMethod.objects.filter(key=POS_TRANSACTION_PAYMENT_QPAY).first()
    if not payment_method:
        pass
 
    payment_method_link_list = POSPaymentMethodBankAccountLink.objects.filter(
        payment_method_id=payment_method.pk
    ).all()
 
    if len(payment_method_link_list) == 0:
        raise Exception("Create Invoice Error!!!")
 
    for link in payment_method_link_list:
        bank_account = BaazBankAccountInfo.objects.filter(pk=link.bank_account_id).first()
        if not bank_account:
            continue
        
        bank_list.append({
            'account_bank_code': bank_account.bank.corp_code,
            'account_number': bank_account.account_number,
            'account_name': bank_account.bank.name,
            'is_default': bank_corp_code == None
        })
 
    try:
        headers = {
            'Authorization': "Bearer" + bearer_token['access_token'],
            "Content-Type": CONTENT_TYPE_JSON
        }
 
        body = {
            'merchant_id': company.qpay_merchant_id,
            'branch_code': pos_terminal.company_brc,
            'amount': float(amount),
            'currency': 'MNT',
            'customer_name': company.name,
            'customer_logo': '',
            'callback_url':  '{}/m25_new/qpay/callback/?invoice_id={}&brc={}'.format(settings.BAAZ_ROUTER, invoice_id, pos_terminal.company_brc),
            'description': str(amount) + ' төгрөгний худалдан авалт.',
            'mcc_code': '',
            'bank_accounts': bank_list,
        }
        print("QPay create invoice request data url: {}".format(settings.QPAY_URL), extra={'headers': headers, 'body': body, 'Request-Id': request_id, 'brc': pos_terminal.company_brc})
        response = requests.post(
            settings.QPAY_URL + '/v2/invoice',
            headers=headers,
            json=body
        )
        if response.status_code == requests.codes.OK:
            resp_json = response.json()
            resp_json.pop('urls')
            resp_json.pop('qr_image')
            cache.set('QPAY_{}'.format(invoice_id), value=resp_json, timeout=5 * 60)
            return resp_json
        print("QPay create invoice response: {}".format(response.text), extra={'Request-Id': request_id, 'brc': pos_terminal.company_brc})
        response.raise_for_status()
    except Exception as e:
        print('QPay invoice failed.\nerror:{}'.format(e), extra={'Request-Id': request_id, 'brc': pos_terminal.company_brc}, exc_info=True)
        raise Exception("QPay exception ", str(e))


def qpay_check_invoice(invoice_id, brc):
    try:
        bearer_token = qpay_get_token(brc)

        headers = {
            'Authorization': "Bearer" + bearer_token,
            "Content-Type": CONTENT_TYPE_JSON
        }

        qpay_invoice_data = cache.get('QPAY_{}'.format(invoice_id))
        print("qpay_invoice_data from cache: {}".format(qpay_invoice_data))

        body = {'invoice_id': qpay_invoice_data['id']}

        response = requests.post(
            settings.QPAY_URL + '/v2/payment/check',
            headers=headers,
            json=body
        )
        resp_json = response.json()
        print("QPay invoice check response: {}".format(resp_json), extra={'brc': brc})
        if response.status_code == requests.codes.OK:
            cache.set('QPAY_{}'.format(invoice_id), value=resp_json, timeout=5 * 60)
            return
        response.raise_for_status()
    except Exception as e:
        print('Qpay invoice check failed.\nerror: {}'.format(e), extra={'brc': brc}, exc_info=True)
        raise Exception("API Response Problem [%s]." % (str(e)))


def qpay_cancel_invoice(request_id, invoice_id, brc):
    try:
        bearer_token = qpay_get_token(brc)
 
        headers = {
            'Authorization': "Bearer" + bearer_token['access_token'],
            "Content-Type": CONTENT_TYPE_JSON
        }
 
        qpay_invoice_data = cache.get('QPAY_{}'.format(invoice_id))
        print("qpay_invoice_data from cache: {}".format(qpay_invoice_data), extra={'Request-Id': request_id})
        if not qpay_invoice_data:
            raise Exception("Нэхэмжлэх Олдсонгүй")
 
        response = requests.delete(
            settings.QPAY_URL + '/v2/invoice/{}'.format(qpay_invoice_data['id']),
            headers=headers
        )
        resp_json = response.json()
        print("QPay invoice cancel response: {}".format(resp_json), extra={'brc': brc, 'Request-Id': request_id})
        if response.status_code == requests.codes.OK:
            cache.delete("QPAY_{}".format(invoice_id))
            return

        response.raise_for_status()
    except Exception as e:
        print('Qpay invoice cancel failed.\nerror: {}'.format(e), extra={'brc': brc, 'Request-Id': request_id}, exc_info=True)
        raise Exception("API Response Problem [%s]." % (str(e)))
