from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg
from datetime import *
from django.views.decorators.cache import never_cache
from django.db.models import Q
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Create your views here.
def index(request):
    four_books = addBook.objects.all()[:4]
    books = addBook.objects.all()
    print(books)
    top_books = []
    for i in books:
        reviews = addReview.objects.filter(title=i.title, bookId=i.id)
        average_rating = reviews.aggregate(Avg('rating')).get('rating__avg') or 0
        for rev in reviews:
            all_user = addUser.objects.filter(email=rev.email)
            for user in all_user:
                top_books.append({
                    'all_user': user,
                    'book': i,
                    'reviews': rev,
                    'date': rev.published_date,
                    'average_rating': average_rating
                })
    latest_review = top_books
    top_book = sorted(top_books, key=lambda x: x["average_rating"], reverse=True)
    latest_review.sort(key=lambda x: x['date'], reverse=True)
    latest_review = latest_review[:3]
    if top_book:
        top_book = top_book[0]
    print(top_book)
    return render(request, 'index.html', {'carousel_books': four_books, 'top_book': top_book,
                                          'latest_review': latest_review})


def loginPage(request):
    return render(request, 'login.html')


def adminloginPage(request):
    return render(request, 'adminLogin.html')


def publisherloginPage(request):
    return render(request, 'publisherLogin.html')


def userSignupPage(request):
    return render(request, 'userSignup.html')


def PublisherSignupPage(request):
    return render(request, 'publisherSignup.html')


def homepage(request):
    books = addBook.objects.all()
    four_books = addBook.objects.all()[:4]
    mail = request.session.get('id')
    users = addUser.objects.get(email=mail)
    top_books = []
    for i in books:
        review = addReview.objects.filter(title=i.title, bookId=i.id)
        average_rating = review.aggregate(Avg('rating'))['rating__avg'] or 0
        for rev in review:
            all_user = addUser.objects.filter(email=rev.email)
            for user in all_user:
                top_books.append({
                    'book': i,
                    'review': rev,
                    'date': rev.published_date,
                    'average_rating': average_rating,
                    'user': user.user_photo
                })
    latest_review = top_books

    top_book = sorted(top_books, key=lambda x: x['average_rating'], reverse=True)
    latest_review.sort(key=lambda x: x['date'], reverse=True)
    latest_review = latest_review[:3]
    if top_book:
        top_book = top_book[0]
    else:
        print("empty")

    return render(request, 'home.html',
                  {'mail': mail, 'books': four_books, 'user': users, 'top_book': top_book,
                   'latest_review': latest_review})


def Bookpublishpage(request):
    mail = request.session.get('id')
    return render(request, 'publishBook.html', {'mail': mail})


def copyrightformpage(request, id):
    book = addBook.objects.get(pk=id)
    return render(request, 'copyrightForm.html', {'book': book})


def removalrequestpage(request):
    requests = copyrightapplied.objects.all()
    flag = 'False'
    for req in requests:
        books = addBook.objects.filter(pk=req.book_Id)
        if not books.exists():
            flag = 'True'
    return render(request, 'requestDisplay.html', {'requests': requests, 'flag': flag})


def adminBookdisplay(request):
    all_book = addBook.objects.all()
    # book_info = all_book
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminBookdisplay))
        if member:
            all_book = addBook.objects.filter(Q(title__icontains=member))
            if all_book:
                print("match found")
            else:
                print("no match")
        else:
            print("no input")
    return render(request, 'adminbookdisp.html', {'books': all_book})


def adminbookmanage(request):
    all_books = addBook.objects.all()
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminbookmanage))
        if member:
            all_books = addBook.objects.filter(Q(title__icontains=member))
            if all_books:
                print("match found")
            else:
                print("no match")
        else:
            print("no input")
    return render(request, 'adminbookManage.html', {'books': all_books})


