from django.db import models

from taggit.managers import TaggableManager
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, EmailMessage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractUser

from django.db.models.query import QuerySet



CCY_LIST = (('GBP', "Pounds Sterling"),("EUR","Euro"), ("USD","US Dollars"))

class MyUser(AbstractUser):

    paid_points = models.IntegerField(default=0)
    new_points = models.IntegerField(default=0)



class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)

class ObjItemMixin(object):

    def open(self):
        return self.filter(status='A')

    def done(self):
        return self.filter(status='P')


class ObjItemQuerySet(QuerySet, ObjItemMixin):
    pass

class ObjManager(models.Manager, ObjItemMixin):
    def get_query_set(self):
        return ObjItemQuerySet(self.model, using=self._db)



class Object(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=120, unique=True, help_text="Copy name exactly as it appears on shopping website")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ccy = models.CharField(max_length=3, choices=CCY_LIST, default="USD", help_text="Select Currency")
    buy_link = models.URLField(blank=True, null=True)
    img_link = models.URLField(blank=True, null=True)
    feet = models.IntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser)

    tags = TaggableManager()
    objects = ObjManager()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)

    @property
    def footprints(self):
        from web.tables import FootprintTable
        return FootprintTable(Footprint.objects.filter(object=self))

    @property
    def feet_required(self):
        count = Footprint.objects.filter(object=self).count()
        return 3-count

class Footprint(models.Model):
    object = models.ForeignKey(Object)
    source = models.URLField(help_text="URL of source of footprint", unique=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Footprint size in kg", validators=[MinValueValidator(0),
                                       MaxValueValidator(100000)])

    notes = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser)

    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['object__name']
        unique_together = ['object','size']

    def __unicode__(self):
        return u'%s - %s kg' % (self.object.name,self.size)

    #def get_absolute_url(self):
    #    return reverse('scrud_detail', args=[self.pk])

    def save(self, *args, **kwargs):

        new =  not self.id

        if not new:
            old = Footprint.objects.get(id=self.id)


        super(Footprint, self).save(*args, **kwargs)

        if new:

            ## more points if first footprint
            #c = Footprint.objects.filter(object=self.object).count()
            #if c > 1:
            #    points = 5
            #else:
            #    points = 10
            points = 1

            Points.objects.create(user=self.created_by, points=points, object=self.object, footprint=self, comment="Added new Footprint")

            self.object.feet +=1
            self.object.save()
        else:
            # award points when verified
            if self.verified and not old.verified:
                points = 1

                Points.objects.create(user=self.created_by, points=points, object=self.object, footprint=self, comment="Footprint verified")


    def delete(self):
        self.object.feet -=1
        self.object.save()
        super(Footprint, self).delete()



class Points(models.Model):

    user = models.ForeignKey(MyUser)
    points = models.IntegerField(max_length=5, default=1)
    object = models.ForeignKey(Object)
    footprint = models.ForeignKey(Footprint)
    comment = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    pending = models.BooleanField(default=True)
    redeemed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        unique_together = ['object','footprint']
        verbose_name_plural = "Points"

    def __unicode__(self):
        return u'Footprint for %s - %s points' % (self.object.name,self.points)

    def save(self, *args, **kwargs):

        if not self.id:
            self.user.new_points += self.points
            self.user.save()

        super(Points, self).save(*args, **kwargs)

    @property
    def redeemed(self):
        return self.redeemed_date
