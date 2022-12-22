from django.db import models


TYPE_CHOICES = [
    ("kitchen", "kitchen"),
    ("client", "client"),
]

STATUS_CHOICES = [
    ("new", "new"),
    ("rendered", "rendered"),
    ("printed", "printed"),
]


class Printer(models.Model):
    name = models.CharField(max_length=60)
    check_type = models.CharField(max_length=60, choices=TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=60, choices=TYPE_CHOICES)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=60,
        choices=STATUS_CHOICES,
        default="new"
    )
    pdf_file = models.FileField(
        upload_to="pdf/",
        null=True,
        blank=True,
    )
