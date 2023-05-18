# DRF ECOMMERCE

DRF Ecommerce is an e-commerce platform built using Django and Django Rest Framework (DRF). It provides a set of APIs
for managing products, orders, and user authentication.

## Configure .env file

###### DJANGO SETTINGS

- SECRET_KEY - you can generate it [here](https://djecrety.ir/).
- DEBUG - by default this value is ```True```.
- LANGUAGE_CODE - by default this value is ```en-us```.
- TIME_ZONE - by default this value is ```UTC```

  ###### DATABASE CONNECTION
- DB_ENGINE - by default this value is ```django.db.backend.sqlite3```.
  For example, you can write ```django.db.backends.postgresql```.
- DB_NAME - any database name that you want, for example ```drf_ecommerce_db```.
- DB_USER - any user that you want.
- DB_PASSWORD - any password that you want.
- DB_HOST - ```localhost```.
- DB_PORT - ```5432``` for example.

  ###### EMAIL CONNECTION
- EMAIL_HOST - any email host that you want, for example
  you can use gmail - ```EMAIL_HOST=smtp.gmail.com```
- EMAIL_HOST_USER - your email.
- EMAIL_HOST_PASSWORD - password from your account if you
  don't use 2FA authentication. If you are using 2FA authentication
  you need to paste here password which Google(if you are yousing Gmail) provided to you during the setup process.
- EMAIL_PORT - ```587``` for example.
- EMAIL_USE_TLS - ```True``` for example.
  #### Some articles about email sending in Django
- **
  *[Send emails with Django and Gmail , a better way](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab)
  ***
- ***[How to Send Email with Django](https://www.abstractapi.com/guides/django-send-email)***
- **
  *[How to send emails with python django through google SMTP server for free](https://bshoo.medium.com/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e)
  ***
- ***[Use Django to send emails with SMTP](https://opensource.com/article/22/12/django-send-emails-smtp)***

  ###### NOVA POSHTA
- NOVA_POSHTA_API_KEY - your nova poshta API KEY.
  To generate API KEY go [there](https://new.novaposhta.ua/), register or
  Sign In. Go to the [settings](https://new.novaposhta.ua/dashboard/settings) and
  after [security](https://new.novaposhta.ua/dashboard/settings/developers) and generate API KEY
  and paste it here ```NOVA_POSHTA_API_KEY=your_api_key```

  ###### PAYPAL
  #### First of all you need to create an account.
- [Create paypal account](https://www.paypal.com/ua/welcome/signup/#/intent)
- [Go to the dashboard](https://developer.paypal.com/dashboard/)
- [Go apps & credentials](https://developer.paypal.com/dashboard/applications/sandbox) and create app.
- Go to your created app.

  #### In .env file
- PAYPAL_CLIENT_ID - paste your ```client_id``` from you app page.
- PAYPAL_CLIENT_SECRET - paste ```your secret_key``` from your app page.

  #### To test payments create sandox account
- Go to the [Testing Tools/Sandox accounts](https://developer.paypal.com/dashboard/accounts)
- [Create account](https://developer.paypal.com/dashboard/accounts/create)
- Select personal(Buyer Account) and create account.
- [At the accounts page](https://developer.paypal.com/dashboard/accounts) click for three buttons and
  click ```view/edit``` account.
- Go to the funding, scroll to down and click edit.
- Write amount that you want to have in an account and click save.

## Installation and running

1. ### Clone the repository:

```git
git clone https://github.com/okuzmenko31/drf-ecommerce.git
```

2. ### Go to the project directory:

```python
cd
ecommerce
```

3. ### Build app with docker-compose

```shell
docker-compose build
```

4. ### Up docker-compose

```shell
docker-compose up
```

## API Reference

## Registration

### Request

``POST /api/v1/user/registration/``

```
{
    "email": "test@gmail.com",
    "password": "password",
    "password1": "password"
}
```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "status": 200,
    "message": "Mail with registration link has been sent to your email.",
    "data": {
        "email": "test@gmail.com"
    }
}
```

## Confimation of email and registration

### Request

```GET /api/v1/user/confirm_email/<token>/<email>/```

### Response - if all is ok.

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "You successfully confirmed your email!"
}
```

## Login

### Request

```POST /api/v1/user/login/```

```
{
    "email": "test@gmail.com",
    "password": "password"
}
```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "Successful authentication",
    "token": "c897d02a01eb25710955228d1c26d70554895660"
}
```

## Profile

### Request

```GET /api/v1/user/profile/```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": "@test",
    "full_name": null,
    "email": "test@gmail.com"
}
```

### Request

```PUT /api/v1/user/profile/```

```
{
    "username": "@test",
    "full_name": Test User
}
```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": "@test",
    "full_name": Test User,
    "email": "test@gmail.com"
}
```

## Change email

### Request

```POST /api/v1/user/change_email/```

```
{
   "email": "new_test@gmail.com"
}
```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "Mail with email changing confirmation has been sent to your new email. Your email in this account will be changed after confirmation."
}
```

## Email changing confirmation

### Request

```GET /api/v1/change_email_confirm/<token>/<email>/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "You successfully changed your email"
}
```

## Password reset

### Request

```POST /api/v1/user/password_reset/```

```
{
   "email": "new_test@gmail.com"
}
```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "Mail with password reset confirmation has been sent to your email."
}
```

## Password reset confirmation

### Request

```GET /api/v1/user/password_reset/<token>/<email>/```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "Password reset page. Write new password."
}
```

### Request

```POST /api/v1/user/password_reset/<token>/<email>/```

```
{
   "password": "new_password",
   "password1": "new_password"
}
```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "Password reset success."
}
```

## Bonuses balance page

### Request

```GET /api/v1/user/bonuses_balance/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "user": 8,
        "balance": 0
    }
]
```

## Update bonuses balance - only for admins

### Request

```PUT /api/v1/user/update_bonuses/<pk>/```

```
{
    "balance": 100
}
```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "user": 2,
    "balance": 100
}
```

## Products

### Request

```GET /api/v1/products/```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 2,
        "name": "Apple iPhone 13 Pro 256GB Space Black",
        "category": 3,
        "price": 54356,
        "price_with_discount": 54356,
        "description": null,
        "photo": null,
        "discount": 0,
        "article": "786081",
        "rating": "0.0",
        "availability_status": "in stock"
    },
    {
        "id": 3,
        "name": "Apple iPhone 13 Pro 256GB Deep Purple",
        "category": 3,
        "price": 52000,
        "price_with_discount": 51480,
        "description": null,
        "photo": null,
        "discount": 1,
        "article": "791854",
        "rating": "0.0",
        "availability_status": "low in stock"
    },
    {
        "id": 1,
        "name": "Apple iPhone 13 Pro 128GB Space Black",
        "category": 3,
        "price": 57859,
        "price_with_discount": 56701,
        "description": null,
        "photo": null,
        "discount": 2,
        "article": "8006227",
        "rating": "0.0",
        "availability_status": "in stock"
    }
]
```

### Request - only for admins

```POST /api/v1/products/```

```
{
    "name": "Apple iPhone 14 Pro Max 512GB Space Black",
    "category": 4,
    "price": 65999,
    "description": null,
    "photo": null,
    "discount": 2,
    "article": "sdf1fsa"
}
```

### Response

```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "name": "Apple iPhone 14 Pro Max 512GB Space Black",
    "category": 4,
    "price": 65999,
    "price_with_discount": 64019,
    "description": null,
    "photo": null,
    "discount": 3,
    "article": "sdf1fsa",
    "rating": "0.0",
    "availability_status": "in stock"
}
```

## Product detail

### Request

```GET /api/v1/products/<pk>/```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "name": "Apple iPhone 13 Pro 128GB Space Black",
    "category": 3,
    "price": 57859,
    "price_with_discount": 56701,
    "description": null,
    "photo": null,
    "discount": 2,
    "article": "8006227",
    "rating": "0.0",
    "availability_status": "in stock"
}

```

## Products by category

### Request

```GET /api/v1/products/by_category/<category_id>/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "Apple iPhone 13 Pro 128GB Space Black",
        "category": 3,
        "price": 57859,
        "price_with_discount": 56701,
        "description": null,
        "photo": null,
        "discount": 2,
        "article": "8006227",
        "rating": "0.0",
        "availability_status": "in stock"
    },
    {
        "id": 2,
        "name": "Apple iPhone 13 Pro 256GB Space Black",
        "category": 3,
        "price": 54356,
        "price_with_discount": 54356,
        "description": null,
        "photo": null,
        "discount": 0,
        "article": "786081",
        "rating": "0.0",
        "availability_status": "in stock"
    },
    {
        "id": 3,
        "name": "Apple iPhone 13 Pro 256GB Deep Purple",
        "category": 3,
        "price": 52000,
        "price_with_discount": 51480,
        "description": null,
        "photo": null,
        "discount": 1,
        "article": "791854",
        "rating": "0.0",
        "availability_status": "low in stock"
    },
    {
        "id": 5,
        "name": "Apple iPhone 13 Pro 512GB Space Black",
        "category": 3,
        "price": 65999,
        "price_with_discount": 64019,
        "description": null,
        "photo": null,
        "discount": 3,
        "article": "sdf1fsa",
        "rating": "0.0",
        "availability_status": "in stock"
    }
]
```

## Product variations

### Request

```GET /api/v1/products/variations/<product_id>/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 6,
        "variation_category_name": "Color Deep Purple",
        "product_name": "Apple iPhone 13 Pro 256GB Deep Purple",
        "product_link": "/api/v1/products/3/"
    },
    {
        "id": 1,
        "variation_category_name": "Memory 128GB",
        "product_name": "Apple iPhone 13 Pro 128GB Space Black",
        "product_link": "/api/v1/products/1/"
    }
]
```

## Product variations by variation category

### Request

```GET /api/v1/products/variations/<product_id>/<parent_id>/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "variation_category_name": "Memory 128GB",
        "product_name": "Apple iPhone 13 Pro 128GB Space Black",
        "product_link": "/api/v1/products/1/"
    }
]
```

## Categories

### Request

```GET /api/v1/categories/```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "Smartphones",
        "parent": null
    },
    {
        "id": 2,
        "name": "Apple Smartphones",
        "parent": 1
    },
    {
        "id": 3,
        "name": "Apple iPhone 13 Pro",
        "parent": 2
    },
    {
        "id": 4,
        "name": "Xiamo",
        "parent": null
    }
]

```

### Request - only for admins

```POST /api/v1/categories/```

```
{
    "id": 9,
    "name": "Samsung smarthphones",
    "parent": 1
}
```

### Response

```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{


    "id": 1,
    "name": "Smartphones",
    "parent": null
}
```

## Category detail

### Request

```GET /api/v1/categories/<pk>/```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "name": "Smartphones",
    "parent": null
}
```

### Request - only for admins

```PUT /api/v1/categories/<pk>/```

```
{
    "id": 1,
    "name": "New smartphones",
    "parent": null
}
```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "name": "New Smartphones",
    "parent": null
}
```

### Request - only for admins

```DELETE /api/v1/categories/<pk>/```

### Response

```
HTTP 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

