from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ..usuarios.models import Provincia

class Encuesta(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True,default=None)

	def __str__(self):
		return (self.name)

class Dimension(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True, default=None)
	encuesta= models.ForeignKey(Encuesta, blank=True, null=True)

	def __str__(self):
		return (self.name)

class Survey(models.Model):
	class Meta:
		verbose_name = "Subtema"
		verbose_name_plural = "Subtemas"
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True, default=None)
	completada = models.BooleanField(default=False)
	orden = models.IntegerField (null=True, default=1)
	dimension= models.ForeignKey(Dimension, blank=True, null=True)


	def __str__(self):
		return (self.name)

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return None

class Category(models.Model):
	class Meta:
		verbose_name = "Indicador"
		verbose_name_plural = "Indicadores"
	name = models.CharField(max_length=400)
	orden = models.IntegerField(null=True, default=1)
	survey = models.ForeignKey(Survey)

	def __str__(self):
		return (str(self.orden) + " - "+self.name)

def validate_list(value):
	'''takes a text value and verifies that there is at least one comma '''
	values = value.split(';')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
	class Meta:
		verbose_name = "Pregunta"
		verbose_name_plural = "Preguntas"
	TEXT = 'text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)

	text = models.TextField()
	required = models.BooleanField(default=True)
	category = models.ForeignKey(Category, blank=True, null=True, verbose_name="Indicador")
	survey = models.ForeignKey(Survey)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=RADIO)
	# the choices field is only used if the question type
	choices = models.TextField(blank=True, null=True,
		help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

	def save(self, *args, **kwargs):
		if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
			or self.question_type == Question.SELECT_MULTIPLE):
			validate_list(self.choices)
		super(Question, self).save(*args, **kwargs)

	def get_choices(self):
		''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
		choices = self.choices.split(';')
		choices_list = []
		for c in choices:
			c = c.strip()
			choices_list.append((c,c))
		choices_tuple = tuple(choices_list)
		return choices_tuple

	def __str__(self):
		return (self.text)

class ResponseMgr(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	completada= models.BooleanField(default=False, blank=True)
	comentarios = models.TextField(blank=True, null=True)
	#organizacion = models.CharField(max_length=200,blank=True, null=True)
	#provincia = models.ForeignKey(Provincia, default=1, null=True)
	encuesta = models.ForeignKey(Encuesta, default=1)
	user = models.ForeignKey(User,default=1)

	def __str__(self):
		return ("Id = "+str(self.id)+" - "+self.encuesta.name +" - "+self.created.strftime('%Y-%m-%d'))

class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	completada = models.BooleanField(default=False, blank=True)
	survey = models.ForeignKey(Survey)
	#interviewer = models.CharField('Entrevistador', max_length=400, default='System')
	#interviewee = models.CharField('Entrevistado', max_length=400, default='System')
	#conditions = models.TextField('Condiciones durante la encuesta', blank=True, null=True)
	#comments = models.TextField('Comentarios', blank=True, null=True)
	interview_uuid = models.CharField('Identificador unico de encuesta', max_length=36)
	user = models.ForeignKey(User,default=1)
	respMgr = models.ForeignKey(ResponseMgr, default='', blank=True, null=True)

	def __str__(self):
		return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
	body = models.IntegerField(blank=True, null=True)