def publisherhomepage(request):
    mail = request.session.get('id')
    print(f"home: {mail}")
    publisher = addPublisher.objects.get(email=mail)
    books = addBook.objects.filter(email=mail)[:4]
    all_books = addBook.objects.filter(email=mail)
    mail = request.session.get('id')
    # user = addUser.objects.get(email=mail)
    top_book = []
    for i in all_books:
        review = addReview.objects.filter(title=i.title, bookId=i.id)

        for rev in review:
            all_user = addUser.objects.filter(email=rev.email)
            average_rating = review.aggregate(Avg('rating'))['rating__avg'] or 0
            for user in all_user:
                top_book.append({
                    'book': i,
                    'review': rev,
                    'average_rating': average_rating,
                    'profile_photo': user.user_photo
                })

    top_book.sort(key=lambda x: x['average_rating'], reverse=True)
    if top_book:
        top_book = top_book[0]
    else:
        print("empty")
    all_rev = []
    for i in all_books:
        reviews = addReview.objects.filter(title=i.title)
        for j in reviews:
            all_user = addUser.objects.filter(email=j.email)
            for user in all_user:
                all_rev.append({
                    'review': j,
                    'date': j.published_date,
                    'profile_photo': user.user_photo
                })
    sorted_reviews = sorted(all_rev, key=lambda x: x['date'], reverse=True)
    latest_review = sorted_reviews[:3]

    return render(request, 'publisherHome.html',
                  {'user': publisher, 'books': books, 'top_book': top_book, 'latest_review': latest_review})


@never_cache
def publisherreviewpage(request):
    mail = request.session.get('id')  # Get logged-in user's email from session
    sort_option = request.GET.get('sort', 'recent')  # Get the sorting option from the URL, default to 'recent'
    related_reviews = []

    publisher_books = addBook.objects.filter(email=mail)  # Get books by the publisher

    # Collect each review as a separate entity
    for book in publisher_books:
        reviews = addReview.objects.filter(title=book.title)
        for review in reviews:  # Treat each review individually
            related_reviews.append({
                'book': book,
                'review': review,
                'rating': review.rating,
                'published_date': review.published_date,
            })

    # Sorting logic based on the 'sort' parameter
    if sort_option == 'top_rated':
        # Sort by highest rating
        related_reviews = sorted(related_reviews, key=lambda x: x['rating'], reverse=True)
    elif sort_option == 'least_rated':
        # Sort by lowest rating
        related_reviews = sorted(related_reviews, key=lambda x: x['rating'])
    else:  # Default is 'recent'
        # Sort by most recent review date
        related_reviews = sorted(related_reviews, key=lambda x: x['published_date'], reverse=True)
    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()
        if not book_title and 'searchInput' in request.GET:
            return redirect(reverse(publisherreviewpage))
        if book_title:
            related_reviews = [
                i for i in related_reviews if i['book'].title.lower() == book_title.lower()
            ]
            if related_reviews:
                print(f"Found {len(related_reviews)} matching book(s).")
            else:
                print("No matching book found.")
        else:
            print("No search input provided.")

    return render(request, 'publisherReview.html', {'reviews': related_reviews, 'sort_option': sort_option})


def adminreviewmanagepage(request):
    reviews = addReview.objects.all()
    review_info = []
    for i in reviews:
        user = addUser.objects.get(email=i.email)
        review_info.append({
            'review': i,
            'username': user.name
        })

    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminreviewmanagepage))
        if member:
            review_info = [
                i for i in review_info if i['review'].name.lower() == member.lower()
            ]
            print(review_info)
            if review_info:
                print("match found")
            else:
                print("no match")
        else:
            print("no input")
    return render(request, 'adminReviewmanage.html', {'reviews': review_info})


def adminpublishermanagepage(request):
    publishers = addPublisher.objects.all()
    publisher_info = publishers
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminpublishermanagepage))
        if member:
            publisher_info = addPublisher.objects.filter(Q(name__icontains=member))
            if publisher_info:
                print("match found")
            else:
                print("no match")
                publisher_info = []
        else:
            print("no input")
    return render(request, 'adminPublishermanage.html', {'publishers': publisher_info})


