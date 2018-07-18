from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import (CharField, TextField, ForeignKey,
                              PositiveSmallIntegerField)


class Pizza(models.Model):
    """This model describes the entity of kind of pizza"""
    class Mete:
        ordering = ['name']

    name = CharField(max_length=128,
                     verbose_name=_("Name"),
                     unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """This model describes order entity"""

    PIZZA_SIZE_30 = 1
    PIZZA_SIZE_50 = 2

    PIZZA_SIZES = (
        (PIZZA_SIZE_30, _("30cm")),
        (PIZZA_SIZE_50, _("50cm"))
    )

    pizza = ForeignKey(Pizza, on_delete=models.CASCADE,
                       verbose_name=_("Pizza"))
    customer_name = CharField(max_length=128, verbose_name=_("Name"))
    customer_address = TextField(verbose_name=_("Address"))
    pizza_size = PositiveSmallIntegerField(verbose_name=_("Pizza size"),
                                           choices=PIZZA_SIZES,
                                           default=PIZZA_SIZE_30)

    def __str__(self):
        return "%s(%s) for %s" % (self.pizza, self.pizza_size, self.customer_name)
