# setup key folders and jsons
import os
import json
import pandas as pd


def create_folder(folder_name):
    path = os.path.join(os.getcwd(), folder_name)
    if not os.path.isdir(path):
        os.mkdir(path)


def add_json_file(dict_to_save, folder, file_name):
    path = os.path.join(os.getcwd(), folder, file_name)
    with open(path, "w") as f:
        json.dump(dict_to_save, f, indent=2)


# create folders for temp files and spam
create_folder("spam_defender_files")
create_folder("temp_files")
create_folder("downloaded_tasks")

# add jsons
credentials = {
    "telegram_token": "",
    "EMAIL_ADDRESS": "",
    "EMAIL_PASSWORD": "",  # from google → manage account → security → activate 2-step verif → then app password and generate
    "EMAIL_FROM": "",
    "spreadsheet_id": "",
    "sheet_name": "",
    "company_name": "",
    "developer_tag_name": "",
    "developer_chat_id": "",
    "teams": {
        "team_name": "google_folder_id"  # where all candidate are stored for this team; team_name should be equal to the one, coming from spreadsheet
    },
}

google_service_credentials = {
    "type": "",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_x509_cert_url": "",
}

add_json_file(credentials, "configs", "creds_and_tokens.json")
add_json_file(google_service_credentials, "configs", "google_service_credentials.json")
add_json_file([], "spam_defender_files", "banned_list.json")
add_json_file([], "spam_defender_files", "already_processed_users.json")
add_json_file({}, "spam_defender_files", "spam_counter.json")

# add template excel task
pd.DataFrame([{"id": "1", "label": "1"}]).to_excel(
    os.path.join(os.getcwd(), "downloaded_tasks", "Excel_task.xlsx"), index=False
)

print(
    "---Done!---\nFollow the instructions in README.md to fill ./configs/creds_and_tokens.json and you are good to go!"
)
print("Press enter to exit")
x = input()