def publishercopyrightspage(request):
    sort_option = request.GET.get('sort', 'recent')
    mail = request.session.get('id')
    books = addBook.objects.all()
    reviews = addReview.objects.all()

    books_with_ratings = []

    for book in books:
        book_reviews = reviews.filter(title=book.title, bookId=book.id)
        average_rating = book_reviews.aggregate(Avg('rating'))['rating__avg']

        # is_publisher_match = book.email == mail

        if average_rating is None:
            average_rating = 0

        books_with_ratings.append({
            'book': book,
            'average_rating': round(average_rating, 1)
        })

    if sort_option == 'top_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
    elif sort_option == 'least_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'])
    else:  # Default is recent
        books_with_ratings.sort(key=lambda x: x['book'].published_date, reverse=True)

    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()
        if not book_title and 'searchInput' in request.GET:
            return redirect(reverse(publishercopyrightspage))
        if book_title:
            books_with_ratings = [
                i for i in books_with_ratings if i['book'].title.lower() == book_title.lower()
            ]

            if books_with_ratings:
                print(f"Found {len(books_with_ratings)} matching book(s).")
            else:
                print("No matching book found.")
        else:
            print("No search input provided.")
    return render(request, 'publishercopyright.html',
                  {'books_with_ratings': books_with_ratings, 'sort_option': sort_option})


def adminusermanagepage(request):
    users = addUser.objects.all()
    print(users)
    user_info = users
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminusermanagepage))
        if member:
            user_info = addUser.objects.filter(Q(name__icontains=member))
            if user_info:
                print("match found")
            else:
                print("no match")
                user_info = []
        else:
            print("no input")
    return render(request, 'adminUsermanage.html', {'users': user_info})


def adminhomepage(request):
    users = addUser.objects.all()
    requests = copyrightapplied.objects.all()
    print(users)
    user_info = users
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminhomepage))
        if member:
            user_info = addUser.objects.filter(Q(name__icontains=member))
            if user_info:
                print("match found")
            else:
                print("no match")
                user_info = []
        else:
            print("no input")

    return render(request, 'adminHome.html', {'users': user_info, 'requests': requests})


def adminpublisherdisplay(request):
    publishers = addPublisher.objects.all()
    publisher_info = publishers
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminpublisherdisplay))
        if member:
            publisher_info = addPublisher.objects.filter(Q(name__icontains=member))
            if publisher_info:
                print("match found")
            else:
                print("no match")
                publisher_info = []
        else:
            print("no input")
    return render(request, 'adminHomepublishersection.html', {'publishers': publisher_info})


def adminreviewdisplay(request):
    reviews = addReview.objects.all()
    review_info = reviews
    if request.method == 'GET':
        member = request.GET.get('searchInput')
        if not member and 'searchInput' in request.GET:
            return redirect(reverse(adminreviewdisplay))
        if member:
            review_info = addReview.objects.filter(name=member)
            print(review_info)
            if review_info:
                print("match found")
            else:
                print("no match")
                review_info = []
        else:
            print("no input")
    return render(request, 'adminHomereviewsection.html', {'reviews': review_info})


def reviewpage(request):
    review = addReview.objects.all()
    sort_option = request.GET.get('sort', 'recent')
    book_review = []
    for i in review:
        user_all = addUser.objects.filter(email=i.email)
        book = addUser.objects.get(email=i.email)
        for user in user_all:
            book_review.append({
                'review': i,
                'username': book.name,
                'profile_photo': user.user_photo
            })
    if sort_option == 'top_rated':
        book_review.sort(key=lambda x: x['review'].rating, reverse=True)
    elif sort_option == 'least_rated':
        book_review.sort(key=lambda x: x['review'].rating)
    elif sort_option == 'your_reviews':
        book_review = [
            i for i in book_review if i['review'].email == request.session.get('id')
        ]
    else:
        book_review.sort(key=lambda x: x['review'].published_date, reverse=True)

    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()
        if not book_title and 'searchInput' in request.GET:
            return redirect(reverse(reviewpage))
        if book_title:
            book_review = [
                i for i in book_review if i['review'].title.lower() == book_title.lower()
            ]
            print(book_review)
            if book_review:
                print(f"Found {len(book_review)} matching book(s).")
            else:
                print("No matching book found.")
        else:
            print("No search input provided.")

    return render(request, 'review.html', {'book_review': book_review, 'sort_option': sort_option})