## Basket

### Request

```GET /api/v1/basket/```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": "You dont have items in your basket!"
}
```

## Basket add

### Request

```POST /api/v1/basket/add/<product_id>/```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": {
        "user": 2,
        "owner_username": "@admin"
    },
    "items": [
        {
            "product": 1,
            "product_name": "Apple iPhone 13 Pro 128GB Space Black",
            "quantity": 1,
            "total_price": 56701
        }
    ],
    "total_amount": 56701,
    "total_quantity_of_products": 1
}
```

## Basket add quantity

### Request

```POST /api/v1/basket/add_quantity/<product_id>/```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": {
        "user": 2,
        "owner_username": "@admin"
    },
    "items": [
        {
            "product": 1,
            "product_name": "Apple iPhone 13 Pro 128GB Space Black",
            "quantity": 2,
            "total_price": 113402
        }
    ],
    "total_amount": 113402,
    "total_quantity_of_products": 2
}
```

## Basket minus quantity

### Request

```POST /api/v1/basket/minus_quantity/<product_id>/```

### Response

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": {
        "user": 2,
        "owner_username": "@admin"
    },
    "items": [
        {
            "product": 1,
            "product_name": "Apple iPhone 13 Pro 128GB Space Black",
            "quantity": 1,
            "total_price": 56701
        }
    ],
    "total_amount": 56701,
    "total_quantity_of_products": 1
}
```

