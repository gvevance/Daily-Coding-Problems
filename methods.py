# functions that are used by multiple scripts

import imaplib,email

imap_url = "imap.gmail.com"

folder_name = '"daily coding problem"'      # enclose the mailbox inside single quotes and double quotes
pickle_file = 'DCP_object.pkl'
credfile = 'user_pw.txt'


def getUserCredentials():
    ''' Get user credentials from user_pw.txt (local file)'''
    error = False
    try :
        with open(credfile,'r') as cfile :
            username = cfile.readline().strip()
            password = cfile.readline().strip()
            
    except FileNotFoundError:
        print(f"File {credfile} does not exist. Cannot login without username and password.")
        print("Exiting ...")
        error=True

    except :
        print("Unknown error. Aborting ...")
        exit()

    if error :
        exit()

    return username,password


def connect_to_server(imap_url,user,password):
    ''' connecting to server '''
    connection = imaplib.IMAP4_SSL(imap_url)
    try :
        connection.login(user,password)

    except :
        print(f"Could not connect to server with the given credentials. Check code or {credfile}. Exiting now ...")
        exit()
    
    return connection


def search_by_problem_num(imap_Obj,problem_num):
    ''' search for the email which has {problem_num} in its subject '''

    if problem_num > 600 :      
        # TODO : a way to keep track of the last problem number received. Or change this number after a year :P
        print("Error in problem number. Exiting ... ")
        exit()

    print(f"Searching for problem number : {problem_num} ...")
    search_criterion = f'(SUBJECT "Daily Coding Problem: Problem #{str(problem_num)}")'
    _, search_data = imap_Obj.search("utf-8", search_criterion)

    byte_ = search_data[0]
    _,data = imap_Obj.fetch(byte_,'(RFC822)')
    _,b = data[0]
    email_message = email.message_from_bytes(b)
    difficulty_rating = email_message['subject'].split('[')[1][:-2]
    
    spl = "--------------------------------------------------------------------------------"
    # Their mails have this separator

    for part in email_message.walk():
        if part.get_content_type()== "text/plain":
            body = part.get_payload(decode = True)
            text_list = body.decode().split(spl)[0].strip().split('\r\n\r\n')
            company_name = text_list[1].split(" asked by ")[-1][:-1]
            problem_statement = '\r\n\r\n'.join(text_list[2:])
    
    return problem_statement,company_name,difficulty_rating