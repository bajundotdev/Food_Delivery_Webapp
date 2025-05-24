# Import all form classes to make them available when importing from package
# app/forms/__init__.py
from .admin_form import ProductForm
from .shopping_form import CartForm
from .main_form import BaseUserForm, LoginForm, RegistrationForm, PasswordChangeForm
# from .forms import BaseUserForm, RegistrationForm, LoginForm, PasswordChangeForm, AdminUserForm, SearchForm, CartOperationForm, OrderStatusForm