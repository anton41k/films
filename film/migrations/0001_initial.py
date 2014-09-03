# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Films'
        db.create_table('film_films', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('orig_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.IntegerField')()),
            ('studio_country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('poster', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('producer', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cast', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('translation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('detail', self.gf('django.db.models.fields.TextField')()),
            ('kinopoisk', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('down_load', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date_film', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('check_film', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ratings_film', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('film', ['Films'])

        # Adding M2M table for field genre on 'Films'
        db.create_table('film_films_genre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('films', models.ForeignKey(orm['film.films'], null=False)),
            ('genres', models.ForeignKey(orm['film.genres'], null=False))
        ))
        db.create_unique('film_films_genre', ['films_id', 'genres_id'])

        # Adding model 'Rating'
        db.create_table('film_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['film.Films'])),
            ('user_rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('film', ['Rating'])

        # Adding model 'AddUser'
        db.create_table('film_adduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('add', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='img/noavatar.png', max_length=100)),
            ('ICQ', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('film', ['AddUser'])

        # Adding M2M table for field user_sms on 'AddUser'
        db.create_table('film_adduser_user_sms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('adduser', models.ForeignKey(orm['film.adduser'], null=False)),
            ('smsuser', models.ForeignKey(orm['film.smsuser'], null=False))
        ))
        db.create_unique('film_adduser_user_sms', ['adduser_id', 'smsuser_id'])

        # Adding model 'SmsUser'
        db.create_table('film_smsuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('received', self.gf('django.db.models.fields.related.ForeignKey')(related_name='received', to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('sms', self.gf('django.db.models.fields.TextField')()),
            ('date_sms', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('film', ['SmsUser'])

        # Adding model 'Screens'
        db.create_table('film_screens', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('films', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screen', to=orm['film.Films'])),
            ('screen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('film', ['Screens'])

        # Adding model 'Coments'
        db.create_table('film_coments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('us', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('coment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['film.Films'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('answer_user', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('date_coment', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('film', ['Coments'])

        # Adding model 'Genres'
        db.create_table('film_genres', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_genre', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('film', ['Genres'])


    def backwards(self, orm):
        # Deleting model 'Films'
        db.delete_table('film_films')

        # Removing M2M table for field genre on 'Films'
        db.delete_table('film_films_genre')

        # Deleting model 'Rating'
        db.delete_table('film_rating')

        # Deleting model 'AddUser'
        db.delete_table('film_adduser')

        # Removing M2M table for field user_sms on 'AddUser'
        db.delete_table('film_adduser_user_sms')

        # Deleting model 'SmsUser'
        db.delete_table('film_smsuser')

        # Deleting model 'Screens'
        db.delete_table('film_screens')

        # Deleting model 'Coments'
        db.delete_table('film_coments')

        # Deleting model 'Genres'
        db.delete_table('film_genres')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'film.adduser': {
            'ICQ': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'AddUser'},
            'about_me': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'add': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'img/noavatar.png'", 'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_sms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['film.SmsUser']", 'null': 'True', 'blank': 'True'})
        },
        'film.coments': {
            'Meta': {'ordering': "['date_coment']", 'object_name': 'Coments'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_user': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'coment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['film.Films']"}),
            'date_coment': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'us': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'film.films': {
            'Meta': {'ordering': "['-date_film']", 'object_name': 'Films'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'check_film': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.IntegerField', [], {}),
            'date_film': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'detail': ('django.db.models.fields.TextField', [], {}),
            'down_load': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['film.Genres']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kinopoisk': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orig_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'producer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ratings_film': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'studio_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'translation': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'film.genres': {
            'Meta': {'ordering': "['name_genre']", 'object_name': 'Genres'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_genre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'film.rating': {
            'Meta': {'ordering': "['film']", 'object_name': 'Rating'},
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['film.Films']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'film.screens': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Screens'},
            'films': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screen'", 'to': "orm['film.Films']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'film.smsuser': {
            'Meta': {'ordering': "['-date_sms']", 'object_name': 'SmsUser'},
            'date_sms': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'received': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sms': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['film']