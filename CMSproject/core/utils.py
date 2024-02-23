import json
from django.core.serializers.json import DjangoJSONEncoder
from uuid import UUID

class UUIDEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')  # or the appropriate encoding

    def dumps(self, obj, *args, **kwargs):
        return super().encode(obj, *args, **kwargs)