def userallbookspage(request):
    sort_option = request.GET.get('sort', 'recent')
    # mail = request.session.get('id')
    books = addBook.objects.all()

    books_with_ratings = []

    for book in books:
        book_reviews = addReview.objects.filter(title=book.title, bookId=book.id)
        average_rating = book_reviews.aggregate(Avg('rating'))['rating__avg']
        print(book_reviews)
        print(average_rating)

        if average_rating is None:
            average_rating = 0

        books_with_ratings.append({
            'book': book,
            'average_rating': round(average_rating, 1)
        })
    if sort_option == 'top_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
    elif sort_option == 'least_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'])
    else:  # Default is recent
        books_with_ratings.sort(key=lambda x: x['book'].published_date, reverse=True)

    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()
        if not book_title and 'searchInput' in request.GET:
            return redirect(reverse(userallbookspage))
        if book_title:
            books_with_ratings = [
                i for i in books_with_ratings if i['book'].title.lower() == book_title.lower()
            ]

            if books_with_ratings:
                print(f"Found {len(books_with_ratings)} matching book(s).")
            else:
                print("No matching book found.")
        else:
            print("No search input provided.")

    return render(request, 'userAllbooks.html', {'books_with_ratings': books_with_ratings, 'sort_option': sort_option})


def userlibrarypage(request):
    email = request.session.get('id', None)

    books = addtoLibrary.objects.filter(email=email)
    books_with_ratings = []

    for book in books:
        # Get the review for this book and publisher
        review = addReview.objects.filter(title=book.title, email=email, bookId=book.book_ID).first()

        # Assign the rating or 'No Rating' if no review exists
        book.rating = review.rating if review else "No Rating"

        # Get all matching books from addBook (to handle duplicates)
        matching_books = addBook.objects.filter(title=book.title, pk=book.book_ID)

        for book_details in matching_books:
            # Append each matching book with its id to the dictionary
            books_with_ratings.append({
                'book': book,  # The book from the library
                'book_id': book_details.id,  # The id from addBook
            })

        # If no matching books are found, add the book with no ID
        if not matching_books.exists():
            books_with_ratings.append({
                'book': book,
                'book_id': None  # No book id found
            })

    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()

        if book_title:
            books_with_ratings = [
                i for i in books_with_ratings if i['book'].title.lower() == book_title.lower()
            ]
        elif 'searchInput' in request.GET:
            return redirect(reverse(userlibrarypage))
    return render(request, 'userLibrary.html', {'books': books_with_ratings})


def publisherallbookspage(request):
    email = request.session.get('id', None)
    sort_option = request.GET.get('sort', 'recent')
    mail = request.session.get('id')
    books_with_ratings = []
    if email:
        books = addBook.objects.filter(email=email)
        for book in books:
            average_rating = addReview.objects.filter(title=book.title, bookId=book.id).aggregate(Avg('rating'))[
                'rating__avg']

            is_publisher_match = book.email == mail

            if average_rating is None or not is_publisher_match:
                average_rating = 0

            books_with_ratings.append({
                'book': book,
                'average_rating': round(average_rating, 1)
            })
    else:
        books = addBook.objects.none()
    if sort_option == 'top_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
    elif sort_option == 'least_rated':
        books_with_ratings.sort(key=lambda x: x['average_rating'])
    else:
        books_with_ratings.sort(key=lambda x: x['book'].published_date, reverse=True)

    if request.method == "GET":
        book_title = request.GET.get('searchInput', '').strip()
        if not book_title and 'searchInput' in request.GET:
            return redirect(reverse(publisherallbookspage))
        if book_title:
            books_with_ratings = [
                i for i in books_with_ratings if i['book'].title.lower() == book_title.lower()
            ]

            if books_with_ratings:
                print(f"Found {len(books_with_ratings)} matching book(s).")
            else:
                print("No matching book found.")
        else:
            print("No search input provided.")

    return render(request, 'publisherAllbooks.html', {'books_with_ratings': books_with_ratings,
                                                      'sort_option': sort_option})


