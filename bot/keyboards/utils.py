from asgiref.sync import sync_to_async
from app_store.models import BotUser

@sync_to_async
def get_user_lang(user_id: int) -> str:
    try:
        user = BotUser.objects.get(telegram_id=user_id)
        return user.lang
    except BotUser.DoesNotExist:
        return "uz"
