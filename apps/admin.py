from django.contrib import admin
from . models import RegisterUser, Project, Task, Writers


admin.site.register(Project),
admin.site.register(Task),
admin.site.register(Writers),
admin.site.register(RegisterUser)