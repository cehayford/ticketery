from rest_framework_sso import claims

def create_authorization_payload(session_token, user, account, **kwargs):
    return {
        claims.TOKEN: claims.TOKEN_AUTHORIZATION,
        claims.SESSION_ID: session_token.pk,
        claims.USER_ID: user.pk,
        claims.EMAIL: user.email,
        'account': account.pk,
    }