import re
def extract_sensitive_infomation(text,url):


    def extract_phone(text):
        phone_number = re.findall(r'(?<!\d)(1[3456789]\d{9})(?!\d|\d)', text)
        return phone_number


    def extract_email(text):
        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return email
    
    def extract_idcard(text):
        idcard = re.findall(r'\b\d{17}[\dXx]\b', text)
        return idcard

    def extract_credentials(text):
        match = re.search(r"username ?: ?(\w+)\b.+password ?: ?(\w+)\b", text,re.I)
        if match:
            return [match.group(1),match.group(2)]
        return []
    


    sensitive_information=dict()
    phone=extract_phone(text)
    email=extract_email(text)
    credentials=extract_credentials(text)
    idcard=extract_idcard(text)
    quantity=len(phone)+len(email)+len(credentials)+len(idcard)

    sensitive_information["phone"]=phone
    sensitive_information["email"]=email
    sensitive_information["idcard"]=idcard
    sensitive_information["credentials"]=credentials
    sensitive_information["quantity"]=quantity

    return sensitive_information