from typing import List, Union

import pendulum
from django.core.management import BaseCommand
from django.db.models import Model, QuerySet


class ActionCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--action", type=str, help="Action to perform")
        return parser

    def handle(self, *args, **options):
        action = options.get("action")
        if not action:
            raise Exception("Action not specified")
        getattr(self, action)()


class ModelActionCommand(BaseCommand):
    """
    Base class for commands that need to load Django settings.
    Usage:
    python manage.py <command_name> --id 1 --action <method_name>
    """

    model_class = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--id",
            type=int,
            help="Instance ID to execute action command on",
        )
        parser.add_argument(
            "--desc",
            action="store_true",
            help="Execute action command on instances in descending order",
        )
        parser.add_argument("--action", type=str, help="Execute command on instance")
        return parser

    def handle(self, *args, **options):
        """
        Load Django settings.
        """
        object_id = options.get("id", None)
        descending = options.get("desc", False)
        action = options.get("action")

        if not self.model_class:
            raise Exception("Model class not specified")
        if not action:
            raise Exception("Action not specified")

        objs = self.model_class.objects.all().order_by("id")
        if descending:
            objs = objs.order_by("-id")
        if object_id:
            objs = objs.filter(id=object_id)

        start_time = pendulum.now()
        self.run_action(action, objs)
        end_time = pendulum.now()
        delta = end_time - start_time

        print(
            "{}.{} took: {}".format(self.model_class.__name__, action, delta.in_words())
        )

    def run_action(
        self,
        action: str,
        objs: Union[QuerySet | List[Model]],
    ):
        log_callback = getattr(self, f"{action}_log", lambda obj: "")
        for n, obj in enumerate(objs, 1):
            try:
                getattr(self, action)(obj)
            except Exception as e:
                print(e)
                print("Error processing object with id: {}".format(obj.id))
                raise e
            print(
                "{}/{} | {} ID: {} | {}".format(
                    n, objs.count(), obj.__class__.__name__, obj.id, log_callback(obj)
                )
            )

        getattr(self, action, objs)
