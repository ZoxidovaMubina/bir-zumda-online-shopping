from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

from django.shortcuts import render


from app_shopping.models import ProductModel, Product, UserModel
from app_shopping.utils import generate_code, send_register_email


# Create your views here.
def index(request):
    products = ProductModel.objects.all()
    context = {'products': products}
    return render(request, 'app/index.html', context)

def mahsulotlar(request):
    products = Product.objects.all()
    query = request.GET.get('search')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__icontains=query))

    sort_option = request.GET.get('sort')

    if sort_option == 'low_price':
        products = products.order_by('price')
    elif sort_option == 'high_price':
        products = products.order_by('-price')
    elif sort_option == 'newest':
        products = products.order_by('created_at')

    context = {'products': products, 'sort_option': sort_option}
    return render(request, 'app/mahsulotlar.html', context)

def blog(request):
    return render(request, 'app/blog.html')
def bizhaqimizda(request):
    return render(request, 'app/biz-haqimizda.html')
def aloqa(request):
    return render(request, 'app/aloqa.html')
def mahsulot_detail(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    context = {'product': product}
    return render(request, 'app/mahsulot-detail.html', context)

def register_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # 1. Validation checks
        if password != password2:
            return render(request, 'app/register.html', {'error': 'Passwords do not match!'})

        if not password.isdigit():
            return render(request, 'app/register.html', {'error': 'Password must contain numbers only!'})

        if UserModel.objects.filter(name=name).exists():
            return render(request, 'app/register.html', {'error': 'Username already exists!'})

        # 2. Save user to database
        try:
            user = UserModel.objects.create(
                name=name,
                email=email,
                password=password,
            )
        except IntegrityError:
            return render(request, 'app/register.html', {'error': 'Database error: Duplicate or invalid fields!'})

        # 3. Session generation
        code = generate_code()
        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)

        # 4. Email sending with error catching
        try:
            send_register_email(to_email=user.email, code=code)
        except Exception as e:
            # Print exact email error to terminal console for debugging
            print("EMAIL SENDING FAILED:", str(e))
            return render(request, 'app/register.html', {
                'error': f'User saved, but email failed to send: {str(e)}'
            })

        return redirect('confirm_password')

    return render(request, 'app/register.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserModel.objects.get(email=email)

        login(request=request, user=user)
        return redirect("index")
    return render(request, "app/login.html")



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = UserModel.objects.filter(email__iexact=email).first()

        if not user:
            messages.error(
                request, "Ushbu email bo'yicha foydalanuvchi topilmadi."
            )
            return render(
                request, "app/forgot-password.html", {"email": email}
            )

        code = generate_code()
        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)
        send_register_email(to_email=user.email, code=code)
        return redirect("confirm_password")


    return render(request, 'app/forgot-password.html')

def confirm_password(request):
    if request.POST.get("code") == request.session.get("verify_code"):
        return redirect("login")

    user = UserModel.objects.filter(id=request.session.get("verify_user_id "))
    user.is_active = True
    request.session.pop("verify_code", None)
    request.session.pop("verify_user_id", None)
    return render(request, 'app/confirm_password.html')