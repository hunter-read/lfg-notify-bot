from enum import Enum
import json
import os
import time

import redis


class AbstractRedisObject:
    @property
    def _list_name(self) -> str:
        raise NotImplementedError

    def serialize(self) -> str:
        raise NotImplementedError

    def deserialize(self, data: any):
        raise NotImplementedError


class Notification(AbstractRedisObject):

    _list_name = "lfg-notification"

    class NotificationType(int, Enum):
        SUBMISSION = 1
        OVERLIMIT = 2

    def __init__(self, **kwargs):
        self.username: str = kwargs.get("username", None)
        self.subject: str = kwargs.get("subject", None)
        self.body: str = kwargs.get("body", None)
        self.type: Notification.NotificationType = kwargs.get("type", None)

    def serialize(self) -> str:
        data = {
            "username": self.username,
            "subject": self.subject,
            "body": self.body,
            "type": self.type
        }
        return json.dumps(data, indent=None)

    def deserialize(self, binary: bin):
        data = json.loads(binary.decode("utf-8"))
        self.username = data["username"]
        self.subject = data["subject"]
        self.body = data["body"]
        self.type = Notification.NotificationType(data["type"])
        return self


class Redis:
    def __init__(self):
        self.__redis: redis.Redis = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'))
        self.__backoff: int = 1

    def push(self, data: AbstractRedisObject) -> None:
        success = False
        while not success:
            try:
                self.__redis.lpush(data._list_name, data.serialize())
                self.__backoff = 1
                success = True
            except redis.exceptions.ConnectionError as e:
                self.backoff_or_raise()



    def append(self, data: AbstractRedisObject) -> None:
        success = False
        while not success:
            try:
                self.__redis.rpush(data._list_name, data.serialize())
                self.__backoff = 1
                success = True
            except redis.exceptions.ConnectionError as e:
                self.backoff_or_raise()

    def blocking_pop(self, obj: AbstractRedisObject) -> None:
        success = False
        while not success:
            try:
                obj.deserialize(self.__redis.blpop(obj._list_name)[1])
                self.__backoff = 1
                success = True
            except redis.exceptions.ConnectionError as e:
                self.backoff_or_raise()
        
    def backoff_or_raise(self) -> None:
        if (self.__backoff > 8): 
            self.__backoff = 1
            raise Exception("Redis is down")
        time.sleep(15*self.__backoff)
        self.__backoff *= 2
