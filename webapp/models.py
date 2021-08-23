from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Region(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name=_('Аймактын аталышы'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Аймак'
        verbose_name_plural = 'Аймактар'


class Village(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name=_('Айылдын аталышы'))

    region = models.ForeignKey('webapp.Region',
                               on_delete=models.CASCADE,
                               related_name='villages',
                               verbose_name=_('Аймагы'))
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Айыл')
        verbose_name_plural = _('Айылдар')


class Member(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name=_('Аты'))

    surname = models.CharField(max_length=128,
                               verbose_name=_('Фамилиясы'))

    avatar = models.ImageField(upload_to='avatars/',
                               null=True,
                               blank=True,
                               verbose_name=_('Суроту'))

    phone_number1 = PhoneNumberField(verbose_name=_('Телефон 1'))
    phone_number2 = PhoneNumberField(verbose_name=_('Телефон 2'))
    whatsapp_number = PhoneNumberField(verbose_name=_('Whatsapp номери'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Мүчө болуу тарыхы'))

    position = models.CharField(max_length=256,
                                verbose_name=_('Кызматы'))

    region = models.ForeignKey('webapp.Region',
                               on_delete=models.CASCADE,
                               verbose_name=_('Аймагы'))

    village = models.ForeignKey('webapp.Village',
                                on_delete=models.CASCADE,
                                verbose_name=_('Айылы'))

    membership_fee = models.BooleanField(default=False,
                                         verbose_name=_('Мүчөлүк төлөмдөн бошотулган'))
    deleted = models.DateTimeField(null=True,
                                   blank=True,
                                   verbose_name=_('Өчүрүлгөн'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Мүчө')
        verbose_name_plural = _('Мүчөлөр')
