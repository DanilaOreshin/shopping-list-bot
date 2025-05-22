from src.config.bot_settings import settings

# texts
hi_text = f'Привет!\n' \
          f'Введи /start для начала работы.'

not_registered_text = f'Ты - незарегистрированный пользователь!!!\n' \
                      f'\n' \
                      f'Введи /start для запуска процесса регистрации.'

welcome_text = f'Добро пожаловать!'

about_text = f'О боте:\n' \
             f'\n' \
             f'Версия: {settings.BOT_VERSION}\n' \
             f'Автор: {settings.BOT_DEVELOPER}\n' \
             f'\n' \
             f'Описание: Бот для создания и управления списками покупок.'

start_registration_text = f'Вы не зарегистрированы!\n' \
                          f'Для начала работы нужно пройти регистрацию 👇'

default_text = f'Действие не выбрано!\n' \
               f'Нажми на доступные кнопки и отправь /start'

cancel_action_text = f'Действие отменено!'

send_pass_text = f'Пришли пароль'

success_user_create_text = f'Пользователь успешно зарегистрирован!'

wrong_pass_text = f'Неверный пароль!\n' \
                  f'\n' \
                  f'Пришли новый пароль или отмени регистрацию 👇'

send_list_name_text = f'Пришли название нового списка'

success_list_create_text = 'Список "{}" успешно создан! 👍'

list_exists_text = f'Список с таким названием уже существует!\n' \
                   f'\n' \
                   f'Пришли другое название или отмени действие 👇'

send_list_new_name_text = f'Пришли новое название списка'

success_list_update_text = f'Список успешно обновлен! 👍'

assign_list_confirm_text = f'Внимание!\n' \
                           f'Списком невозможно будет управлять после его назначения!\n' \
                           f'Советую сделать все изменения до того, как назначать список.\n' \
                           f'\n' \
                           f'Вы уверены, что хотите назначить его сейчас?'

send_contact_text = f'Пришли контакт пользователя, на которого хочешь назначить список,\n' \
                    f'или отмени действие 👇'

wrong_contact_text = f'Этот пользователь не зарегистрирован!\n' \
                     f'\n' \
                     f'Пришли другой контакт или отмени действие 👇'

list_assigned_successfully_text = 'Список успешно назначен! 👍'

delete_list_confirm_text = f'Внимание!\n' \
                           f'Все товары в листе и сам лист будут удалены!\n' \
                           f'\n' \
                           f'Вы уверены?'

success_list_delete_text = f'Список успешно удален! 👍'

list_is_empty_text = f'Список пуст 🙁'

show_list_items_prefix_text = f'Товары:'

check_icon = '✅'

uncheck_icon = '⬜️'

check_item_text = check_icon + f'Отметить'

uncheck_item_text = uncheck_icon + f'Отметить'

send_items_text = 'Пришли список товаров в формате:\n' \
                  '{имя товара} - {кал-во товара (число)}\n' \
                  '{имя товара}\n' \
                  '\n' \
                  'Пример:\n' \
                  'Молоко - 1\n' \
                  'Хлеб\n' \
                  'Куриная грудка - 5'

success_item_delete_text = f'Товар успешно удален! 👍'

cant_parse_items_data_text = f'Не удалось распарсить данные!\n' \
                             f'\n' \
                             f'Пришли новый список или отмени действие 👇'

no_one_item_insert_text = f'Ни один товар не был добавлен 🙁'

partly_item_insert_text = f'Часть товаров добавлена!\n' \
                          f'\n' \
                          f'Товары, которые не были добавлены:\n'

all_item_insert_text = f'Все товары успешно добавлены! 👍'

list_preview_text = 'Список "{0}"\n' \
                    '\n' \
                    'Количество товаров - {1}\n\n'

no_lists_text = f'У тебя еще нет списков 🙁'

my_lists_text = f'Мои списки:'

add_items_button_text = '⬇️Добавить товары'
update_button_text = '✏️Обновить'
delete_button_text = '🗑Удалить'
watch_items_button_text = '📜Раскрыть'
assign_list_button_text = '🤝Назначить'
preview_list_button_text = '📋Показать список'
cancel_button_text = '❌Отменить'
yes_button_text = '👍Да'
