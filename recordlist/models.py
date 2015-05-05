from django.db import models

# Create your models here.


class Record(models.Model):
    recordId = models.AutoField(primary_key=True)
    srNumber = models.BigIntegerField(null=True)
    customer = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)
    openDate = models.DateField(null=True)
    modifiedDate = models.DateField(null=True)
    touchDate = models.DateField(null=True)
    closeDate = models.DateField(null=True)
    escalationLevel = models.CharField(max_length=512, null=True)
    calReviewDate = models.DateField(null=True)
    calSummary = models.TextField(null=True)
    overallStatus = models.TextField(null=True)
    reviewRequired = models.NullBooleanField(default=True, null=True)
    calPriority = models.IntegerField(default=3)
    faultCategory = models.TextField(null=True)

