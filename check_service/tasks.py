from base64 import b64encode
from dataclasses import dataclass
from io import BytesIO
import json
import requests
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.core.files import File
from sheep_fish.celery import app

# {"order_number": 1,
#  "items" : {
#      "pizza": {
#          "quantity": 1
#          "price": 15
#      },
#      "pasta": {
#          "quantity": 2
#          "price": 30
#      },
#  }
# }


@dataclass
class Item:
    name: str
    quantity: int
    price: int | float


@dataclass
class Order:
    order_number: int
    items: list[Item]

    def __init__(self, order_number: int, items: dict):
        self.order_number = order_number
        self.items = [
            Item(name=name, quantity=data["quantity"], price=data["price"])
            for name, data in items.items()
        ]


def get_pdf_check(html):
    url = settings.HTML_TO_PDF_URL
    encoding = "utf-8"

    base64_bytes = b64encode(html)
    base64_string = base64_bytes.decode(encoding)

    data = {"contents": base64_string}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def save_to_pdf_field(check, response, pdf, pdf_name):
    if response.status_code == 200:
        check.status = "rendered"
        check.save()
    check.pdf_file = File(BytesIO(pdf), pdf_name)
    check.save()


def render_template(order, template_name: str) -> bytes:
    with open(template_name, "r") as f:
        template = Template(f.read())
    html_file = template.render(context=Context({"order": order}))
    return bytes(str(html_file), encoding="utf8")


@app.task
def render_pdf_check(check, template):
    order = Order(**check.order)
    html = render_template(order=order, template_name=template)
    response = get_pdf_check(html)
    pdf_file = response.content
    pdf_name = f"{order.order_number}_{check.type}.pdf"
    save_to_pdf_field(check, response, pdf_file, pdf_name)
