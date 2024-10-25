import os 
from .. import app_dir
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Config:
    MEDIA_DIR = os.getenv('MEDIA_DIR', os.path.join(app_dir, 'media'))
    ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpg', 'image/jpeg']
    MAX_IMAGE_SIZE = 24000
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
    TOKEN_LIFE = 120
    
    ALLOWED_HOSTS = ["*"]
    ALLOWED_METHODS = ["*"]
    ALLOWED_HEADERS = ["*"]

    TEMPLATE_PATH = "static/template/"
    TEMPLATE_ADMIN_PATH = TEMPLATE_PATH + "adminpanel"
    ERROR_404_TEMPLATE = "error404.html"
    DEFAULT_TEMPLATE = "default.html"
    DEFAULT_CATEGORY_TEMPLATE = "default_category.html"




class ConfigSite:
        SITE_NAME = "GNU w0rld App FrameWork"
