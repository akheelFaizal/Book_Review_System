from django.db import models


# Create your models here.

class addUser(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    gender_choices = [('male', 'male'), ('female', 'female'), ('not specified', 'not specified')]
    gender = models.CharField(max_length=200, choices=gender_choices, default='not specified')
    user_photo = models.FileField(max_length=200, default='no photo')

    def __str__(self):
        return self.name


class addPublisher(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    business_Type = models.CharField(max_length=200)
    company_Name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    gender_choices = [('male', 'male'), ('female', 'female'), ('not specified', 'not specified')]
    gender = models.CharField(max_length=200, choices=gender_choices, default='not specified')
    publisher_photo = models.FileField(max_length=200)

    def __str__(self):
        return self.name


class adminlog(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class addBook(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    authors_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    published_date = models.CharField(max_length=200)
    book_photo = models.FileField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class addReview(models.Model):
    # book = models.ForeignKey(addBook, on_delete=models.CASCADE, related_name='all_books')
    bookId = models.IntegerField(default=None)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    authors_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    rating = models.IntegerField(null=True, blank=True)
    published_date = models.DateTimeField()
    review = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.title} by {self.name}"


class addtoLibrary(models.Model):
    book_ID = models.IntegerField(default=None)
    email = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200, default='nil')
    photo = models.FileField(max_length=500, default='no image')
    review = models.ForeignKey(addReview, on_delete=models.CASCADE,
                               related_name='library_items', null=True, blank=True)

    def __str__(self):
        return f"added {self.title} to library by {self.email}"


class copyrightapplied(models.Model):

    # BOOK DETAILS
    book_Name = models.CharField(max_length=200)
    book_Id = models.IntegerField()
    published_Date = models.CharField(max_length=200)
    published_Name = models.CharField(max_length=200, default="not set")

    # USER DETAILS
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_Number = models.CharField(max_length=200)

    # REASON
    reason = models.CharField(max_length=1000)

    # DECLARATION
    declaration = models.CharField(max_length=200)
    signature = models.FileField(max_length=200)
    document = models.FileField(max_length=200)

    # status
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
