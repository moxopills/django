from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Blog(models.Model):
    CATEGORY_CHOICES = (
    ('free', '자유'),
    ('travle','여행'),
    ('cat','고양이'),
    ('dog','강아지')
    )
    category = models.CharField('카테고리', max_length=100, choices=CATEGORY_CHOICES)
    title = models.CharField('제목',max_length=100)
    content = models.TextField('본문')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField('작성일자',auto_now_add=True)
    updated_at = models.DateTimeField('수정일자',auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('cb_blog_detail', kawrgs={'pk':self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'