def adduserAction(request):
    if request.method == "POST":
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('mail', '')
        usr = request.POST.get('username', '')
        pas = request.POST.get('password', '')
        con_pass = request.POST.get('conf_password', '')
        gen = request.POST.get('gender', 'not specified')
        picture = request.FILES.get('pic', None) or 'no photo'
        data = addUser.objects.filter(email=em)
        if pas == con_pass:
            if data:
                messages.info(request, 'email already exists')
                return redirect(userSignupPage)
            else:
                data1 = addUser.objects.create(name=nm, phone=ph, email=em, username=usr, password=pas, gender=gen,
                                               user_photo=picture)
                data1.save()
                messages.info(request, 'record added')
                return redirect(userSignupPage)
        else:
            messages.info(request, 'Password Mismatch.Try Again!!')
            return redirect(userSignupPage)


def addpublisherAction(request):
    if request.method == "POST":
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('mail', '')
        b_type = request.POST.get('bs_type') or 'Self-Publisher'
        cmp_nm = request.POST.get('cmp_name') or 'nil'
        # print(f"b_type: {b_type}, cmp_nm: {cmp_nm}")
        # print(request.POST)
        gen = request.POST.get('gender', 'not specified')
        usr = request.POST.get('username', '')
        pic = request.FILES.get('photo', None)
        pas = request.POST.get('password', '')
        con_pass = request.POST.get('conf_password', '')
        data = addPublisher.objects.filter(email=em)
        if pas == con_pass:
            if data:
                messages.info(request, 'email already exists')
                return redirect(PublisherSignupPage)
            else:
                data1 = addPublisher.objects.create(name=nm, phone=ph, email=em, business_Type=b_type,
                                                    company_Name=cmp_nm,
                                                    username=usr, password=pas, gender=gen, publisher_photo=pic)
                data1.save()
                messages.info(request, 'record added')
                return redirect(PublisherSignupPage)
        else:
            messages.info(request, 'Password Mismatch.Try Again!!')
            return redirect(PublisherSignupPage)


def userloginAction(request):
    if request.method == "POST":
        em = request.POST['mail']
        pas = request.POST['password']
        data = addUser.objects.filter(email=em)
        print(em)
        if data:
            data1 = addUser.objects.get(email=em)
            if data1.password == pas:
                request.session['id'] = em
                print(request.session.get('id'))
                return redirect(homepage)
            else:
                messages.info(request, 'wrong E-mail or Password.Try Again!!')
                return redirect(loginPage)
        else:
            messages.info(request, 'wrong E-mail or Password.Try Again!!')
            return redirect(loginPage)


def userlogoutAction(request):
    if 'id' in request.session:
        request.session.flush()
        return redirect(index)
    else:
        mail = request.session.get('id', None)
        return HttpResponse(mail)


def adminloginAction(request):
    if request.method == "POST":
        nm = request.POST['name']
        pas = request.POST['password']
        data = adminlog.objects.filter(username=nm)
        if data:
            data1 = adminlog.objects.get(username=nm)
            if data1.password == pas:
                request.session['id'] = nm
                return redirect(adminhomepage)
            else:
                messages.info(request, 'wrong Username or Password.Try Again!!')
                return redirect(adminloginPage)
        else:
            messages.info(request, 'wrong Username or Password.Try Again!!')
            return redirect(adminloginPage)


def publisherloginAction(request):
    if request.method == "POST":
        em = request.POST['mail']
        pas = request.POST['password']
        data = addPublisher.objects.filter(email=em)
        if data:
            data1 = addPublisher.objects.get(email=em)
            if data1.password == pas:
                request.session['id'] = em
                return redirect(publisherhomepage)
            else:
                messages.info(request, 'wrong E-mail or Password.Try Again!!')
                return redirect(publisherloginPage)
        else:
            messages.info(request, 'wrong E-mail or Password.Try Again!!')
            return redirect(publisherloginPage)


def addbookaction(request):
    if request.method == "POST":
        nm = request.POST.get('name', '')
        em = request.POST.get('mail', '')
        aut_nm = request.POST.get('authorname', '')
        title = request.POST.get('title', '')
        genre = request.POST.get('genre')
        date = request.POST.get('date', 'not specified')
        pic = request.FILES.get('photo', None)
        desc = request.POST.get('desc', '')
        data = addBook.objects.create(name=nm, email=em, authors_name=aut_nm, title=title, genre=genre,
                                      published_date=date, book_photo=pic, description=desc)
        data.save()
        messages.info(request, 'book added')
        return redirect(publisherhomepage)


