from django import forms
from django.forms import inlineformset_factory

from .models import Product, Creator, Versions


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super(StyleFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug',)

    def clean_field(self, field_data, field_name):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар']
        if any(word in field_data.lower() for word in forbidden_words):
            raise forms.ValidationError(f"{field_name.capitalize()} содержит запрещенные слова.")
        return field_data

    def clean_name(self):
        name = self.cleaned_data['name']
        return self.clean_field(name, 'Название продукта')

    def clean_description(self):
        description = self.cleaned_data['description']
        return self.clean_field(description, 'Описание продукта')

    class Meta:
        model = Product
        exclude = ('slug',)


# Определение формы для модели Versions
class VersionForm(StyleFormMixin, forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        is_current_version = cleaned_data.get('is_current_version')

        if is_current_version:
            existing_active_versions = Versions.objects.filter(
                product=self.instance.product,
                is_current_version=True
            ).exclude(id=self.instance.id)

            if existing_active_versions.exists():
                raise forms.ValidationError("Может быть активной только одна версия продукта. Пожалуйста, выберите только одну активную версию.")

        return cleaned_data

# Создание InlineFormset
VersionInlineFormset = inlineformset_factory(
    Product,
    Versions,
    form=VersionForm,
    fields=['version_number', 'version_name', 'is_current_version'],
    extra=1,
    can_delete=True
)


class CreatorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'
