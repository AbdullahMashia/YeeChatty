
class Error_yee:

    user_taken = {
        'success':False,
        'type':'register',
        'm': 'user is taken'
    }
    email_exists={
        'type':'register',
        'success':False,
        'm':'email exists'

    }
    user_not_found ={
        'type':'find',
        'success':False,
        'm': 'user profile could be private'
        }


    wrong_creden ={
        'type':'login',
        'success':False,
        'm': 'email or password not correct'

    }
    password_match = {
        'type':'register',
        'success':False,
        'm': "password don't match"
    }
    request_sent ={
        'type':'requesnt_sent',
        'success':False,
        'm':'request already sent'

    }
    user_already_found = {
        'type':'find',
        'success':False,
        'm': "check your requests or chats for the user"
    }
    user_reverse_req = {
        "type":"send_request",
        "success":False,
        "m": "Can't send request to same account"

    }


