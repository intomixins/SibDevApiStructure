from django.db import models


class Gem(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=128)
    spent_money = models.IntegerField(default=0)
    gems = models.ManyToManyField(
        Gem,
        related_name='customers',
        blank=True,
    )

    def __str__(self) -> str:
        return self.username


class Deal(models.Model):
    username = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='deal_username',
        blank=True,
    )
    item = models.ForeignKey(
        Gem,
        on_delete=models.CASCADE,
        related_name='deal_gems',
        blank=True,
    )
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.username}: {self.item}x{self.quantity}'