def deletebookaction(request, id):
    data = addBook.objects.filter(pk=id)
    # data.save()
    print(data)
    for book in data:
        book.delete()
        addtoLibrary.objects.filter(title=book.title, book_ID=book.id).delete()
        addReview.objects.filter(title=book.title, bookId=book.id).delete()
    messages.info(request, 'Book Deleted')
    return redirect(publisherallbookspage)


def updatebookaction(request):
    if request.method == "POST":
        ID = request.POST.get('bookId', '')
        bookTitle = request.POST.get('title', '')
        bookAuthor = request.POST.get('author', '')
        bookGenre = request.POST.get('genre', '')
        bookDate = request.POST.get('publishedDate', '')
        bookPhoto = request.FILES.get('photo')
        bookDesc = request.POST.get('desc', '')
        if bookPhoto:
            upd = addBook.objects.filter(id=ID).first()
            upd.book_photo = bookPhoto
            addBook.objects.filter(id=ID).update(authors_name=bookAuthor,
                                                       title=bookTitle,
                                                       genre=bookGenre,
                                                       published_date=bookDate,
                                                       book_photo=bookPhoto,
                                                       description=bookDesc)
            upd.save()

        else:
            addBook.objects.filter(id=ID).update(authors_name=bookAuthor,
                                                 title=bookTitle,
                                                 genre=bookGenre,
                                                 published_date=bookDate,
                                                 description=bookDesc)
        messages.info(request, 'Book Updated!')
        return redirect(publisherallbookspage)


def library(request, book_id):
    user_email = request.session.get('id')
    if not user_email:
        return redirect(loginPage)
    book = get_object_or_404(addBook, pk=book_id)
    print(book)
    print(book.id)
    if not addtoLibrary.objects.filter(email=user_email, book_ID=book_id).exists():
        addtoLibrary.objects.create(email=user_email, book_ID=book_id, photo=book.book_photo, title=book.title,
                                    author_name=book.authors_name)
        messages.info(request, 'Added to library')
    else:
        messages.info(request, 'Already added to library')

    return redirect(userallbookspage)


def deletefromLibrary(request, id):
    data = addtoLibrary.objects.filter(pk=id).delete()
    messages.info(request, 'Book Removed From Library!!')
    return redirect(userlibrarypage)


def submit_review(request):
    if request.method == 'POST':
        booknum = request.POST['bid']
        name = request.POST['name']
        mail = request.session.get('id')  # Assuming user email is in session
        author = request.POST['author']
        title = request.POST['title']
        rating = int(request.POST['rating'])  # Convert the rating value to an integer
        date = request.POST['publishedDate']
        review = request.POST['review']

        rev = addReview.objects.filter(email=mail, title=title)
        if rev:
            addReview.objects.filter(email=mail, title=title).update(name=name,
                                                                     bookId=booknum,
                                                                     email=mail,
                                                                     authors_name=author,
                                                                     title=title,
                                                                     rating=rating,
                                                                     published_date=date,
                                                                     review=review)
            messages.info(request, 'Review updated successfully!')

        # Save the review data to the database
        else:
            addReview.objects.create(
                bookId=booknum,
                name=name,
                email=mail,
                authors_name=author,
                title=title,
                rating=rating,
                published_date=date,
                review=review
            )

            messages.info(request, 'Review submitted successfully!')
        return redirect(userlibrarypage)


def userdeleteaction(request, id):
    data = addUser.objects.filter(pk=id)
    for user in data:
        addtoLibrary.objects.filter(email=user.email).delete()
    data.delete()
    messages.info(request, "User Deleted")
    return redirect(adminusermanagepage)


def publisherdeleteaction(request, id):
    data = addPublisher.objects.filter(pk=id)
    for user in data:
        addBook.objects.filter(email=user.email).delete()
    data.delete()
    messages.info(request, "Publisher Deleted")
    return redirect(adminpublishermanagepage)


