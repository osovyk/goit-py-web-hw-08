import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/contacts"

def pretty_print(resp):
    print("Status:", resp.status_code)
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)
    print("-" * 50)

# 1. Create a new contact
new_contact = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "phone": "+380501112233",
    "birthday": "1815-12-10",
    "additional_info": "First programmer"
}
print("CREATE CONTACT")
resp = requests.post(BASE_URL + "/", json=new_contact)
pretty_print(resp)
contact_id = resp.json().get("id")

# 2. List all contacts
print("LIST CONTACTS")
resp = requests.get(BASE_URL + "/")
pretty_print(resp)

# 3. Get one contact by id
print("GET ONE CONTACT")
resp = requests.get(f"{BASE_URL}/{contact_id}")
pretty_print(resp)

# 4. Update contact
print("UPDATE CONTACT")
update_data = {"phone": "+380501112244"}
resp = requests.put(f"{BASE_URL}/{contact_id}", json=update_data)
pretty_print(resp)

# 5. Search contacts by name
print("SEARCH CONTACTS (first_name=Ada)")
resp = requests.get(BASE_URL + "/", params={"first_name": "Ada"})
pretty_print(resp)

# 6. Get upcoming birthdays
print("UPCOMING BIRTHDAYS")
resp = requests.get(BASE_URL + "/birthdays/upcoming")
pretty_print(resp)

# 7. Delete contact
print("DELETE CONTACT")
resp = requests.delete(f"{BASE_URL}/{contact_id}")
print("Status:", resp.status_code)
print("-" * 50)

# 8. List again to confirm deletion
print("LIST CONTACTS AFTER DELETE")
resp = requests.get(BASE_URL + "/")
pretty_print(resp)
