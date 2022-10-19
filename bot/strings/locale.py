from bot.filters.command_filters import command_cancel


registration_menu_TEXT = "To start using the service, you need to register 😉"
registration_menu_message_IK_TEXT = "🆗"

restart_command_TEXT = " 👉 👈 The current state is reset"
restart_command_TEXT_error = "An error has occurred. " + restart_command_TEXT

main_menu_TEXT = "Main menu"
main_menu_message_IK_BTN_account_TEXT = "👤"

help_EMOJI = "📝"
help_TEXT = "Help text"

user_registration_TEXT = "Enter Your First and Last Name (Example: John Doe)"
user_state_finish_TEXT = "💾Your data is saved"
user_state_incorrect_input_TEXT = "❗Incorrect input format"
user_state_incorrect_input_TEXT_delimeter_error = user_state_incorrect_input_TEXT + " There is no space between words"

admin_panel_TEXT = "👨‍💼Admin panel"
admin_panel_BTN_items_mgmt_TEXT = "Managing elements"
admin_panel_BTN_server_stats_TEXT = "💻 Server Status"

manager_panel_TEXT = "👨Manager panel"
manager_panel_BTN_items_mgmt_TEXT = "User Management"

items_mgmt_message_IK_TEXT = "Here you can edit the list of *items*"
items_mgmt_message_IK_TEXT_error = "The list of items is missing in the database"
items_mgmt_ACTION_TEXT_cancel = f"Cancel the action /{command_cancel.commands[0]}"

items_mgmt_action_ADD_TEXT_pre = "ADD ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_UPDATE_TEXT_pre = "UPDATE ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_DELETE_TEXT_pre = "DELETE ITEM." + items_mgmt_ACTION_TEXT_cancel

items_mgmt_action_ADD_TEXT_past = "ITEM ADDED."
items_mgmt_action_UPDATE_TEXT_past = "ITEM UPDATED."
items_mgmt_action_DELETE_TEXT_past = "ITEM DELETED."


def account_menu_message_IK_TEXT(user):
    return f"""Your account

*id*: {user['user_id']}
*name*: {user['first_name']} {user['last_name']}"""


navigation_menu_TEXT = "Navigation"
navigation_BTN_back = "👈"
navigation_BTN_back_to_menu = "👈 menu"

throttling_too_many_requsets_TEXT = f"Too many requests!"
throttling_unlocked_TEXT = "The command is unblocked"

# ----------------------------------------------------------------------------------------

common_commands = \
    [
        {"command": "start", "description": "starting the bot"},
        {"command": "help", "description": "tech support"},
        {"command": "reload", "description": "restarting the bot and reset state"},
    ]
admin_commands = \
    [
        {"command": "admin", "description": "admin panel"},
        {"command": "logs", "description": "event log"},
        {"command": "cancel", "description": "when something went wrong"}
    ]
manager_commands = \
    [
        {"command": "manager", "description": "manager panel"},
        {"command": "cancel", "description": "when something went wrong"}
    ]
