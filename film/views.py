# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from film.models import *
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from django.template import Template
from django.core.urlresolvers import reverse
from film.forms import *
from film.backends import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import F
from django.conf import settings
import os
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import operator
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

def xhr_test(request):
    if request.is_ajax():
        message = "Hello AJAX!"
    else:
        message = "Hello"
    return HttpResponse(message)

def proc(request):
	if request.is_ajax():
		if request.user.is_authenticated():
			try:
				counts=AddUser.objects.get(add=request.user)
				new_sms_counts=counts.user_sms.filter(received=request.user,lable=False).count()
				message1 = "У вас %s новое сообщение!" % new_sms_counts
				message = message1
			except AddUser.DoesNotExist:
				message = "ERROR"
		else:message = "ERROR1"
	else:
		message = "ERROR????"
	return HttpResponse(message)

from django.db.models import Count
def film(request,genre_pk=None):
	url = request.META.get('HTTP_REFERER', 'None')
	allfilm=''
	form_filter=FilterForm(label_suffix=' ')
	if not genre_pk:
		film = Films.objects.all()
		paginator = Paginator(film, 10)
		page = request.GET.get('page')
		try:
			allfilm = paginator.page(page)
		except PageNotAnInteger:
			allfilm = paginator.page(1)
		except EmptyPage:
			allfilm = paginator.page(paginator.num_pages)
		if request.is_ajax():
			templaters = 'center.html'
		else:templaters = 'film.html'
	elif genre_pk:
		genr=get_object_or_404(Genres,pk=genre_pk)
		f_genre=genr.films_set.all()
		paginator = Paginator(f_genre, 10)
		page = request.GET.get('page')
		try:
			allfilm = paginator.page(page)
		except PageNotAnInteger:# If page is not an integer, deliver first page.
			allfilm = paginator.page(1)
		except EmptyPage:# If page is out of range (e.g. 9999), deliver last page of results.
			allfilm = paginator.page(paginator.num_pages)
		form_filter=FilterForm(label_suffix='',initial={'genre_search':genr})
		templaters = 'center.html'
	users=request.user
	public_date = datetime.datetime.now()
	if request.method == 'GET' and 'year_search' in request.GET:
		criterions = [(Q(check_film=True))]
		if 'genre_search' in request.GET and request.GET['genre_search']:
			genre_film=request.GET['genre_search']	
			criterions.append(Q(genre__exact=genre_film))
		if request.GET['year_search']!=u'all':
			year=request.GET['year_search']
			criterions.append(Q(date__icontains=year))
		if request.GET['format_film_search']!=u'all':
			format_film=request.GET['format_film_search']
			criterions.append(Q(quality__icontains=format_film))
		if request.GET['sort']==u'down':
			if request.GET['sort_search']==u'add_date':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-date_film')
			if request.GET['sort_search']==u'review':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-count')
			if request.GET['sort_search']==u'coments':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).annotate(com=Count('coments')).order_by('-com')
			if request.GET['sort_search']==u'rating':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-ratings_film')
		if request.GET['sort']==u'up':
			if request.GET['sort_search']==u'add_date':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('date_film')
			if request.GET['sort_search']==u'review':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('count')
			if request.GET['sort_search']==u'coments':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).annotate(c=Count('coments')).order_by('c')
			if request.GET['sort_search']==u'rating':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('ratings_film')
		paginator = Paginator(allfilm, 10)
		page = request.GET.get('page')
		try:
			f_search = paginator.page(page)
		except PageNotAnInteger:
			f_search = paginator.page(1)
		except EmptyPage:
			f_search = paginator.page(paginator.num_pages)
		form_filter=FilterForm(label_suffix=' ',initial={'genre_search':request.GET['genre_search'],'year_search':request.GET['year_search'],'format_film_search':request.GET['format_film_search'],'sort_search':request.GET['sort_search'],'sort':request.GET['sort']})
		templaters = 'filter.html'
	return render_to_response( templaters,locals(), context_instance=RequestContext(request))

