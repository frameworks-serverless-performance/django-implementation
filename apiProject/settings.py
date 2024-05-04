from pathlib import Path
from botocore.config import Config
import boto3

BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

ROOT_URLCONF = 'apiProject.urls'
WSGI_APPLICATION = 'apiProject.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# initialize DynamoDB client
botoConfig = Config(
    region_name='eu-central-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)
dynamodb = boto3.client('dynamodb', config=botoConfig)
globals()['DYNAMODB_CLIENT'] = dynamodb
