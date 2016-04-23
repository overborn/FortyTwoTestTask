from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models

APP_LIST = (
    't1_contact',
    't3_requests',
    't5_edit',
    't8_tag',
)


class Command(BaseCommand):
    help = "Prints models and number of instances for an app"

    def handle(self, *args, **kwargs):
        for app in APP_LIST:
            for model in get_models(get_app(app)):
                self.stdout.write(
                    "model {} has {} instances".format(
                        model.__name__, model.objects.count()
                    )
                )
                self.stderr.write(
                    "error: model {} has {} instances".format(
                        model.__name__, model.objects.count()
                    )
                )
