import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_email(event, context):
    """
    Send email via serverless function.
    
    Expected payload:
    {
        "action": "SIGNUP_WELCOME" | "BOOKING_CONFIRMATION",
        "patient_email": "email@example.com",
        "patient_name": "John Doe",
        "doctor_name": "Dr. Smith",
        "date": "2025-12-20",
        "time": "14:00:00"
    }
    """
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'SIGNUP_WELCOME':
            return handle_signup_welcome(body)
        elif action == 'BOOKING_CONFIRMATION':
            return handle_booking_confirmation(body)
        else:
            return error_response(400, f"Unknown action: {action}")
    
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        return error_response(500, str(e))


def handle_signup_welcome(data):
    """Handle signup welcome email."""
    user_email = data.get('user_email')
    user_name = data.get('user_name')
    role = data.get('role')
    
    email_body = f"""
    Welcome to HMS!
    
    Hi {user_name},
    
    Thank you for signing up as a {role}.
    
    Your account is now active. You can log in at http://localhost:8000/auth/login/
    
    Best regards,
    HMS Team
    """
    
    logger.info(f"Sending welcome email to {user_email}")
    # In production, integrate with AWS SES or similar
    # ses.send_email(...) 
    
    return success_response({
        'message': 'Welcome email sent',
        'recipient': user_email
    })


def handle_booking_confirmation(data):
    """Handle booking confirmation email."""
    patient_email = data.get('patient_email')
    patient_name = data.get('patient_name')
    doctor_name = data.get('doctor_name')
    date = data.get('date')
    time = data.get('time')
    
    email_body = f"""
    Appointment Confirmation
    
    Hi {patient_name},
    
    Your appointment with {doctor_name} has been confirmed.
    
    Date: {date}
    Time: {time}
    
    Please arrive 10 minutes early.
    
    Best regards,
    HMS Team
    """
    
    logger.info(f"Sending booking confirmation to {patient_email}")
    # In production, integrate with AWS SES or similar
    # ses.send_email(...)
    
    return success_response({
        'message': 'Booking confirmation email sent',
        'recipient': patient_email
    })


def success_response(data):
    """Return success response."""
    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def error_response(status_code, message):
    """Return error response."""
    return {
        'statusCode': status_code,
        'body': json.dumps({'error': message}),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
def handle_signup_welcome(data):
    required = ["recipient_email", "recipient_name", "role"]
    validate_required_fields(data, required)

    logger.info(f"Sending welcome email to {data['recipient_email']}")

    return success_response({
        "message": "Welcome email sent",
        "recipient": data["recipient_email"]
    })
def handle_booking_confirmation_doctor(data):
    required = ["recipient_email", "recipient_name", "patient_name", "date", "time"]
    validate_required_fields(data, required)

    logger.info(f"Sending booking confirmation to doctor {data['recipient_email']}")

    return success_response({
        "message": "Booking notification sent to doctor",
        "recipient": data["recipient_email"]
    })
def validate_required_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
def success_response(data):
    return {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {"Content-Type": "application/json"}
    }


def error_response(status_code, message):
    return {
        "statusCode": status_code,
        "body": json.dumps({"error": message}),
        "headers": {"Content-Type": "application/json"}
    }
