def verifyEmail(email):
    
    #Divide the e-mail into two indexes to verify if e-mail is from Etec
    email = email.split('@')
    
    #Get the first index to verify if the e-mail is from Etec
    domain = email[1].split('.')
    
    if domain[0] == "etec":
        return True
    else:
        return False
