# -*- coding: utf-8 -*-
from film.models import *
from django.contrib.auth.models import User
from film.forms import *
from film.views import *
from django.db.models import Q
import datetime
from django.db.models import Count
from django.core.cache import cache

def menu_proc(request):
	now= datetime.datetime.now()
	delta=datetime.timedelta(seconds=-300)
	return {
		'genres':Genres.objects.all(),
		'posters':Films.objects.filter(check_film=True).order_by('-count'),
		'films':Films.objects.all(),
		'coments':Coments.objects.all(),
		'all_user':User.objects.annotate(com_count=Count('coments')).order_by('-com_count')[:5],
		'top_10':Films.objects.all().order_by('-ratings_film')[:10],
		'count_users':User.objects.all(),
		'count_user_online':AddUser.objects.filter(Q(lastlogin__gt=now+delta)).count()
}

def user_proc(request):
	if request.user.is_authenticated():
		count_films_user=Films.objects.filter(Q(check_film=False)&Q(autor=request.user)).count()
		check_count_films_user=Films.objects.filter(autor=request.user).count()
		check_films=Films.objects.filter(check_film=False).count()
		try:
			counts=AddUser.objects.get(add=request.user)
			new_sms_counts=counts.user_sms.filter(received=request.user,lable=False).count()
			coment_count=Coments.objects.filter(us=request.user).count()
		except AddUser.DoesNotExist:
			return{
				'sms_count':0,
				'new_sms_count':0,
				'coment_count':0,}
		return{
			'sms_count':counts.user_sms.all().count(),
			'new_sms_count':new_sms_counts,
			'coment_count':coment_count,
			'check_film':check_films,
			'count_films_user':count_films_user,
			'check_count_films_user':check_count_films_user}
	else:
		return{}


def log_in(request):
	if request.method == 'POST' and 'username' in request.POST:
		form_log = LoginForm(request.POST)
		if form_log.is_valid():
			data = form_log.cleaned_data
			if '@' in data['username']:
				user = auth.authenticate(username=user_obj.username, password=data['password'])
				if user is None:
					form_log.errors['password'] = [u'Вы неправильно ввели пароль']
				elif user is not None and user.is_active:
					auth.login(request, user)                
					return HttpResponseRedirect('/')
			else:
				user = auth.authenticate(username=data['username'], password=data['password'])
				if user is None:
					form_log.errors['password'] = [u'Вы неправильно ввели пароль']
				elif user is not None and user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect('/')             
	else:
		form_log = LoginForm()
	return {'form_log':form_log}


def index(request):
    users_cached = cache.get('users_online', {})
    users_online = users_cached and User.objects.filter(
        id__in=users_cached.keys()) or []
    guests_cached = cache.get('guests_online', {})
    guest_count = len(guests_cached)
    users_count = len(users_online)
    sum_count_user = guest_count + User.objects.count()

    return {
        'sum_count_user':sum_count_user,
        'guests_cached':guests_cached,
        'users_online': users_online,
        'online_count': users_count,
        'guest_count': guest_count,

    }