def detail(request,i_pk,com_pk=None,coment_pk=None):
	url = request.META.get('HTTP_REFERER', 'None')
	counts=Films.objects.filter(pk=i_pk).update(count=F('count')+1)
	film=get_object_or_404(Films,pk=i_pk)
	if not film.check_film and request.user!=film.autor and not request.user.is_superuser:
		raise Http404
	adduser=AddUser.objects.all()
	if request.user.is_authenticated():
		user_rating_film=Rating.objects.filter(film=film,user_rating=request.user)
	else:
		guests = cache.get('guests', {})
		guest_sid = request.COOKIES.get(settings.SESSION_COOKIE_NAME, '')
		cache.set(guest_sid, True, 60 * 60 * 24)
		c=cache.get(guest_sid)
	
		'''if guests[guest_sid] not in cache:
			user_rating_film=Rating.objects.filter(film=film)
			cache.add(guests[guest_sid],True)'''
	if request.method == 'POST' and 'rating' in request.POST and not user_rating_film:
		rating_form = RatingForm(request.POST)
		if rating_form.is_valid():
			data = rating_form.cleaned_data
			film_rating=rating_form.save(commit=False)
			film_rating.film=film
			film_rating.user_rating=request.user
			film_rating.save()
			ratings=film.rating_set.all()
			sums=0
			count_rating=film.rating_set.all().count()
			for i in ratings:
				sums=int(i.rating)+sums
			try:
				zsums=float(sums)/count_rating
			except ZeroDivisionError:
				zsums=0
			zsums='%03.1f' % zsums
			r=Films.objects.filter(pk=film.pk).update(ratings_film=zsums)
			return HttpResponseRedirect(url)
	else:
		rating_form= RatingForm()
	count_rating=film.rating_set.all().count()
	if request.user.is_authenticated():
		user_rating_film=Rating.objects.filter(film=film,user_rating=request.user)
	else:user_rating_film=''
	form = ComentForm()
	return render_to_response( 'detail.html',
											{'user_rating_film':user_rating_film, 												'count_rating':count_rating, 												'rating_form':rating_form,
											'film':film,
											'form':form,
											'adduser':adduser,},
								context_instance=RequestContext(request))
@login_required
def coments(request,i_pk=None,com_pk=None,coment_pk=None):
	url = request.META.get('HTTP_REFERER', 'None')
	film=get_object_or_404(Films,pk=i_pk)
	adduserall=AddUser.objects.all()
	try:
		if com_pk:
			com=Coments.objects.get(pk=com_pk)
			com.delete()
			if '/user/coments/' in url:
				return HttpResponseRedirect("/user/coments/")
			elif ('/%s/' % i_pk) in url:
				return HttpResponseRedirect('/%s/' % i_pk)
	except Coments.DoesNotExist:
		pass
	if request.method == 'POST' and 'coment' in request.POST:
		form = ComentForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if coment_pk:
				com=get_object_or_404(Coments,pk=coment_pk)
				c=Coments()
				c.us=request.user
				c.coment=film
				c.message=data['coment']
				c.answer=com.message
				c.answer_user=com.us
				c.save()
			else:
				c=Coments()
				c.us=request.user
				c.coment=film
				c.message=data['coment']
				c.save()
			return HttpResponseRedirect('/%s/' % i_pk)
	else:
		form = ComentForm()
	return render_to_response( 'coments.html',{'adduserall':adduserall}, context_instance=RequestContext(request))
	
def coments_user(request,user_pk):
	adduserall=AddUser.objects.all()
	return render_to_response( 'coments.html',{'adduserall':adduserall}, context_instance=RequestContext(request))

