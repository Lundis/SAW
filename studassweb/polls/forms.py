# Here you want some form
# Google for inline formset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
# or look at install/forms.py, maybe easier

class PollForm(forms.ModelForm):

    class Meta:
        model = Examinator
        fields = ('name',)
