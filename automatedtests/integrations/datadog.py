import time
from typing import Sequence
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.event_create_request import EventCreateRequest
from datadog_api_client.exceptions import ApiException


def send_event_to_datadog(title: str, text: str, extra_tags: Sequence[str] | None = None) -> None:
    """
       Sends an event to Datadog. Tag `run_id:<unix_ts>` is always added
       to group events from the same test run.

           title: Event title.
           text: Event description.
           extra_tags: Additional tags (e.g. ["env:stage", "suite:smoke"]).
               Accepts list/tuple or any string sequence. If None — only base tags are sent.
       Raises:
           ConnectionError: Raised if the SDK returns an error sending the event.
       """
    cfg = Configuration()
    uniq = str(int(time.time()))
    tags = [f'run_id:{uniq}']

    if extra_tags:
        tags.extend((list(extra_tags)))

    try:
        with ApiClient(cfg) as client:
            EventsApi(client).create_event(
                body=EventCreateRequest(title=title, text=text, tags=tags)
            )
    except ApiException as exc:
       raise ConnectionError(f'Error sending event to Datadog {exc}')

