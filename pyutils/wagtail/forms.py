from wagtail.admin.forms import WagtailAdminModelForm


class UserTimestampWagtailAdminForm(WagtailAdminModelForm):
    def full_clean(self):
        super().full_clean()
        if not self.instance.created_by_id:
            self.instance.created_by = self.for_user
        self.instance.modified_by = self.for_user


class TimestampFormViewMixin:
    form_class = UserTimestampWagtailAdminForm

    def get_form_class(self, *args, **kwargs):
        return self.form_class
