from django.core.mail import send_mail
from django.conf import settings


def send_registration_email(to_email):
    print(to_email)
    subject = 'Đăng ký thành công'
    message = 'Chúc mừng bạn đã đăng ký thành công!'
    from_email = settings.EMAIL_HOST_USER  # Địa chỉ email đã cấu hình trong settings.py

    try:
        send_mail(subject, message, from_email, [to_email])
        print("Email đã được gửi thành công.")
    except Exception as e:
        print("Lỗi khi gửi email:", e)


def send_email_to_user(user, hotel_request):
    subject = 'Yêu cầu khách sạn của bạn đã được chấp nhận!'
    message = f'''
    Xin chào {user.username},

    Chúng tôi vui mừng thông báo rằng yêu cầu khách sạn của bạn đã được chấp nhận và khách sạn "{hotel_request.hotel_name}" đã được tạo thành công!

    Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi.

    Trân trọng,
    Đội ngũ hỗ trợ
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