def reviewdeleteaction(request, id):
    addReview.objects.filter(pk=id).delete()
    messages.info(request, "Review Deleted")
    return redirect(adminreviewmanagepage)


def publisherupdateaction(request, id):
    if request.method == "POST":
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('mail', '')
        b_type = request.POST.get('bs_type') or 'Self-Publisher'
        cmp_nm = request.POST.get('cmp_name') or 'nil'
        # print(f"b_type: {b_type}, cmp_nm: {cmp_nm}")
        print(request.POST)
        gen = request.POST.get('gender', 'not specified')
        usr = request.POST.get('username', '')

        addPublisher.objects.filter(pk=id).update(name=nm,
                                                  phone=ph,
                                                  email=em,
                                                  business_Type=b_type,
                                                  company_Name=cmp_nm,
                                                  username=usr,
                                                  gender=gen)
        messages.info(request, "Publisher Details Updated!")
        return redirect(adminpublishermanagepage)


def userupdateaction(request, id):
    if request.method == "POST":
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('mail', '')
        usr = request.POST.get('username', '')
        gen = request.POST.get('gender', 'not specified')

        addUser.objects.filter(pk=id).update(name=nm, phone=ph, email=em, username=usr, gender=gen)
        messages.info(request, "User Details Updated!")
        return redirect(adminusermanagepage)


def homeuserupdateaction(request, id):
    if request.method == "POST":
        pic = request.FILES.get('picture')
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('ml', '')
        usr = request.POST.get('username', '')

        if pic:
            d = addUser.objects.get(pk=id)
            d.user_photo = pic
            d.save()
            addUser.objects.filter(pk=id).update(name=nm,
                                                 phone=ph,
                                                 email=em,
                                                 username=usr,
                                                 )
            request.session['id'] = em
            messages.info(request, "User Details Updated!")
            return redirect(homepage)

        else:
            addUser.objects.filter(pk=id).update(name=nm,
                                                 phone=ph,
                                                 email=em,
                                                 username=usr)
            request.session['id'] = em
            messages.info(request, "User Details Updated!")
            return redirect(homepage)


def homepublisherupdateaction(request, id):
    if request.method == "POST":
        mail = request.session.get('id')
        pic = request.FILES.get('picture')
        nm = request.POST.get('name', '')
        ph = request.POST.get('phone', '')
        em = request.POST.get('ml', '')
        usr = request.POST.get('username', '')

        if pic:
            d = addPublisher.objects.get(pk=id)
            addBook.objects.filter(email=mail).update(email=em)
            d.publisher_photo = pic
            d.email = em
            request.session['id'] = em
            d.save()
            addUser.objects.filter(pk=id).update(name=nm,
                                                 phone=ph,
                                                 username=usr)
            print(f"upd: {mail}")
            messages.info(request, "User Details Updated!")
            return redirect(publisherhomepage)

        else:
            d = addPublisher.objects.get(pk=id)
            addBook.objects.filter(email=mail).update(email=em)
            d.email = em
            request.session['id'] = em

            d.save()
            addPublisher.objects.filter(pk=id).update(name=nm,
                                                      phone=ph,
                                                      username=usr)
            messages.info(request, "User Details Updated!")
            print(f"upd: {mail}")
            return redirect(publisherhomepage)


def admindeletebookaction(request, id):
    data = addBook.objects.filter(pk=id)
    # data.save()
    print(data)
    for book in data:
        book.delete()
        addtoLibrary.objects.filter(title=book.title, book_ID=book.id).delete()
        addReview.objects.filter(title=book.title, bookId=book.id).delete()
    messages.info(request, 'Book Deleted')
    return redirect(adminbookmanage)


def adminupdatebookaction(request, id):
    if request.method == "POST":
        pubName = request.POST.get('name', '')
        bookTitle = request.POST.get('title', '')
        bookAuthor = request.POST.get('author', '')
        bookGenre = request.POST.get('genre', '')
        bookDate = request.POST.get('publishedDate', '')
        addBook.objects.filter(pk=id).update(authors_name=bookAuthor,
                                             title=bookTitle,
                                             genre=bookGenre,
                                             published_date=bookDate,
                                             name=pubName)

        messages.info(request, 'Book Updated!')
        return redirect(adminbookmanage)


