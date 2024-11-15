# database sharding

## 샤딩

데이터베이스를 여러 개로 나누는 것으로 각 샤드는 서로 다른 물리적 서버에 존재 가능. 각 샤드는 독립적으로 작동하며 데이터를 삽입할 때 데이터 분포 규칙에 따라 특정 샤드에 저장. 샤딩을 구현하는 데는 다양한 전략이 있으며 그중 가장 많이 사용되는 것이 **해시 기반 샤딩**으로 이 방법은 특정 키(예: 사용자 ID)에 대한 해시 값을 계산하여 데이터를 어떤 샤드에 저장할지 결정.

### 예시

```python
# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "default.sqlite3",
    },
    "shard1": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "shard1.sqlite3",
    },
    "shard2": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "shard2.sqlite3",
    },
}

DATABASE_ROUTERS = ["path.to.db_router.ShardRouter"]

# db_router.py
import hashlib


class HashShardRouter:
    SHARDS = ["shard1", "shard2"]

    # 해시 기반으로 샤드를 선택
    def get_shard(self, user_id):
        # SHA256 해시 사용 후 10진수로 변환
        hash_val = int(hashlib.sha256(str(user_id).encode()).hexdigest(), 16)
        # 샤드 개수로 나눈 나머지 연산을 통해 샤드 선택
        shard_index = hash_val % len(self.SHARDS)
        return self.SHARDS[shard_index]

    # 데이터를 저장할 데이터베이스를 결정하는 로직
    def db_for_write(self, model, **hints):
        if hasattr(model, "user_id"):
            return self.get_shard(model.user_id)
        return "default"

    # 데이터를 읽을 데이터베이스를 결정하는 로직
    def db_for_read(self, model, **hints):
        if hasattr(model, "user_id"):
            return self.get_shard(model.user_id)
        return "default"

```

위와 같이 여러 샤드를 준비하고 각각에 저장 및 불러오기가 가능
