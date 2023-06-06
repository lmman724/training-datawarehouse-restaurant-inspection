import csv
import random
from datetime import datetime, timedelta

# Define the headers for the CSV file
headers = ['Ref#', 'requestedDate', 'requestor', 'location', 'department', 'reasonCode', 'Endorser', 'Approver', 'Status', 'Stage']

# Define the possible values for some of the columns
locations = ['New York', 'Chicago', 'Los Angeles', 'San Francisco', 'Seattle', 'Miami']
departments = ['Sales', 'Marketing', 'Engineering']
reason_codes = ['RC-001', 'RC-002', 'RC-003']
endorsers = ['Jane Smith', 'Robert Lee', 'David Kim', 'Samantha Davis', 'Bob Johnson', 'George Brown', 'Susan Wong', 'John Doe']
approvers = ['Jane Smith', 'Robert Lee', 'David Kim', 'Samantha Davis', 'Bob Johnson', 'George Brown', 'Susan Wong', 'John Doe']
statuses = ['Pending', 'Approved', 'Rejected']
stages = ["closed", "Manager Decision", "Booking"]

# Generate the data for the CSV file
data = []
for i in range(1000):
    ref = str(i+1).zfill(3)
    requested_date = datetime.now() - timedelta(days=random.randint(0, 30))
    requested_date = requested_date.strftime('%Y-%m-%d')
    requestor = 'Requestor ' + str(i+1)
    location = random.choice(locations)
    department = random.choice(departments)
    reason_code = random.choice(reason_codes)
    endorser = random.choice(endorsers)
    approver = random.choice(approvers)
    status = random.choice(statuses)
    stage = random.choice(stages)
    row = [ref, requested_date, requestor, location, department, reason_code, endorser, approver, status, stage]
    data.append(row)

# Write the data to a CSV file
with open('travel_requests.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)
