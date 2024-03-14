import json
import time
import hmac
import base64
import hashlib
import requests
from decimal import Decimal
from django.urls import reverse
from django import template
from django.utils.html import escapejs
from django.conf import settings

from ..config import get_config

register = template.Library()


@register.simple_tag
def baton_config():
    # retrieve the default language
    default_language = None
    try:
        default_language = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
    except AttributeError:
        default_language = settings.LANGUAGES[0][0]
    except:
        pass

    # retrieve other languages for translations
    other_languages = []
    try:
        other_languages = [l[0] for l in settings.LANGUAGES if l[0] != default_language]
    except:
        pass

    ai_config = get_config('AI') or {}

    conf = {
        "api": {
            "app_list": reverse('baton-app-list-json'),
            "gravatar": reverse('baton-gravatar-json'),
        },
        "ai": {
            "enableTranslations": ai_config.get('ENABLE_TRANSLATIONS', False) if (get_config('BATON_CLIENT_ID') and get_config('BATON_CLIENT_SECRET')) else False,
            "enableCorrections": ai_config.get('ENABLE_CORRECTIONS', False) if (get_config('BATON_CLIENT_ID') and get_config('BATON_CLIENT_SECRET')) else False,
            "translateApiUrl": reverse('baton-translate'),
            "summarizeApiUrl": reverse('baton-summarize'),
            "generateImageApiUrl": reverse('baton-generate-image'),
            "correctApiUrl": reverse('baton-correct'),
        },
        "confirmUnsavedChanges": get_config('CONFIRM_UNSAVED_CHANGES'),
        "showMultipartUploading": get_config('SHOW_MULTIPART_UPLOADING'),
        "enableImagesPreview": get_config('ENABLE_IMAGES_PREVIEW'),
        "changelistFiltersInModal": get_config('CHANGELIST_FILTERS_IN_MODAL'),
        "changelistFiltersAlwaysOpen": get_config('CHANGELIST_FILTERS_ALWAYS_OPEN'),
        "changelistFiltersForm": get_config('CHANGELIST_FILTERS_FORM'),
        "changeformFixedSubmitRow": get_config('CHANGEFORM_FIXED_SUBMIT_ROW'),
        "collapsableUserArea": get_config('COLLAPSABLE_USER_AREA'),
        "menuAlwaysCollapsed": get_config('MENU_ALWAYS_COLLAPSED'),
        "menuTitle": escapejs(get_config('MENU_TITLE')),
        "messagesToasts": get_config('MESSAGES_TOASTS'),
        "gravatarDefaultImg": get_config('GRAVATAR_DEFAULT_IMG'),
        "gravatarEnabled": get_config('GRAVATAR_ENABLED'),
        "loginSplash": get_config('LOGIN_SPLASH'),
        "searchField": get_config('SEARCH_FIELD'),
        "forceTheme": get_config('FORCE_THEME'),
        "defaultLanguage": default_language,
        "otherLanguages": other_languages,
    }

    return conf


@register.simple_tag
def baton_config_value(key):
    return get_config(key)

@register.inclusion_tag('baton/footer.html', takes_context=True)
def footer(context):
    user = context['user']
    return {
        'user': user,
        'support_href': get_config('SUPPORT_HREF'),
        'site_title': get_config('SITE_TITLE'),
        'copyright': get_config('COPYRIGHT'),
        'powered_by': get_config('POWERED_BY'),
    }


@register.simple_tag(takes_context=True)
def call_model_admin_method(context, **kwargs):
    try:
        model_admin = kwargs.pop('model_admin')
        method = kwargs.pop('method')
        return getattr(model_admin, method)(context['request'], **kwargs)
    except Exception as e:
        return None


@register.filter
def to_json(python_dict):
    return json.dumps(python_dict)


@register.inclusion_tag('baton/ai_stats.html', takes_context=True)
def baton_ai_stats(context):
    user = context['user']

    # The API endpoint to communicate with
    # url_post = "https://baton.sqrt64.it/api/v1/stats/"
    url_post = "http://192.168.1.245:1323/api/v1/stats/"

    # A GET request to the API
    ts = str(int(time.time()))
    h = hmac.new(settings.BATON_AI_CLIENT_SECRET.encode('utf-8'), ts.encode('utf-8'), hashlib.sha256)
    sig = base64.b64encode(h.digest()).decode()

    error = False
    errorMessage = None
    status_code = 200
    budget = 0
    translations = {}
    summarizations = {}
    corrections = {}
    images = {}
    response_json = {}

    try:
        response = requests.get(url_post, headers={
            'X-Client-Id': settings.BATON_AI_CLIENT_ID,
            'X-Timestamp': ts,
            'X-Signature': sig,
        })

        status_code = response.status_code
        if status_code != 200:
            error = True
            try:
                errorMessage = response.json().get('message', None)
            except:
                pass
        else:
            response_json = response.json()
            budget = round(Decimal(response_json.get('budget', 0.0)), 2)
            translations = response_json.get('translations', {})
            summarizations = response_json.get('summarizations', {})
            corrections = response_json.get('corrections', {})
            images = response_json.get('images', {})
    except:
        error = True

    return {
        'user': user,
        'error': error,
        'error_message': errorMessage,
        'status_code': status_code,
        'budget': budget,
        'translations': translations,
        'summarizations': summarizations,
        'corrections': corrections,
        'images': images,
    }
