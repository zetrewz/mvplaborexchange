from django.db.models import Model, ForeignKey, CASCADE, BooleanField

from resume.models import Resume
from vacancy.models import Vacancy


class Application(Model):
    resume = ForeignKey(Resume, on_delete=CASCADE)
    vacancy = ForeignKey(Vacancy, on_delete=CASCADE)
    applied = BooleanField(default=False)

    def __str__(self):
        return (f'{self.vacancy.company_name}---{self.vacancy.name} | '
                f'{self.resume.first_name} {self.resume.last_name}'
                f'---{self.resume.work_name}')
