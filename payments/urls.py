from django.urls import path

from .views import click_callback, failed, payme_callback, success

urlpatterns = [
    path("success/", success, name="payment-success"),
    path("failed/", failed, name="payment-failed"),
    path("click/callback/", click_callback, name="click-callback"),
    path("payme/callback/", payme_callback, name="payme-callback"),
]