## Basket clear

### Request

```POST /api/v1/basket/clear/```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": {
        "user": 2,
        "owner_username": "@admin"
    },
    "items": [],
    "total_amount": 0,
    "total_quantity_of_products": 0
}
```

## Checkout

### Request

```GET /api/v1/orders/checkout/```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "basket": {
        "user": 2,
        "owner_username": "@admin"
    },
    "items": [
        {
            "product": 1,
            "product_name": "Apple iPhone 13 Pro 128GB Space Black",
            "quantity": 1,
            "total_price": 56701
        }
    ],
    "total_amount": 56701,
    "total_quantity_of_products": 1
}
```

### Request

```POST /api/v1/orders/checkout/```

```
{
    "shipping_info": {
        "name": "Test",
        "surname": "User",
        "patronymic": "Userovich",
        "email": "new_test@gmail.com",
        "address": "Test address",
        "city": "Абазівка (Полтавський р-н, Полтавська обл)",
        "post_office": "Відділення №5 (до 30 кг): вул. Перемоги, 13, прим. №1, 2, 3, 4"
        
    },
    "payment_method": 2,
    "delivery_method": 2,
    "coupon": null,
    "activate_bonuses": false,
    "comment": "",
    "create_account": false
}
```

### Response

```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 89,
    "shipping_info": {
        "name": "Test",
        "surname": "User",
        "patronymic": "Userovich",
        "email": "new_test@gmail.com",
        "address": "Test address",
        "city": "Абазівка (Полтавський р-н, Полтавська обл)",
        "post_office": "Відділення №5 (до 30 кг): вул. Перемоги, 13, прим. №1, 2, 3, 4"
    },
    "payment_method": 2,
    "delivery_method": 2,
    "coupon": null,
    "activate_bonuses": false,
    "comment": "",
    "create_account": false,
    "total_amount": 56701,
    "payment_link": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-2AH72020TS646435P",
    "order_items": [
        {
            "order_id": 89,
            "product": {
                "id": 1,
                "name": "Apple iPhone 13 Pro 128GB Space Black",
                "category": 3,
                "price": 57859,
                "price_with_discount": 56701,
                "description": null,
                "photo": null,
                "discount": 2,
                "article": "8006227",
                "rating": "0.0",
                "availability_status": "in stock"
            },
            "quantity": 1,
            "total_price": 56701
        }
    ]
}
```