def users(request,i_pk):
	try:
		users=User.objects.get(pk=i_pk)
	except User.DoesNotExist:
		users=User.objects.get(username=request.user)
	count_film=Films.objects.filter(autor=users).count()
	new_count_film=Films.objects.filter(Q(autor=users)&Q(check_film=False)).count()
	list_film=Films.objects.filter(Q(autor=users)&Q(check_film=True))
	adduserall=AddUser.objects.all()
	try:
		adduser=AddUser.objects.get(add=users)
	except AddUser.DoesNotExist:
		adduser=None
	if request.method == 'POST':
		form_user=AddForm(request.POST, files=request.FILES,instance=adduser)
		if request.user.is_superuser:
			form = SuperUserForm(request.POST,instance=users)
		else:
			form = UserForm(request.POST,instance=users)
		if form.is_valid() and form_user.is_valid():
			form.save()
			add_user=form_user.save(commit=False)
			add_user.add=users
			add_user.save()
	else:
		if request.user.is_superuser:
			form = SuperUserForm(instance=users)
		else:
			form = UserForm(instance=users)
		form_user=AddForm(instance=adduser)
	return render_to_response( 'users.html',{'users':users,'list_film':list_film,'new_count_film':new_count_film,'count_film':count_film,'form_user':form_user,'form':form,'users':users,'adduser':adduser,'adduserall':adduserall}, context_instance=RequestContext(request))

@login_required
def sms(request,send_pk,rec_pk='',sms_pk='',add_film_user_pk=''):
	if sms_pk:
		answer=get_object_or_404(SmsUser,pk=sms_pk)
	else:
		answer=None
	u=User.objects.get(pk=send_pk)
	users=request.user
	receiv1=get_object_or_404(AddUser,add=users)
	sms_users=receiv1.user_sms.all()
	add_user=AddUser.objects.all()
	error=''
	if request.method == 'POST':
		form = SmsForm(request.POST)
		if form.is_valid():
			smsuser=form.save(commit=False)
			smsuser.sender=users
			if request.POST['received']==u.username:
				error= "Нельзя отправить сообщение самом себе!"
			else:
				smsuser.save()
				receiv=get_object_or_404(AddUser,add=smsuser.received.pk)
				receiv.user_sms.add(smsuser)
				send=get_object_or_404(AddUser,add=smsuser.sender.pk)
				send.user_sms.add(smsuser)
				return render_to_response('send_sms.html', context_instance=RequestContext(request))
	else:
		if add_film_user_pk:
			film=Films.objects.get(pk=rec_pk)
			form = SmsForm(initial={'received':User.objects.get(pk=add_film_user_pk),'topic':film.name,'sms':u'Исправьте следующие ошибки по раздаче: '+'\n'+film.name+'\n'})
		elif sms_pk:
			form = SmsForm(initial={'received':answer.sender,'topic':'RE:'+answer.topic,'sms':answer.sms})
		else:form = SmsForm()
	return render_to_response( 'sms.html',{'form':form,'users':users,'sms_users':sms_users,'add_user':add_user,'error':error}, context_instance=RequestContext(request))

def del_add_film(request,add_film_pk=''):
	film=Films.objects.get(pk=add_film_pk)
	url = request.META.get('HTTP_REFERER', 'None')
	if 'del_add_film' in url:
		film.delete()
		return HttpResponseRedirect('/')
	return render_to_response( 'delete_film.html',{'del_film':film}, context_instance=RequestContext(request))

@login_required
def user_sms(request):
	if request.user.is_authenticated():
		adduser=get_object_or_404(AddUser,add=request.user)
		u_sms=adduser.user_sms.filter(received=request.user).order_by('lable','-date_sms')
		if request.method == 'POST':
			form = ActionsOnSms(request.POST)
			if request.POST['action_sms']=='del' and 'id' in request.POST:
				sms=SmsUser.objects.get(pk=request.POST['id'])
				adduser.user_sms.remove(sms)
				s=AddUser.objects.get(pk=sms.sender.pk)
				r=AddUser.objects.get(pk=sms.received.pk)
				if sms not in s.user_sms.all() and sms not in r.user_sms.all():
					sms.delete()
			if request.POST['action_sms']=='mark' and 'id' in request.POST:
				sms=SmsUser.objects.filter(pk=request.POST['id']).update(lable=True)
			if request.POST['action_sms']=='uncheck' and 'id' in request.POST:
				sms=SmsUser.objects.filter(pk=request.POST['id']).update(lable=False)
			if request.POST['action_sms']=='delall':
				sms=adduser.user_sms.filter(received=request.user)
				for i in sms:
					adduser.user_sms.remove(i)
					s=AddUser.objects.get(pk=i.sender.pk)
					r=AddUser.objects.get(pk=i.received.pk)
					if i not in s.user_sms.all() and i not in r.user_sms.all():
						i.delete()
		else:
			form = ActionsOnSms()
	else:
		form=''
		u_sms=''
	return render_to_response( 'user_sms.html',{'form':form,'u_sms':u_sms}, context_instance=RequestContext(request))

