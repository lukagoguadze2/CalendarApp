from django.db import models


class Syllabus(models.Model):
    course = models.OneToOneField('universities.Course', on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='syllabus/')


class StudyMaterial(models.Model):
    course = models.ForeignKey('universities.Course', on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()  # Week number (1 to N); 0 - for general materials
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.week_number == 0:
            return f"General: {self.course.name} Study Materials"

        return f"Study Material for Week {self.week_number} - {self.course.name}"

    def __repr__(self):
        return f"StudyMaterial(Week {self.week_number}: {self.course.name})"


class StudyMaterialFile(models.Model):
    name = models.CharField(max_length=255)
    study_material = models.ForeignKey(StudyMaterial, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='study_materials/')  # The actual file (can be PDF, Word, etc.)
    description = models.TextField(null=True, blank=True)  # Optional description of the file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # When the file was uploaded

    def __str__(self):
        return f"File for {self.study_material.title} - {self.file.name}"
