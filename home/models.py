from django.db import models
from account.models import User


class Category(models.Model):
    """ Product Categories """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Product """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du produit")
    category_id = models.ForeignKey(
        Category,
        related_name="category",
        verbose_name="Catégorie ID",
        on_delete=models.CASCADE,
    )

    nutriscore = models.CharField(max_length=1, verbose_name="Nutriscore")
    url = models.URLField(unique=True, verbose_name="URL")
    photo = models.URLField(verbose_name="Photo")
    ingredients = models.URLField(verbose_name="Ingredients", null=True)
    fat_100g = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    sugars_100g = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    salt_100g = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    saturate_fat_100g = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"


class Rating(models.Model):
    """ Product """

    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    user_id = models.ForeignKey(
        User, related_name="user", verbose_name="User ID", on_delete=models.CASCADE,
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_id", "user_id"], name="unique_rating",
            )
        ]
        verbose_name = "Note"
