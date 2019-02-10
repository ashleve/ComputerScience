from django.db import models



class Movie(models.Model):
	title = models.CharField(max_length=100)
	genre = models.CharField(max_length=50)
	rating = models.FloatField()	# average score of the movie
	num_of_ratings = models.IntegerField()	# number of people who rated the film
	# role = models.ManyToManyField('Actors', through='MovieCast')

	def __str__(self):
		return self.title



class Actor(models.Model):
	name = models.CharField(max_length=40)
	surname = models.CharField(max_length=40)
	age = models.PositiveSmallIntegerField()

	MALE = 'male'
	FEMALE = 'female'
	OTHER = 'other'
	GENDERS = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(OTHER, 'Other')
	)
	gender = models.CharField(max_length=15, choices=GENDERS)

	def __str__(self):
		return f'{self.name} {self.surname}'



class MovieCast(models.Model):
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True) 
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

	LEAD = 'lead'
	SUPPORTING = 'supportive'
	FEATURED = 'featured'
	BACKGROUND = 'background'
	ROLES = (
		(LEAD, 'Lead'),
		(SUPPORTING, 'Supporting'),
		(FEATURED, 'Featured'),	# has a few lines of dialog
		(BACKGROUND, 'Background')	# small role, few or no lines
	)
	role = models.CharField(max_length=15, choices=ROLES)




