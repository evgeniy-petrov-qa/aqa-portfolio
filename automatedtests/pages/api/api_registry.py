from automatedtests.pages.api.respons_models.accounts_models import AccountHoldersResponse

api_registry = {
    'checking_contact:get': {
        'endpoint': '/fdx/v5/accounts/deposit_01_checking/contact',
        'method': 'GET',
        'model':AccountHoldersResponse,
        'request_model': None,
    }
}
