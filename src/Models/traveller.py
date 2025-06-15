class Traveller:
    def __init__(
        self, id, first_name, last_name, birthday, gender, street, house_number,
        zip_code, city, email, phone, driving_license, registration_date
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.street = street
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        self.email = email
        self.phone = phone
        self.driving_license = driving_license
        self.registration_date = registration_date

    def __repr__(self):
        return f"<Traveller {self.id}: {self.first_name} {self.last_name}>"