## Payment complete

### Request

```GET /api/v1/orders/order/<order_id>/<payment_id>/<payer_id/>```

### Response

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": "You successfully paid for order!"
}
```

## Stock

### Request

```GET /api/v1/stock```

### Response

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "product": 2,
        "product_name": "Apple iPhone 13 Pro 256GB Space Black",
        "product_link": "/api/v1/products/2/",
        "product_category_name": "Apple iPhone 13 Pro",
        "product_price": "54356",
        "product_article": "786081",
        "quantity_in_stock": 1,
        "quantity_sold": 15,
        "stock_date": "2023-05-20T17:42:00+03:00",
        "last_sales_date": "2023-05-18T21:42:00+03:00"
    }
]
```

### Request

```POST /api/v1/stock/```

```
{
    "product": Apple iPhone 13 Pro 512GB Space Black,
    "quantity_in_stock": 1,
    "quantity_sold": 15,
    "stock_date": "2023-05-20T17:42:00+03:00",
    "last_sales_date": "2023-05-18T21:42:00+03:00"
}
```

### Reponse

```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 2,
    "product": 5,
    "product_name": "Apple iPhone 13 Pro 512GB Space Black",
    "product_link": "/api/v1/products/5/",
    "product_category_name": "Apple iPhone 13 Pro",
    "product_price": "65999",
    "product_article": "sdf1fsa",
    "quantity_in_stock": 1,
    "quantity_sold": 15,
    "stock_date": "2023-05-20T17:46:00+03:00",
    "last_sales_date": "2023-05-18T17:46:00+03:00"
}
```

## Stock item detail

### Request

```GET /api/v1/stock/<item_id>/```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "product": 2,
    "product_name": "Apple iPhone 13 Pro 256GB Space Black",
    "product_link": "/api/v1/products/2/",
    "product_category_name": "Apple iPhone 13 Pro",
    "product_price": "54356",
    "product_article": "786081",
    "quantity_in_stock": 1,
    "quantity_sold": 15,
    "stock_date": "2023-05-20T17:42:00+03:00",
    "last_sales_date": "2023-05-18T21:42:00+03:00"
}
```

### Request

```PUT /api/v1/stock/<itemd_id>/```

```
{
    "id": 1,
    "product": 2,
    "product_name": "Apple iPhone 13 Pro 256GB Space Black",
    "product_link": "/api/v1/products/2/",
    "product_category_name": "Apple iPhone 13 Pro",
    "product_price": "54356",
    "product_article": "786081",
    "quantity_in_stock": 47,
    "quantity_sold": 100,
    "stock_date": "2023-05-20T17:42:00+03:00",
    "last_sales_date": "2023-05-18T21:42:00+03:00"
}
```

### Response

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "product": 2,
    "product_name": "Apple iPhone 13 Pro 256GB Space Black",
    "product_link": "/api/v1/products/2/",
    "product_category_name": "Apple iPhone 13 Pro",
    "product_price": "54356",
    "product_article": "786081",
    "quantity_in_stock": 47,
    "quantity_sold": 100,
    "stock_date": "2023-05-20T17:48:00+03:00",
    "last_sales_date": "2023-05-18T17:48:00+03:00"
}
```

### Request

```DELETE /api/v1/stock/<item_id>/```

### Response

```
HTTP 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```
