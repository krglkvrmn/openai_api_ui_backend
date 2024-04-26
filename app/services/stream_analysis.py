import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import AsyncIterator, Callable, Coroutine, Optional


class SystemEventsProcessorBase(ABC):
    def __init__(
        self,
        start_token: Optional[str] = None,
        end_token: Optional[str] = None,
        valid_system_events_action: Callable[[dict], Coroutine] = None
    ):
        self.__action = valid_system_events_action
        self.start_token = start_token.strip() if start_token else None
        self.end_token = end_token.strip() if end_token else None

    @abstractmethod
    async def analyse(self, system_events: list[dict]) -> tuple[bool, dict]:
        pass

    async def analyse_and_act(self, system_events: list[dict]) -> tuple[bool, dict]:
        is_valid, report = await self.analyse(system_events)
        if is_valid and self.__action is not None:
            await self.__action(report)
        return is_valid, report


class TitleProcessor(SystemEventsProcessorBase):
    def __init__(
            self,
            min_length: int,
            max_length: int,
            start_token: Optional[str] = None,
            end_token: Optional[str] = None,
            valid_system_events_action: Callable[[dict], Coroutine] = None
    ):
        super().__init__(start_token, end_token, valid_system_events_action)
        self.min_length = min_length
        self.max_length = max_length

    async def analyse(self, system_events: list[dict]) -> tuple[bool, dict]:
        system_events_full_text = "".join([event['choices'][0]['delta'].get('content', '') for event in system_events])
        system_events_full_text = system_events_full_text.strip(f'."\'{self.start_token}{self.end_token} \n') \
                                                         .removeprefix("Title: ")
        if len(system_events_full_text) > self.max_length:
            return False, {}
        elif len(system_events_full_text) < self.min_length:
            return False, {}
        return True, {"title": system_events_full_text}


class StreamAnalyser:
    def __init__(
            self,
            stream_iterator: AsyncIterator[str],
            system_events_processor: Optional[SystemEventsProcessorBase] = None
    ):
        self.__system_events_processor = system_events_processor
        self.__stream_iterator = stream_iterator
        self.__user_events_raw: list[str] = []
        self.__system_events_raw: list[str] = []
        self.__system_events: list[dict] = []
        self.__save_user_events = True

    @staticmethod
    def __parse_sse(event: str) -> dict:
        sse_json = json.loads(event.strip().removeprefix('data: '))
        return sse_json

    @staticmethod
    def __check_stream_end(sse_json: dict) -> bool:
        return sse_json['choices'][0]['finish_reason'] is not None

    def __check_system_events_start(self, event: dict) -> bool:
        start_token = self.__system_events_processor.start_token
        if start_token:
            return event['choices'][0]['delta'].get('content', '').strip().startswith(start_token)
        return False

    def __check_system_events_end(self, event: dict) -> bool:
        end_token = self.__system_events_processor.end_token
        if end_token:
            return event['choices'][0]['delta'].get('content', '').strip().startswith(end_token)
        return False

    def _process_event(self, event: str) -> dict[str, bool | str]:
        event_info = {
            "is_stream_end": False,
            "is_skipped": False,
        }
        try:
            sse_json = self.__parse_sse(event)
            is_stream_end = self.__check_stream_end(sse_json)
            is_sys_events_start = self.__check_system_events_start(sse_json)
            is_sys_events_end = self.__check_system_events_end(sse_json)
            if is_sys_events_end:
                self.__save_user_events = True
            elif is_sys_events_start:
                self.__save_user_events = False
            if (not self.__save_user_events or is_sys_events_end) and not is_stream_end:
                self.__system_events_raw.append(event)
                self.__system_events.append(sse_json)
                return {"is_stream_end": is_stream_end, "is_skipped": True, "event": event}
            else:
                self.__user_events_raw.append(event)
                return {**event_info, "is_stream_end": is_stream_end, "event": event}
        except JSONDecodeError:
            return {**event_info, "event": event}

    async def __aiter__(self):
        async for event in self.__stream_iterator:
            event_info = self._process_event(event)
            if event_info["is_stream_end"]:
                await self.__system_events_processor.analyse_and_act(self.__system_events)
            if not event_info["is_skipped"]:
                yield event_info["event"]
