import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_market.settings')
django.setup()

from django.test import Client

def main():
    c = Client()
    try:
        response = c.post('/accounts/register/', {
            'username': 'testuser123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser123@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        print(f"Status: {response.status_code}")
        if response.status_code != 302:
            print("Response not 302. Checking context for form errors...")
            if hasattr(response, 'context') and response.context and response.context.get('form'):
                print(response.context['form'].errors)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
