from django.db import models

#storing search logs 
class CaseQuery(models.Model):
    case_type = models.CharField(max_length=50)
    case_number = models.IntegerField()
    filing_year = models.IntegerField()
    raw_json = models.TextField()
    queried_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_type} {self.case_number}/{self.filing_year}"