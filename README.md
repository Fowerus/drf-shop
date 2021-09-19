# **DRF API Internet Shop**

## **Inroduction**

It is a simle online store with bitcoin payment and to be precise with Paykassa merchant which built with Django-Rest-Framework.

## **Installation**

* Go to backend `cd backend/`
* Establish a virtual environment(recommend use python3)  
  In python3 you can do that with with `python3 -m venv <environment name>`
* Activate the virtual environment `source <environment name>/bin/activate`
* Install all libraries from requirements.txt  
  You can do that with run `python3 -m pip install -r requirements.txt`
* Install all migrations `python3 manage.py makemigrations && python3 manage.py migrate`
* Do not forget to create a superuser account `python3 manage.py createsuperuser`  

## **Testing**

Before running tests you need
* Create the Paykassa merchant
* Go to file `backend/Shop/merchant.py`
* Change `merchant_id`, `merchant_secret_key`, `merchant_domain` according to your merchant details.
* Run `python3 manage.py test`

But if you don't want to do that you can comment last three methods in `backend/Shop/tests/test_api.py` and testing the payment functions will be ignored.

## **Running**

For running you just need run `python3 manage.py runserver`

## **Other**

Right now API doesn't implement sending image to the client. So user cannot change account image. There is no opportunity to add a product, you can do that only with Django admin site.
