# **Django-Rest-Framework Shop**

## **Inroduction**

It is a simle online store with bitcoin payment and to be precise with Paykassa merchant which built with Django-Rest-Framework.

## **Installation**

* Establish a virtual environment(recommend use python3)  
  In python3 you can do that with with `python3 -m venv <environment name>`
* Install all libraries from requierements.txt  
  You can do that with run `python3 -m pip install -r requirements.txt`

## **Testing**

Before running tests you need
* Create the Paykassa merchant
* Go to file `backend/Shop/merchant.py`
* Change `merchant_id`, `merchant_secret_key`, `merchant_domain` according to your merchant details.

But if you don't want to do that you can comment last three methods in `backend/Shop/tests/test_api.py` and testing the payment functions will be ignored.

## **Running**

For running you just need run `python3 manage.py runserver`

## **Other**

Right now API doesn't implement sending image to the client. So user cannot change account image. There is no opportunity to add a product, you can do that only with Django admin site.
