from dataclasses import dataclass


@dataclass
class Button:
    text: str
    callback_data: object = None
