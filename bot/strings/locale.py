from bot.filters.commands import command_cancel


registration_menu_TEXT = "To start using the service, you need to register ๐"
registration_menu_message_IK_TEXT = "๐"

restart_command_TEXT = " ๐ ๐ The current state is reset"
restart_command_TEXT_error = "An error has occurred. " + restart_command_TEXT

main_menu_TEXT = "Main menu"
main_menu_message_IK_BTN_account_TEXT = "๐ค"

help_EMOJI = "๐"
help_TEXT = "Help text"

user_registration_TEXT = "Enter Your First and Last Name (Example: John Doe)"
user_state_finish_TEXT = "๐พYour data is saved"
user_state_incorrect_input_TEXT = "โIncorrect input format"
user_state_incorrect_input_TEXT_delimeter_error = user_state_incorrect_input_TEXT + " There is no space between words"

admin_panel_TEXT = "๐จโ๐ผAdmin panel"
admin_panel_BTN_items_mgmt_TEXT = "Managing elements"
admin_panel_BTN_server_stats_TEXT = "๐ป Server Status"

manager_panel_TEXT = "๐จManager panel"
manager_panel_BTN_items_mgmt_TEXT = "User Management"

items_mgmt_message_IK_TEXT = "Here you can edit the list of *items*"
items_mgmt_message_IK_TEXT_error = "The list of items is missing in the database"
items_mgmt_ACTION_TEXT_cancel = f"Cancel the action /{command_cancel.commands[0]}"

items_mgmt_action_ADD_TEXT_pre = "ADD ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_UPDATE_TEXT_pre = "UPDATE ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_DELETE_TEXT_pre = "DELETE ITEM." + items_mgmt_ACTION_TEXT_cancel


def account_menu_message_IK_TEXT(user):
    return f"""Your account

*id*: {user['user_id']}
*name*: {user['first_name']} {user['last_name']}"""


navigation_menu_TEXT = "Navigation"
navigation_BTN_back = "๐"
navigation_BTN_back_to_menu = "๐ menu"

throttling_too_many_requsets_TEXT = f"Too many requests!"
throttling_unlocked_TEXT = "The command is unblocked"
