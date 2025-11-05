
# 타사 스토리지에 채팅 기록 저장

## 프로그래밍 언어 선택

이 자습서에서는 사용자 지정 `ChatMessageStore` 를 구현하고  
이를 `ChatAgent` 와 함께 사용하여 **에이전트 채팅 기록을 외부 스토리지에 저장**하는 방법을 보여줍니다.

기본적으로 `ChatAgent` 를 사용하는 경우,
서비스에서 지원하면 채팅 기록은 `AgentThread` 객체 메모리 또는 기본 유추 서비스에 저장됩니다.

하지만 다음 상황에서는 **사용자 지정 저장소**가 필요할 수 있습니다:

- 서비스가 기록 저장을 지원하지 않는 경우
- 자체 저장소를 사용하고 싶은 경우
- 장기 세션 유지가 필요한 경우

---

## 필수 조건

필수 구성 요소는 다음 단계를 참조하세요:

- 이 자습서의 **간단한 에이전트 만들기 및 실행**

---

## 사용자 지정 ChatMessageStore 만들기

사용자 지정 메시지 저장소를 만들려면  
`ChatMessageStore` 프로토콜을 구현해야 합니다.

핵심 메서드:

| 메서드 | 역할 |
|--------|------|
| `add_messages` | 새 메시지를 저장 |
| `list_messages` | 저장된 메시지를 검색 |

`list_messages` 는 반드시 **오름차순(과거→미래)** 으로 반환해야 합니다.

**⚠️ 중요한 점**

- 모델이 처리할 수 있는 메시지 수 제한을 고려해야 합니다.
- 요약/트리밍은 `list_messages()` 내부에서 수행해야 합니다.

---

## 직렬화

`ChatMessageStore` 인스턴스는 다음 시점에 생성 및 연결됩니다:

- 스레드를 처음 생성할 때
- 직렬화된 스레드 상태를 다시 로드할 때

따라서 저장소는 외부 데이터(키, 설정 값)를  
`serialize_state / deserialize_state` 로 유지/복원해야 합니다.

---

## Redis 기반 ChatMessageStore 예시

다음 구현은 Redis `LIST` 구조를 사용합니다:

- `RPUSH`: 메시지를 시간순으로 추가
- `LRANGE`: 메시지를 오름차순으로 조회
- `LTRIM`: 오래된 메시지 자동 제거 가능

```python
from collections.abc import Sequence
from typing import Any
from uuid import uuid4
from pydantic import BaseModel
import json
import redis.asyncio as redis
from agent_framework import ChatMessage


class RedisStoreState(BaseModel):
    """State model for serializing and deserializing Redis chat message store data."""

    thread_id: str
    redis_url: str | None = None
    key_prefix: str = "chat_messages"
    max_messages: int | None = None


class RedisChatMessageStore:
    """Redis-backed implementation of ChatMessageStore using Redis Lists."""

    def __init__(
        self,
        redis_url: str | None = None,
        thread_id: str | None = None,
        key_prefix: str = "chat_messages",
        max_messages: int | None = None,
    ) -> None:
        """Initialize the Redis chat message store.

        Args:
            redis_url: Redis connection URL (for example, "redis://localhost:6379").
            thread_id: Unique identifier for this conversation thread.
                      If not provided, a UUID will be auto-generated.
            key_prefix: Prefix for Redis keys to namespace different applications.
            max_messages: Maximum number of messages to retain in Redis.
                         When exceeded, oldest messages are automatically trimmed.
        """
        if redis_url is None:
            raise ValueError("redis_url is required for Redis connection")

        self.redis_url = redis_url
        self.thread_id = thread_id or f"thread_{uuid4()}"
        self.key_prefix = key_prefix
        self.max_messages = max_messages

        # Initialize Redis client
        self._redis_client = redis.from_url(redis_url, decode_responses=True)

    @property
    def redis_key(self) -> str:
        """Get the Redis key for this thread's messages."""
        return f"{self.key_prefix}:{self.thread_id}"

    async def add_messages(self, messages: Sequence[ChatMessage]) -> None:
        """Add messages to the Redis store.

        Args:
            messages: Sequence of ChatMessage objects to add to the store.
        """
        if not messages:
            return

        # Serialize messages and add to Redis list
        serialized_messages = [self._serialize_message(msg) for msg in messages]
        await self._redis_client.rpush(self.redis_key, *serialized_messages)

        # Apply message limit if configured
        if self.max_messages is not None:
            current_count = await self._redis_client.llen(self.redis_key)
            if current_count > self.max_messages:
                # Keep only the most recent max_messages using LTRIM
                await self._redis_client.ltrim(self.redis_key, -self.max_messages, -1)

    async def list_messages(self) -> list[ChatMessage]:
        """Get all messages from the store in chronological order.

        Returns:
            List of ChatMessage objects in chronological order (oldest first).
        """
        # Retrieve all messages from Redis list (oldest to newest)
        redis_messages = await self._redis_client.lrange(self.redis_key, 0, -1)

        messages = []
        for serialized_message in redis_messages:
            message = self._deserialize_message(serialized_message)
            messages.append(message)

        return messages

    async def serialize_state(self, **kwargs: Any) -> Any:
        """Serialize the current store state for persistence.

        Returns:
            Dictionary containing serialized store configuration.
        """
        state = RedisStoreState(
            thread_id=self.thread_id,
            redis_url=self.redis_url,
            key_prefix=self.key_prefix,
            max_messages=self.max_messages,
        )
        return state.model_dump(**kwargs)

    async def deserialize_state(self, serialized_store_state: Any, **kwargs: Any) -> None:
        """Deserialize state data into this store instance.

        Args:
            serialized_store_state: Previously serialized state data.
            **kwargs: Additional arguments for deserialization.
        """
        if serialized_store_state:
            state = RedisStoreState.model_validate(serialized_store_state, **kwargs)
            self.thread_id = state.thread_id
            self.key_prefix = state.key_prefix
            self.max_messages = state.max_messages

            # Recreate Redis client if the URL changed
            if state.redis_url and state.redis_url != self.redis_url:
                self.redis_url = state.redis_url
                self._redis_client = redis.from_url(self.redis_url, decode_responses=True)

    def _serialize_message(self, message: ChatMessage) -> str:
        """Serialize a ChatMessage to JSON string."""
        message_dict = message.model_dump()
        return json.dumps(message_dict, separators=(",", ":"))

    def _deserialize_message(self, serialized_message: str) -> ChatMessage:
        """Deserialize a JSON string to ChatMessage."""
        message_dict = json.loads(serialized_message)
        return ChatMessage.model_validate(message_dict)

    async def clear(self) -> None:
        """Remove all messages from the store."""
        await self._redis_client.delete(self.redis_key)

    async def aclose(self) -> None:
        """Close the Redis connection."""
        await self._redis_client.aclose()
```

---

## 정리

이 방식으로:

✅ 외부 스토리지(DB, Redis, Blob, Redis Cloud 등)에 메시지 저장
✅ 장기 세션 가능
✅ 서버 재시작 후에도 기록 복원
✅ 모델 입력 길이 제어 가능

---

## 추천 확장 아이디어

* Azure Table Storage 버전 구현
* Cosmos DB 기반 ChatStore
* S3(Bucket) 기반 JSON 스토리지
* OpenSearch 기반 검색형 대화 기억

