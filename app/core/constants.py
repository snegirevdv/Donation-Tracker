"""Constants used in the app."""

JWT_LIFETIME = 3600


class MinLength:
    USER_PASSWORD = 3
    PROJECT_NAME = 5
    PROJECT_DESCRIPTION = 10


class MaxLength:
    PROJECT_NAME = 100


class Message:
    PASSWORD_LEN_ERROR = (
        f'The password must be at least {MinLength.USER_PASSWORD} characters long.'
    )
    PASSWORD_EMAIL_ERROR = 'The password cannot contain your email.'
    PROJECT_EXISTS = 'A project with this name already exists!'
    PROJECT_SMALL_FULL_AMOUNT = (
        'The full_amount cannot be set lower than the already invested amount.'
    )
    PROJECT_CLOSED = 'A closed project cannot be edited!'
    PROJECT_INVESTED = 'Funds have been invested in the project, it cannot be deleted!'


class Field:
    PROJECT_NAME = (
        f'Project name (from {MinLength.PROJECT_NAME} '
        f'to {MaxLength.PROJECT_NAME} characters)'
    )
    PROJECT_DESCRIPTION = (
        f'Project description (at least {MinLength.PROJECT_DESCRIPTION} characters)'
    )
    PROJECT_FULL_AMOUNT = 'Required amount, a positive integer'
    DONATION_FULL_AMOUNT = 'Donation amount'
    DONATION_COMMENT = 'Comment on the donation'