def copyrightapplyaction(request):
    # BOOK DETAILS
    if request.method == "POST":
        book_title = request.POST.get('title')
        b_id = request.POST.get('b_id')
        pub_name = request.POST.get('pub_name')
        pub_date = request.POST.get('date')

        # USER DETAILS

        u_name = request.POST.get('user_name')
        u_email = request.POST.get('email')
        u_phone = request.POST.get('phone')

        # REASON

        rem_reason = request.POST.get('reason')

        # DECLARATION

        decl = request.POST.get('declaration')
        sig = request.FILES.get('signature')
        doc = request.FILES.get('document')

        data = copyrightapplied.objects.create(book_Name=book_title,
                                               book_Id=b_id,
                                               published_Name=pub_name,
                                               published_Date=pub_date,
                                               name=u_name,
                                               email=u_email,
                                               phone_Number=u_phone,
                                               reason=rem_reason,
                                               declaration=decl,
                                               signature=sig,
                                               document=doc)
        print(request.POST)
        data.save()
        messages.info(request, 'requested for removal!')
        return redirect(publishercopyrightspage)


def requestaccept(request, id):
    requestcpy = copyrightapplied.objects.get(pk=id)
    requestcpy.status = 'Approved'
    requestcpy.save()
    # book = addBook.objects.get(id=requestcpy.book_Id)
    subject = "Approval Notification"
    recipient_mail = requestcpy.email
    body = f'We are pleased to inform you that your request to use {requestcpy.book_Name} has been approved. If you have any further questions or need additional information, feel free to reach out.'
    try:
        email_ver_act(recipient_mail, body, subject)
        messages.info(request, "Email Send")
    except:
        messages.info(request, "Network Error")
    return redirect(removalrequestpage)


def requestreject(request, id):
    requestcpy = copyrightapplied.objects.get(pk=id)
    requestcpy.status = 'Rejected'
    requestcpy.save()
    # book = addBook.objects.get(id=requestcpy.book_Id)
    subject = "Rejection Notification"
    recipient_mail = requestcpy.email
    body = f'We are pleased to inform you that your request to use {requestcpy.book_Name} has been Rejected. If you have any further questions or need additional information, feel free to reach out.'
    try:
        email_ver_act(recipient_mail, body, subject)
        messages.info(request, "Email Send")
    except:
        messages.info(request, "Network Error")

    return redirect(removalrequestpage)


def rembookreq(request, id, rid):
    data = addBook.objects.filter(pk=id)
    if not data.exists():
        messages.info(request, 'Book already deleted')
        return redirect(removalrequestpage)

    requestcpy = copyrightapplied.objects.get(pk=rid)
    books = addBook.objects.get(id=requestcpy.book_Id)
    print(data)
    for book in data:
        book.delete()
        addtoLibrary.objects.filter(title=book.title, book_ID=book.id).delete()
        addReview.objects.filter(title=book.title, bookId=book.id).delete()
    subject = "Book Removal Notification"
    recipient_mail = books.email
    body = f'We are pleased to inform you that your book {requestcpy.book_Name} has been Removed due to copyright. If you have any further questions or need additional information, feel free to reach out. '
    if books:
        try:
            email_ver_act(recipient_mail, body, subject)
            messages.info(request, "Email Send")
            messages.info(request, 'Book Deleted')

        except:
            messages.info(request, "Network Error")
    else:
        messages.info(request, "book not found")

    return redirect(removalrequestpage)


def remrequest(request, id):
    copyrightapplied.objects.get(pk=id).delete()
    messages.info(request, 'Request Removed')

    return redirect(removalrequestpage)


# EMAIL
def email_ver_act(e, msgs, subject):
    # Email configuration
    sender_email = 'akheeelfaisal@gmail.com'
    password = 'yleawtjifdwweuci'

    # Create the email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = e
    msg['Subject'] = subject
    msg.attach(MIMEText(msgs, 'plain'))

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, e, msg.as_string())