@login_required
def sms_sends(request):
	adduser=get_object_or_404(AddUser,add=request.user.pk)
	s_sms=adduser.user_sms.filter(sender=request.user).order_by('lable','-date_sms')
	if request.method == 'POST':
		form = SubmittedOnSms(request.POST)
		if request.POST['action_sms']=='del' and 'id' in request.POST:
			sms=SmsUser.objects.get(pk=request.POST['id'])
			adduser.user_sms.remove(sms)
			s=AddUser.objects.get(add=sms.sender.pk)
			r=AddUser.objects.get(add=sms.received.pk)
			if sms not in s.user_sms.all() and sms not in r.user_sms.all():
				sms.delete()
		if request.POST['action_sms']=='delall':
			sms=adduser.user_sms.filter(sender=request.user)
			for i in sms:
				adduser.user_sms.remove(i)
				s=AddUser.objects.get(pk=i.sender.pk)
				r=AddUser.objects.get(pk=i.received.pk)
				if i not in s.user_sms.all() and i not in r.user_sms.all():
					i.delete()
	else:
		form = SubmittedOnSms()
	return render_to_response( 'dispatch _sms.html',{'form':form,'s_sms':s_sms}, context_instance=RequestContext(request))

@login_required
def new_sms(request,i_pk,u_pk=''):
	if u_pk:
		user=get_object_or_404(User,pk=u_pk)
		adduser=get_object_or_404(AddUser,add=user)
		sms=get_object_or_404(SmsUser,pk=i_pk)
		adduser.user_sms.remove(sms)
		return HttpResponseRedirect('/user/sms/')
	users=request.user
	add_user=AddUser.objects.all()
	try:
		sms_new=users.received.get(pk=i_pk)
		sms_new.lable=True
		sms_new.save()
	except SmsUser.DoesNotExist:
		raise Http404
	return render_to_response( 'new_sms.html',{'sms_new':sms_new,'add_user':add_user}, context_instance=RequestContext(request))	

@login_required
def dispatch(request,i_pk,u_pk=''):
	if u_pk:
		user=get_object_or_404(User,pk=u_pk)
		adduser=get_object_or_404(AddUser,add=user)
		sms=get_object_or_404(SmsUser,pk=i_pk)
		adduser.user_sms.remove(sms)
		return HttpResponseRedirect('/user/sms_sends/')
	users=request.user
	add_user=AddUser.objects.all()
	addus=AddUser.objects.get(add=users)
	try:
		sms_users=addus.user_sms.get(pk=i_pk)
	except SmsUser.DoesNotExist:
		raise Http404
	return render_to_response( 'send_detail_sms.html',{'sms_users':sms_users,'add_user':add_user}, context_instance=RequestContext(request))

def movies_to_check(request):
	film=Films.objects.filter(autor=request.user).order_by('check_film','-date_film')
	paginator = Paginator(film, 10)
	page = request.GET.get('page')
	try:
		films = paginator.page(page)
	except PageNotAnInteger:
		films = paginator.page(1)
	except EmptyPage:
		films = paginator.page(paginator.num_pages)
	return render_to_response( 'movies_to_check.html',{'paginator':paginator,'films':films}, context_instance=RequestContext(request))

def new_movies_to_check(request):
	films=Films.objects.filter(check_film=False)
	return render_to_response( 'new_movies_to_check.html',{'films':films}, context_instance=RequestContext(request))

