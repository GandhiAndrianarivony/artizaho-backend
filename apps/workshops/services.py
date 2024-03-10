from django.db import models


def update_django_model(instance: models.Model, field, value):
    setattr(instance, field, value)
    instance.save()


def get_object(model, data, data_attr, exception, message, model_field):
    try:
        filter_kwargs = {model_field: data.get(data_attr)}
        instance = model.objects.get(**filter_kwargs)
    except:
        raise exception(message)

    return instance
