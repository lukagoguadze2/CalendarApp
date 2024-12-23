from hashids import Hashids
from django.conf import settings

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)


def generate_user_hash(user_id):
    return hashids.encode(user_id)


def decode_user_hash(user_hash):
    decoded = hashids.decode(user_hash)
    return decoded[0] if decoded else None
