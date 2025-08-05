JAZZMIN_SETTINGS = {
    "site_title": "Nestorc",
    "site_header": "Nestorc",
    "site_brand": "Nestorc",
    "welcome_sign": "Welcome to Nestorc Admin Panel",
    "copyright": "Nestorc",
    "search_model": ["accounts.CustomUser", "auth.Group"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["accounts.view_customuser"]},
      #   {"name": "📄 Download All Users PDF", "url": "admin:download_all_users_pdf", "permissions": ["accounts.view_customuser"], "new_window": True},
    ],
    "app_labels": {
        "accounts": "",
    },
    "icons": {
        "accounts.CustomUser": "fas fa-users",
        "accounts": "fas fa-user-circle",
        "auth.Group": "fas fa-users-cog",
        "services": "fas fa-concierge-bell",
    },
    "hide_apps": [
        "auth",
        "contenttypes",
        "sessions",
        "messages",
        "staticfiles",
        "admin",
    ],
    "hide_models": [
        "account.emailaddress",
        "account.passwordresetcode",
        "accounts.passwordresetcode",
        "authtoken.token",
        "authtoken.tokenproxy",
        "sites.site",
        "socialaccount.socialaccount",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "token_blacklist.blacklistedtoken",
        "token_blacklist.outstandingtoken",
        "rest_framework_simplejwt.token_blacklist.blacklistedtoken",
        "rest_framework_simplejwt.token_blacklist.outstandingtoken",
        "django_rest_passwordreset.resetpasswordtoken",
        "dj_rest_auth.tokenmodel",
        "allauth.account.emailaddress",
        "allauth.account.emailconfirmation",
        ],
}


JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # Themes: cerulean, cosmo, darkly, flatly, etc.
    "navbar": "navbar-dark bg-primary",
    "footer_fixed": True,
    "body_small_text": False,
}

# Additional configuration for development vs production
JAZZMIN_DEVELOPMENT_SETTINGS = {
    "show_ui_builder": True,  # Enable UI builder in development
}

JAZZMIN_PRODUCTION_SETTINGS = {
    "show_ui_builder": False,  # Disable UI builder in production
}


