from django.db import models

class NotifyTemplet(models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=255)
    subject=models.CharField(max_length=255)
    txt_content=models.TextField()
    contain_variable=models.TextField()

    class Meta:
        db_table = 'notify_template'

    def __str__(self):
        return self.name