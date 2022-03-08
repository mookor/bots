class Duty:
    def __init__(self, name="", phone="", email="", id=0) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.id = id

    def set_attribute(self, name, phone, email, id):
        self.name = name
        self.phone = phone
        self.email = email
        self.id = id
