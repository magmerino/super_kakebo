
from djongo import models
import uuid


# Abstract classes
class Entry(models.Model):
    text = models.TextField()
    amount = models.FloatField()

    class Meta:
        abstract = True


class Overview(models.Model):
    income = models.ArrayField(model_container=Entry)
    fixed_expenses = models.ArrayField(model_container=Entry)
    savings_goal = models.EmbeddedField(model_container=Entry)
    spending_goal = models.EmbeddedField(model_container=Entry)

    class Meta:
        abstract = True


class DailyPurchase(models.Model):
    monday = models.FloatField()
    tuesday = models.FloatField()
    wednesday = models.FloatField()
    thursday = models.FloatField()
    friday = models.FloatField()
    saturday = models.FloatField()
    sunday = models.FloatField()

    class Meta:
        abstract = True


class Purchase(models.Model):
    purchase = models.TextField()
    category = models.CharField(max_length=255)
    days = models.EmbeddedField(model_container=DailyPurchase)

    class Meta:
        abstract = True


class Week(models.Model):
    purchases = models.ArrayField(model_container=Purchase)

    class Meta:
        abstract = True


class Spending(models.Model):
    needs = models.FloatField()
    wants = models.FloatField()
    culture = models.FloatField()
    unplanned = models.FloatField()
    total = models.FloatField()

    class Meta:
        abstract = True


class Review(models.Model):
    weekly_spending = models.ArrayField(model_container=Spending)
    total_spending = models.EmbeddedField(model_container=Spending)
    money_saved = models.FloatField()
    text = models.TextField()

    class Meta:
        abstract = True


# Concrete classes
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=10, default='user')
    currency = models.CharField(max_length=5, default='USD')
    language = models.CharField(max_length=5, default='en')

    def __str__(self):
        return self.email


class Month(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    overview = models.EmbeddedField(model_container=Overview)
    weeks = models.ArrayField(model_container=Week, blank=True)
    review = models.EmbeddedField(model_container=Review, blank=True)

    def __str__(self):
        return f'{self.user_id}/{self.year}-{self.month}'
