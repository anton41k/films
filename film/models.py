# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Films(models.Model):
	name=models.CharField(max_length=100,verbose_name=u'Фильм')
	orig_name=models.CharField(max_length=100,verbose_name=u'Оригинальное название')
	date=models.IntegerField(verbose_name=u'Год выхода')
	studio_country=models.CharField(max_length=500,verbose_name=u'Студия/Страна', blank=True, null=True)
	poster=models.ImageField(upload_to='poster/%Y/%m/%d',verbose_name=u'Постер')
	genre=models.ManyToManyField('Genres',verbose_name=u'Жанр')
	producer=models.CharField(max_length=30,verbose_name=u'Режисер')
	cast=models.CharField(max_length=300,verbose_name=u'В ролях')
	duration=models.CharField(max_length=10,verbose_name=u'Продолжительность')
	translation=models.CharField(max_length=20,verbose_name=u'Перевод')
	quality=models.CharField(max_length=10,verbose_name=u'Качество')
	size=models.CharField(max_length=20,verbose_name=u'Размер')
	detail=models.TextField(verbose_name=u'Описание')
	kinopoisk=models.IntegerField(verbose_name=u'ID фильма на сайте kinopoisk.ru', blank=True, null=True)
	down_load=models.URLField(verbose_name=u'Скачать')
	date_film = models.DateTimeField(verbose_name=u'Дата', default=timezone.now)
	autor=models.ForeignKey('auth.User',verbose_name=u'Разместил', blank=True, null=True)
	count = models.IntegerField(u"Количество просмотров", default=0)
	check_film = models.BooleanField(verbose_name=u'Проверено',default=False)
	coment_count=models.IntegerField( default=0)
	ratings_film = models.FloatField(verbose_name=u"Рейтинг фильма", default=0.0)
	def __unicode__(self):
		return u'%s %s %s %s'%(self.name,self.orig_name,self.date,self.quality)
	class Meta:
		verbose_name_plural = "Фильмы"
		ordering=['-date_film']

r=(
					('1','1'),
					('2','2'),
					('3','3'),
					('4','4'),
					('5','5'),
)
class Rating(models.Model):
	film=models.ForeignKey('Films',verbose_name=u'Фильм')
	user_rating=models.ForeignKey('auth.User',verbose_name=u'Поставил рейтинг', blank=True, null=True)
	rating=models.CharField(max_length=1,choices=r,verbose_name=u'Рейтинг')
	def __unicode__(self):
		return u'%s,%s'%(self.film,self.rating)
	class Meta:
		verbose_name_plural = "Рейтинг"
		ordering=['film']

class AddUser(models.Model):
	add=models.OneToOneField('auth.User')
	about_me=models.TextField(max_length=2000,verbose_name=u'Немного о себе', blank=True, null=True)
	avatar=models.ImageField(upload_to='avatar/%Y/%m/%d',verbose_name=u'Аватарка',default='img/noavatar.png')
	ICQ=models.IntegerField(verbose_name=u'Номер ICQ', blank=True, null=True)
	city=models.CharField(max_length=50,verbose_name=u'Место жительства', blank=True, null=True)
	user_sms=models.ManyToManyField('SmsUser',verbose_name=u'Сообщение', blank=True, null=True)
	lastlogin = models.DateTimeField(verbose_name=u'Дата', default=timezone.now)
	def __unicode__(self):
		return u'%s'%(self.add)
	class Meta:
		verbose_name_plural = "Редактирование информации"

class SmsUser(models.Model):
	sender =models.ForeignKey('auth.User',verbose_name=u'Автор')
	received=models.ForeignKey('auth.User',verbose_name=u'Получатель',related_name='received')
	topic=models.CharField(max_length=300,verbose_name=u'Тема')
	sms=models.TextField(verbose_name=u'Сообщение')
	date_sms = models.DateTimeField(verbose_name=u'Дата', default=timezone.now)
	lable= models.BooleanField(default=False)
	def __unicode__(self):
		return u'%s'%(self.topic)
	class Meta:
		verbose_name_plural = "Отправка персонального сообщений"
		ordering=['-date_sms']

class Screens(models.Model):
	films=models.ForeignKey('Films',related_name='screen')
	screen=models.ImageField(upload_to='screens/%Y/%m/%d',verbose_name=u'Скрины')
	def __unicode__(self):
		return u'%s'%(self.pk)
	class Meta:
		verbose_name_plural = "Скрины"
		ordering=['pk']

class Coments(models.Model):
	us=models.ForeignKey('auth.User',verbose_name=u'Автор')
	coment=models.ForeignKey('Films',verbose_name=u'Коментарии к фильму')
	message=models.TextField(verbose_name=u'Сообщение')
	answer=models.TextField(verbose_name=u'Ответ', blank=True, null=True)
	answer_user=models.CharField(max_length=30,verbose_name=u'Ответил на коментарий', blank=True, null=True)
	date_coment = models.DateTimeField(verbose_name=u'Дата', default=timezone.now)
	def __unicode__(self):
		return u'%s'%(self.us)
	class Meta:
		verbose_name_plural = "Коментарии"
		ordering=['date_coment']

class Genres(models.Model):
	name_genre=models.CharField(max_length=30,verbose_name=u'Жанр')
	def __unicode__(self):
		return u'%s'%(self.name_genre)
	class Meta:
		verbose_name_plural = "Жанры"
		ordering=['name_genre']

