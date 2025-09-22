from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from utils.models import TimestampModel

User = get_user_model()

class Blog(TimestampModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travle','여행'),
        ('cat','고양이'),
        ('dog','강아지')
    )
    category = models.CharField('카테고리', max_length=100, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'


# Comment 모델은 Blog 밖에서 독립적으로 정의
class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at']
