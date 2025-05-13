from dataclasses import dataclass
from flask import Blueprint, request, render_template, redirect
from ..forms import RegistrationForm
from ..models import User, UserAddress, Order
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')