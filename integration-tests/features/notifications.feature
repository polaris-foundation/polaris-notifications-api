Feature: Email notifications
    As a user
    I want to receive e-mail notifications
    So that I can manage my account on Sensyne products


    Scenario: Valid email type is sent
        Given there exists a user
        When a WELCOME_EMAIL is sent to the user
        Then the user receives the email

    Scenario: Email type for which there is no template
        Given there exists a user
        When a DUMMY_EMAIL is sent to the user
        Then the user does not receive the email