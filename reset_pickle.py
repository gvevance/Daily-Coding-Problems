''' To reset pickle to the state we want (problem number) in case of any mismatch.
Populate the company list too if required.
'''

import imaplib,email,pickle

imap_url = "imap.gmail.com"

folder_name = '"daily coding problem"'      # enclose the mailbox inside single quotes and double quotes
pickle_file = 'DCP_object.pkl'
credfile = 'user_pw.txt'


def getUserCredentials():
    ''' Get credentials from the user_pw.txt file'''
    try :
        with open(credfile,'r') as cfile :
            username = cfile.readline().strip()
            password = cfile.readline().strip()
            
    except FileNotFoundError:
        print(f"File {credfile} does not exist. Cannot login without username and password.")
        print("Exiting ...")
        exit()

    except :
        print("Unknown error. Aborting ...")
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
    ''' search for the email which has "problem_num" in its subject '''

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


def populate_companies_getDict(problem_num):
    
    username,password = getUserCredentials()
    imap_Obj = connect_to_server(imap_url,username,password)    # IMAP4 object
    imap_Obj.select(mailbox=folder_name, readonly=True)

    company_dict = {}
    for i in range(1,problem_num+1):
        _,company_name,__ = search_by_problem_num(imap_Obj,i)
        print("Found.")
        if company_name not in company_dict :
            company_dict[company_name] = [i]
        
        else :
            company_dict[company_name].append(i)

    return company_dict


def main():
    try :
        with open(pickle_file,'rb') as pfile :
            problem = pickle.load(pfile)
            comp_list = pickle.load(pfile)
        
        print(f"Records show that you have solved {problem} problem(s).")
        print("Companies stored till now :")

        for item in comp_list :
            print(item)
        print()     # print new line

        reset = input("Do you want to reset it to another state ? (yes/no) : ")

        if reset == "yes" :

            new_problem = int(input(f"Enter problem number to update {pickle_file} with : "))
            with open(pickle_file,'wb') as pfile :
                pickle.dump(new_problem,pfile)
                pickle.dump(populate_companies_getDict(new_problem),pfile)
        
        elif reset == "no" :
            print("Okay. Exiting ... ")

        else :
            print("Error in entered choice. Please enter \"yes\" or \"no\" next time. Exiting ... ")

             
    except FileNotFoundError :

        reset = input(f"{pickle_file} not found. Do you want to generate it to some state ? (yes/no) : ")
        new_problem = int(input(f"Enter problem number to update {pickle_file} with : "))

        if reset == "yes" :
            with open(pickle_file,'wb') as pfile :
                pickle.dump(new_problem,pfile)
                pickle.dump(populate_companies_getDict(new_problem),pfile)

        elif reset == "no" :
            print("Okay. Exiting ... ")

        else :
            print("Error in entered choice. Please enter \"yes\" or \"no\" next time. Exiting ... ")


    except :
        print(f"Error. Check code and {pickle_file}. Exiting ...")


if __name__ == "__main__" :
    main()