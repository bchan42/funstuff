import pandas as pd
import usaddress # package handles splitting addresses

fake_prf = pd.read_csv('fake_prf_reponses.csv')
fake_prf.columns = fake_prf.columns.str.strip().str.replace(r'[\r\n]+', ' ', regex=True) # handle funky row extraction

# split name
def split_name(name):
    name_parts = name.split(' ', 1)
    first_name, last_name = name_parts[0], name_parts[1]
    return first_name, last_name

# parse address into street, city, state, zip 
def parse_address(address):
    parsed_address, address_type = usaddress.tag(address)

    # handles case where multiple words for city name
    street = parsed_address.get('AddressNumber', '') + ' ' + parsed_address.get('StreetName', '')
    apartment = parsed_address.get('OccupancyIdentifier', '')
    city = parsed_address.get('PlaceName', '')
    state = parsed_address.get('StateName', '')
    zip_code = parsed_address.get('ZipCode', '')

    return street.strip(), apartment.strip(), city.strip(), state.strip(), zip_code.strip()



for index, row in fake_prf.iterrows():

    # event stuff
    event_name = row['What event was the purchase for? (Not what the purchase was)']
    description = row['Description of Purchase']
    requested_amt = row['Requested Amount']

    # name
    first_name, last_name = split_name(row['First and Last Name']) # need to split

    # address
    street, apartment, city, state, zip_code = parse_address(row['Address (Street, Apt, City, State, Zip)']) # split with some geo package?
    street = street or ''
    apartment = apartment or ''
    city = city or ''
    state = state or ''
    zip_code = zip_code or '' # handles missing vals
    full_street = f"{street} {apartment}".strip() # combine street and apartment
    
    # contact info
    email = row['Cal Poly Email address']
    phone = row["Phone Number (you don't have to include the dashes)"]

    # payment / reciept
    payment_type = row['Payment Type'] # selection
    receive_payment = row["Receiving Payment If you're not enrolled in direct deposit and would like to do so, fill out this form (this is optional)"]
    receipt_url = row["Combine all your receipts or invoices into one pdf and upload here (make sure receipts are itemized) *NOTE: If the last 4 digits of the card used is not visible, please attach a bank/credit card statement with the transaction for proof of payment"]


    print(f"Event: {event_name}, Description: {description}, Requested Amount: {requested_amt}")
    print(f"Name: {first_name} {last_name}")
    print(f"Address: {street}, {apartment}, {city}, {state}, {zip_code}")
    print(f"Email: {email}, Phone: {phone}")
    print(f"Payment Type: {payment_type}, Receive Payment: {receive_payment}")
    print(f"Receipt URL: {receipt_url}")