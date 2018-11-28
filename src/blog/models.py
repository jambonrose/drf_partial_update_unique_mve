"""Data models for Blog; actually a MVE for DRF bug"""
from datetime import date

from django.db.models import CharField, DateField, Model, SlugField


class Post(Model):
    """Simple Post object for MVE purposes

    Demonstrates working ModelSerializer usage
    """

    title = CharField(max_length=63)
    slug = SlugField(max_length=63)
    pub_date = DateField(default=date.today)


class UniquePost(Model):
    """Post object with a unique constraint

    Demonstrates failing ModelSerializer usage
    """

    title = CharField(max_length=63)
    slug = SlugField(max_length=63, unique_for_month="pub_date")
    pub_date = DateField(default=date.today)
