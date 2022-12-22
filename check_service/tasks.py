import json
from base64 import b64encode
from io import BytesIO

import requests
from celery import shared_task
from django.conf import settings
from django.core.files import File
from django.template import Template, Context
from requests import Response

from check_service.models import Check
from orders.models import Order
from sheep_fish.celery import app


def get_pdf_check(html: bytes) -> Response:
    url = settings.HTML_TO_PDF_URL
    encoding = "utf-8"

    base64_bytes = b64encode(html)
    base64_string = base64_bytes.decode(encoding)

    data = {"contents": base64_string}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def save_to_pdf_field(
        check: Check,
        response: Response,
        pdf: bytes,
        pdf_name: str
) -> None:
    if response.status_code == 200:
        check.status = "rendered"
        check.save()
    check.pdf_file = File(BytesIO(pdf), pdf_name)
    check.save()


def render_template(order: Order, template_name: str) -> bytes:
    with open(template_name, "r") as f:
        template = Template(f.read())
    html_file = template.render(context=Context({"order": order}))
    return bytes(str(html_file), encoding="utf8")


@shared_task
def render_pdf_check(check_id, ) -> None:
    check = Check.objects.get(id=check_id)
    order = check.order
    if check.type == "client":
        html = render_template(
            order=order,
            template_name=settings.CLIENT_CHECK_TEMPLATE)
    if check.type == "kitchen":
        html = render_template(
            order=order,
            template_name=settings.KITCHEN_CHECK_TEMPLATE)
    response = get_pdf_check(html)
    pdf_file = response.content
    pdf_name = f"{order.order_number}_{check.type}.pdf"
    save_to_pdf_field(check, response, pdf_file, pdf_name)
