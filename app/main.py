from pyconnectwise import ConnectWiseManageAPIClient
import os
from dotenv import load_dotenv
import datetime

# ------- authentication  -------  #
env_path = "/root/per-diem/app/.env"
load_dotenv(env_path)
company_id = os.getenv("company_id")
manage_url = os.getenv("manage_url")
client_id = os.getenv("client_id")
public_key = os.getenv("public_key")
private_key = os.getenv("private_key")
manage_api_client = ConnectWiseManageAPIClient(company_id, manage_url, client_id, public_key, private_key)

# ------- global variables  -------  # customize it as needed
employee_names = ["aaa", "bbb", "ccc"]
last_days = 60 # days to look back in time. Change this as you want
hours_limit = 2 # hours limit for traveling time. Change this as you want. Set 2 hours as default

current_date = datetime.datetime.now()
past_date = datetime.datetime.now() - datetime.timedelta(days=last_days)

text_body = f"""
**__Per-Diem Submission Reminder__**\n
**What is this?**\nBased on recent time entries, you may need to submit a per-diem for this ticket.\n
**Already submitted per-diem?**\nIf you have already submitted your per-diem, no further action is required. \nThis email is automatically sent to employees with travel time entries exceeding {hours_limit} hours last {last_days} days.\n
**Have questions?**\nPlease contact __[me](mailto:xxx@xxx.ca)__ for any inquiries.\n
*__This is an automated email. Please do not reply.__*\n
"""

# ------- Getting local time (7h behind) to pass -------  #
def get_localtime(current_datetime):
  """
  convert current time to local time (7h behind) to pass when getting tickets
  :param current_datetime:
  :return: local time (7h behind)
  """
  # Get current time as a datetime object
  now =  current_datetime

  # Subtract 7 hours to get local time
  local_time_now_7h_behind = now + datetime.timedelta(hours=7)

  # Format the local time in the same way
  local_date = local_time_now_7h_behind.strftime("%Y-%m-%d")
  local_time = local_time_now_7h_behind.strftime("%H:%M:%S")
  return f"[{local_date}T{local_time}Z]"

# ------- pulling tickets ID   -------  #
def get_ticket_ids(employee_name, localtime_from, localtime_to):
  """
  Get ticket IDs that have time entries exceeding certain hours by a specific employee.

  :param employee_name:
  :param localtime_from:
  :param localtime_to:
  :return: List of ticket IDs
  """
  time_entries = manage_api_client.time.entries.get(params={
          'conditions': f'member/identifier = "{employee_name}" '
                        f'and timeStart > {localtime_from} and timeStart < {localtime_to} '
                        f'and workType/name = "Travel"'
                        f'and actualHours > {hours_limit}',
          'pageSize': 100, # it returns 100 records
      })

  tickets = [entry.ticket.id for entry in time_entries]
  print(f"For {employee_name}, the following tickets have travel time entries exceeding 2 hours during last {last_days} days:\n{list(dict.fromkeys(tickets))}")
  print("====================================")
  return list(dict.fromkeys(tickets))

# ------- getting tech's email address by identifier   -------  #
def get_tech_email(employee_name):
    """
    Get the email address of the employee
    
    :param employee_name:
    :return: email address
    """
    tech_info = manage_api_client.system.info.members.get(params={
        'conditions': f'identifier = "{employee_name}"',
    })
    email = tech_info[0].default_email
    return email

# ------- sending email  -------  #
def send_email(tickets_id, tech_email):
  """
  Send email to the assigned employee with internal notes.

  :param tickets_id:
  :param tech_email:
  """
  if tickets_id == []:
    print(f"This tech does not have the ticket that has travel time entries during last {last_days} days")
    print("====================================")
  else:
    for ticket in tickets_id:
      # 0 getting the current cc email address
      current_cc_email = manage_api_client.service.tickets.id(ticket).get().automatic_email_cc

      # 1 changing the email flag to send email to the assigned employee
      data_for_patch1 = [
        # email flags to send email by adding notes
        {
          "op": "replace",
          "path": "automaticEmailContactFlag",
          "value": "false"
        },
        {
          "op": "replace",
          "path": "automaticEmailResourceFlag",
          "value": "false"
        },
        {
          "op": "replace",
          "path": "automaticEmailCc",
          "value": f"{tech_email}" # temporally replacing the cc email address to email the tech by adding note
        },
        {
          "op": "replace",
          "path": "automaticEmailCcFlag",
          "value": "true" # this needs to be on to send email
         },

      ]
      manage_api_client.service.tickets.id(ticket).patch(data=data_for_patch1)
      print(f"Changed CC list for #{ticket} to send an email")

      # 2 sending email to the assigned employee by adding internal notes
      data_passed_note = {
        "text": text_body,
        "detailDescriptionFlag": True, # if this is true, it goes to discussion. and needs to be true to send email to cc
        "internalAnalysisFlag": True, # if this is true, it goes to internal notes.
        "processNotifications": True, # if this is false, it does not send email even if the flags are true. needs to be on
      }
      manage_api_client.service.tickets.id(ticket).notes.post(data=data_passed_note)
      print(f"Email sent for #{ticket}, the email address is {tech_email}")

      # 3 changing back the cc email address
      data_for_patch2 = [
        {
          "op": "replace",
          "path": "automaticEmailCc",
          "value": f"{current_cc_email}"
        },
        {
          "op": "replace",
          "path": "automaticEmailCcFlag",
          "value": "false"
        },
      ]
      manage_api_client.service.tickets.id(ticket).patch(data=data_for_patch2)
      print(f"CC email address changed back for #{ticket} and now the email address is {current_cc_email}")

      # 4 getting note ID just created
      notes = manage_api_client.service.tickets.id(ticket).notes.get()
      latest_note_id = notes[len(notes)-1].id # getting the latest note = just the one created to send an email

      # 5 changing the note to internal notes
      data_for_patch3 = {
          "op": "replace",
          "path": "detailDescriptionFlag",
          "value": "false"
        },
      manage_api_client.service.tickets.id(ticket).notes.id(latest_note_id).patch(data=data_for_patch3)
      print(f"changed the note to internal for #{ticket}")
      print("====================================")



if __name__ == "__main__":
  for employee_name in employee_names:
    tickets_list = get_ticket_ids(employee_name, get_localtime(past_date), get_localtime(current_date))
    send_email(tickets_list, get_tech_email(employee_name))