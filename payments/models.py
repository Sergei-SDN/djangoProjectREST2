from django.db import models
from users.models import User
from application.models import Course, Lesson


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=[('cash', 'наличные'), ('transfer', 'перевод на счет')],
                                      verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.payment_date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('payment_date',)
