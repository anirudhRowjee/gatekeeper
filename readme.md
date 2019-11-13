# Gatekeeper

## Simple protocol to manage ticketing for events.

## Functionalities
1. Create and Issue guest passes by means of barcode
2. See if a pass has been scanned already
3. Issue Guest Passes


## Tech Stack
* Django normal with REST-Type requests and response handling


## Models


1. Student
    - name
    - Admission Number (unique)

2. Dates
    - event
    - date

3. Barcodes
    - unique ID 
    - Image

4. GuestPass
    - barcode (fkey barcodes)
    - datevalid (fkey dates)
    - Name of Issuee
    - email of Issuee
    - Dateissued
    - paid (bool)
    - Guest of (fkey student)
    
## Workflow

1. Guest pass registration

    - enter Number of student who they are guest of (student Name/ Admission Number)
    - Enter name and email of guest
    - generate barcode
    - Collect Payment
    - Mail to email ID

2. Annual Day entry

    - scan barcode
    - check if valid per date and checkout status
    - if yes, allow entry
    - if no, don't allow entry
    
    - checkout - scan barcode on checkout
    - alter checkout status
    - checkin - scan barcode to see if checked out
    - if all OK let them in