from django.forms.formsets import formset_factory, BaseFormSet
@login_required
def add_film(request,film_pk=None):
	if film_pk:
		add_film=get_object_or_404(Films,pk=film_pk)
		screen_film=add_film.screen.all()
	else:
		add_film=''
		screen_film=''
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = False
	ScreensFormSet = formset_factory(ScreensForm,extra=3,max_num=3,formset=RequiredFormSet)
	if request.method == 'POST':
		def initial_form_count(self):return 3
		ScreensFormSet.initial_form_count=initial_form_count
		if film_pk:
			formset = ScreensFormSet(request.POST, files=request.FILES,initial=[{'screen':x.screen} for x in screen_film])
			form_film = FilmsForm(request.POST, files=request.FILES,instance=add_film)
		else:
			form_film = FilmsForm(request.POST, files=request.FILES, initial={'count':0})
			formset = ScreensFormSet(request.POST, files=request.FILES,initial=[{'screen':x.screen} for x in screen_film])
		if form_film.is_valid() and formset.is_valid():
			film=form_film.save(commit=False)
			if not film_pk:
				film.autor=request.user
			film.save()
			form_film.save_m2m()
			f=get_object_or_404(Films,pk=film.pk)
			if film_pk:
				if request.user.is_superuser and film.check_film:
					sms=SmsUser()
					sms.sender=request.user
					sms.received=film.autor
					sms.topic=u'Ваша публикация %s была одобрена'%(film.name)
					sms.sms=u'Ваша публикация "%s" http://anton41k.djangohost.name/%s была одобрена'%(film.name,film.pk)
					sms.save()
					receiv=get_object_or_404(AddUser,add=sms.received.pk)
					receiv.user_sms.add(sms)
					send=get_object_or_404(AddUser,add=sms.sender.pk)
					send.user_sms.add(sms)
				for x,y in zip(formset.cleaned_data,screen_film):
					s=Screens.objects.get(pk=y.pk)
					s.films=film
					s.screen=x['screen']
					s.save()
			else:
				for form in formset.forms:
					s=Screens(films=f,**form.cleaned_data)
					s.save()
			return HttpResponseRedirect('/%s/'% film.pk)
	else:
		if film_pk:	
			form_film = FilmsForm(instance=add_film)
			formset = ScreensFormSet(initial=[{'screen':x.screen} for x in screen_film])
		else:	
			form_film = FilmsForm()
			formset = ScreensFormSet()
	return render_to_response( 'info_add.html',{'add_film':add_film,"formset":formset,'form_film':form_film},  context_instance=RequestContext(request)) 

