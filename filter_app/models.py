from django.db import models


class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    customer = models.CharField(max_length=255)
    date = models.DateField()
    text = models.TextField()
    another_text = models.CharField(max_length=255)
    boolean_field = models.BooleanField(default=False)
    boolean_field1 = models.BooleanField(default=True)
    boolean_field2 = models.BooleanField(default=True)
    some_text = models.TextField(default='Default text')
    price = models.IntegerField(default=100)
    vendor = models.CharField(max_length=255, default='My vendor')

    @property
    def number_customer(self):
        return f'{self.amount}, {self.customer}'
