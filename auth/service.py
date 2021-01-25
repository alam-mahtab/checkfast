# from fastapi import BackgroundTasks
# import jwt
# from jwt.exceptions import InvalidTokenError
# from datetime import datetime, timedelta
# from typing import Optional
# from tortoise.query_utils import Q

# #from src.config import settings

# #from src.app.user import schemas, service, models
# #from .send_email import send_new_account_email
# from .model import VerificationOut
# #, Verification

# async def verify_registration_user(uuid: VerificationOut) -> bool:
#     """ Подтверждение email пользователя """
#     verify = await Verification.get(link=uuid.link).prefetch_related("user")
#     if verify:
#         await service.user_s.update(schema=schemas.UserBaseInDB(is_active=True), id=verify.user.id)
#         await Verification.filter(link=uuid.link).delete()
#         return True
#     else:
#         return False