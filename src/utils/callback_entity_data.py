from aiogram.filters.callback_data import CallbackData


class CallbackEntityData(CallbackData, prefix='callback_entity_data'):
    action: str
    entity_id: int