def log_out(request):
	auth.logout(request)
	last = request.META.get('HTTP_REFERER', 'None')
	return HttpResponseRedirect("/")   

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST.copy())
        if form.is_valid():
            data = form.cleaned_data
            try:
                user_obj = User.objects.get(username=data['username1'])
            except User.DoesNotExist:
                user_obj = User.objects.create_user(data['username1'], data['email'], data['password2'])
                user = auth.authenticate(username=data['username1'], password=data['password2'])
                auth.login(request, user)
                adduser=AddUser()
                adduser.add=request.user
                adduser.save()
                return HttpResponseRedirect('/user/add/')
            else:
                form.errors['username1'] = ['Пользователь уже существует']
    else:
        form = RegistrationForm()
    return render_to_response( 'register.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def adduser(request):
	user=request.user
	try:
		adduser=AddUser.objects.get(add=user)
	except AddUser.DoesNotExist:
		adduser=AddUser()
		adduser.add=user
	if request.method == 'POST':
		form = AddForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.cleaned_data
			adduser.about_me=data['about_me']
			adduser.avatar=data['avatar']
			adduser.ICQ=data['ICQ']
			adduser.city=data['city']
			adduser.save()
			return HttpResponseRedirect('/')
	else:
		form = AddForm()
	return render_to_response( 'add_user.html', {'form': form,'adduser':adduser}, context_instance=RequestContext(request))


def search(request):
	public_date = datetime.datetime.now()
	form_advanced_search=AdvancedSearchForm(label_suffix='')
	form_seaech=SearchForm(label_suffix='')
	if request.method == 'GET' and 'search_1' in request.GET:
		search = request.GET['search_1']
		if search:
			form_advanced_search=AdvancedSearchForm(label_suffix='',initial={'advanced_search':search})
			allfilm=Films.objects.filter((Q(name__icontains=search)|Q(orig_name__icontains=search))&(Q(check_film=True))).order_by('-date_film')
	elif request.method == 'GET' and 'advanced_search' in request.GET:
		criterions = [(Q(check_film=True))]
		search = request.GET['advanced_search']
		if request.GET['search']==u'any_word':
			any_word=search.split(' ')
			search_word=[]
			for word in any_word:
				if len(word)>=3:
					if request.GET['where_search']==u'name':
						search_word.append(Q(name__icontains=word))
					if request.GET['where_search']==u'producer':
						search_word.append(Q(producer__icontains=word))
					if request.GET['where_search']==u'cast':
						search_word.append(Q(cast__icontains=word))
			search_any_word=(reduce(operator.or_,search_word))
			criterions.append(search_any_word)
		else:
			if request.GET['where_search']==u'name':
				criterions.append(Q(name__icontains=search)|Q(orig_name__icontains=search))
			if request.GET['where_search']==u'producer':
				criterions.append(Q(producer__icontains=search))
			if request.GET['where_search']==u'cast':
				criterions.append(Q(cast__icontains=search))
		if 'genre_search' in request.GET and request.GET['genre_search']:
			genre_film=request.GET['genre_search']	
			criterions.append(Q(genre__exact=genre_film))
		if request.GET['year_search']!=u'all':
			year=request.GET['year_search']
			criterions.append(Q(date__icontains=year))
		if request.GET['during_the_creation']==u'now':
			criterions.append(Q(date_film__day=public_date.day))
			criterions.append(Q(date_film__month=public_date.month))
			criterions.append(Q(date_film__year=public_date.year))
		if request.GET['during_the_creation']==u'3_day':
			delta_date=datetime.timedelta(days=-3)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['during_the_creation']==u'week':
			delta_date=datetime.timedelta(weeks=-1)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['during_the_creation']==u'month':
			delta_date=datetime.timedelta(days=-30)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['during_the_creation']==u'3_month':
			delta_date=datetime.timedelta(days=-91)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['during_the_creation']==u'6_month':
			delta_date=datetime.timedelta(days=-183)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['during_the_creation']==u'year':
			delta_date=datetime.timedelta(days=-365)
			criterions.append(Q(date_film__gte=(public_date+delta_date)))
		if request.GET['sort']==u'down':
			if request.GET['sort_search']==u'add_date':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-date_film')
			if request.GET['sort_search']==u'review':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-count')
			if request.GET['sort_search']==u'coments':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).annotate(com=Count('coments')).order_by('-com')
			if request.GET['sort_search']==u'rating':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('-ratings_film')
		if request.GET['sort']==u'up':
			if request.GET['sort_search']==u'add_date':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('date_film')
			if request.GET['sort_search']==u'review':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('count')
			if request.GET['sort_search']==u'coments':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).annotate(com=Count('coments')).order_by('com')
			if request.GET['sort_search']==u'rating':
				allfilm=Films.objects.filter(reduce(operator.and_,criterions)).order_by('ratings_film')
				
		form_advanced_search=AdvancedSearchForm(label_suffix='',initial={'advanced_search':search})
		form_seaech=SearchForm(label_suffix='',initial={'search':request.GET['search'],
														'genre_search':request.GET['genre_search'],
														'where_search':request.GET['where_search'],
														'year_search':request.GET['year_search'],
														'during_the_creation':request.GET['during_the_creation'],
														'sort_search':request.GET['sort_search'],
														'sort':request.GET['sort']})
		#return HttpResponse(allfilm)
	return render_to_response( 'search.html', locals(), context_instance=RequestContext(request))

def advanced_search(request):
	form_seaech=SearchForm(label_suffix='')
	return render_to_response( 'advanced_search.html', {'form_seaech':form_seaech}, context_instance=RequestContext(request))




