class CitizenErrorBase(Exception):
    pass

class RegisterCitizenNotAllowedError(CitizenErrorBase):
    pass

class RegisterCitizenError(CitizenErrorBase):
    pass

