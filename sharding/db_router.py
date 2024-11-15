import hashlib

from django.conf import settings


class HashShardRouter:
    SHARDS = list(settings.DATABASES.keys())[1:]

    # 모든 데이터베이스에서 마이그레이션 허용
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

    def get_shard(self, user_id):
        hash_val = int(hashlib.sha256(str(user_id).encode()).hexdigest(), 16)
        shard_index = hash_val % len(self.SHARDS)
        return self.SHARDS[shard_index]

    def db_for_write(self, model, **hints):
        if hasattr(model, "user_id"):
            return self.get_shard(model.user_id)
        return "default"

    def db_for_read(self, model, **hints):
        if hasattr(model, "user_id"):
            return self.get_shard(model.user_id)
        return "default"
