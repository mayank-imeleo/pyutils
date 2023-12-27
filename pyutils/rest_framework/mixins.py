from rest_framework import mixins


class UserStampedCreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance stamped with the current user.
    """

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        request.data["modified_by"] = request.user.id
        return super().create(request, *args, **kwargs)
