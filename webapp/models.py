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

    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s"/>' % escape(self.avatar.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Мүчө')
        verbose_name_plural = _('Мүчөлөр')

class TransferType(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name=_('Аталышы'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Которуу түрү')
        verbose_name_plural = _('Которуу түрлөрү')

class MembershipFee(models.Model):
    payer = models.ForeignKey('webapp.Member',
                              on_delete=models.CASCADE,
                              related_name='payments',
                              verbose_name=_('Төлөөчү'))

    amount = models.PositiveIntegerField(default=200,
                                         verbose_name=_('Төлөм суммасы'))

    transfer_type = models.ForeignKey('webapp.TransferType',
                                      on_delete=models.CASCADE,
                                      related_name='membership_fee',
                                      verbose_name=_('Которуу түрү'))

    info = models.TextField(max_length=2048,
                            verbose_name=_('Кошумча маалымат'))

    created_at = models.DateTimeField(auto_now_add=True)
    is_payed = models.BooleanField(default=False,
                                   verbose_name=_('Төлөндү белгиси'))

    payed_at = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name=_('Төлөнгөн тарыхы'))

    def __str__(self):
        return f'{self.payer}: {self.is_payed}'

PAYMENT_CHOICES=[
    ('income','Киреше'),
    ('expense', 'Чыгаша')
]

class Payments(models.Model):
    payer = models.CharField(max_length=128,
                             verbose_name=_('Төлөөчү'))

    amount = models.PositiveIntegerField(verbose_name=_('Төлөм суммасы'))

    type = models.CharField(max_length=128,
                            choices=PAYMENT_CHOICES,
                            verbose_name=_('Төлөм түрү'))

    info = models.TextField(max_length=2048,
                            verbose_name=_('Кошумча маалымат'))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Төлөм тарыхы'))

    def __str__(self):
        return f'{self.payer}:{self.amount} - {self.type}'

    class Meta:
        verbose_name = _('Төлөм')
        verbose_name_plural = _('Төлөмдөр')
