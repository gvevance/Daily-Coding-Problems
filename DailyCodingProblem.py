# My script to automate Daily Coding Problem

# Steps :
# 1 Connect to email server
# 2 Search for mails with the required subject
# 3 Set up a system where mails are appropriately sorted base on difficulty, company. Implement a search functiionality (dictionary?)
# 4 Push my solution to git with proper formatting (comments, file names, etc)

import imaplib,email,pickle
from os.path import exists

imap_url = "imap.gmail.com"

folder_name = '"daily coding problem"'      # enclose the mailbox inside single quotes and double quotes
pickle_file = 'DCP_object.pkl'
credfile = 'user_pw.txt'


def getUserCredentials():
    try :
        with open(credfile,'r') as cfile :
            username = cfile.readline().strip()
            password = cfile.readline().strip()
            
    except FileNotFoundError:
        print(f"File {credfile} does not exist. Cannot login without username and password.")
        print("Exiting ...")
        exit()

    return username,password


def connect_to_server(imap_url,user,password):
    ''' connecting to server '''
    connection = imaplib.IMAP4_SSL(imap_url)
    connection.login(user,password)
    return connection


def search_by_difficulty(imap_Obj,difficulty='Easy'):
    ''' search for emails with {difficulty} in its subject '''

    if difficulty not in ['Easy','Medium','Hard'] :
        print("Error in difficulty rating keyword. Exiting ... ")
        exit()

    since_date = '01-Jan-2022'
    print(f"\nSearching by difficulty level : {difficulty} ... ")
    print(f"\nPrinting problems since {since_date}\n")

    search_criterion = f'(SUBJECT "[{difficulty}]" SINCE "{since_date}")'        # SINCE to reduce number of 'hits'
    _, search_data = imap_Obj.search("utf-8", search_criterion)

    byte_list = search_data[0].split()
    for byte_ in byte_list :
        _,data = imap_Obj.fetch(byte_,'(RFC822)')
        _,b = data[0]
        email_message = email.message_from_bytes(b)
        print(email_message['subject'])


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
    
    print("Found.")
    return problem_statement,company_name,difficulty_rating


def search_by_company(imap_Obj,company):
    ''' search by company name'''
    
    with open(pickle_file,'rb') as pfile:
        _ = pickle.load(pfile)
        company_list = pickle.load(pfile)
    
    if company not in company_list :
        print("Error in company name. Exiting ... ")
        exit()

    since_date = '15-Nov-2021'

    print(f"\nSearching by company : {company} ... ")
    print(f"\nPrinting problems since {since_date}\n")
    search_criterion = f'(SUBJECT "Daily Coding Problem: Problem #" BODY "This problem was asked by {company}" SINCE "15-Nov-2021")'        # SINCE to reduce number of 'hits'
    _, search_data = imap_Obj.search("utf-8", search_criterion)

    byte_list = search_data[0].split()
    for byte_ in byte_list :
        _,data = imap_Obj.fetch(byte_,'(RFC822)')
        _,b = data[0]
        email_message = email.message_from_bytes(b)
        print(email_message['subject'])


def update_pickle_file(problem_num,comp,company_list,verbose = False):
    ''' update the file to reflect the most recent problem solved'''

    with open(pickle_file,'wb') as pfile :
        pickle.dump(problem_num,pfile)

        if comp not in company_list :
            company_list.append(comp)

        pickle.dump(company_list,pfile)

    print("Updated pickle file with the new problem number and the company detected (if any).")

    if verbose :
        with open(pickle_file,'rb') as pfile :
            problem = pickle.load(pfile)
            comp_list = pickle.load(pfile)

        print(f"\nLast problem solved = #{problem}\n")
        print("Companies encountered : \n")

        for x in comp_list:
            print(x)
        print()


def create_file(prob,comp,diff,problem_num):
    
    newfile = "Problem #"+str(problem_num)+"_"+diff+"_"+comp+".py"
    starter_code = '''
def main():
    pass

if __name__=="__main__":
    main()
    '''
    
    if exists(newfile):
        print(f"Error. {newfile} already exists. Exiting ...")
        exit()

    with open(newfile,'a') as file :
        file.write("'''\n\n")
        file.write(f"Problem number - {problem_num}\n")
        file.write(f"Difficulty rating - {diff}\n")
        file.write(f"Company - {comp}\n\n")
        file.write(prob)
        file.write("\n\n'''\n")
        file.write(starter_code)
    
    print(f"New file created - \"{newfile}\"\n")


def main():

    # step 1 - connect to server and login
    username,password = getUserCredentials()
    imap_Obj = connect_to_server(imap_url,username,password)    # IMAP4 object
    imap_Obj.select(mailbox=folder_name, readonly=True)

    if exists(pickle_file) :
        with open(pickle_file,'rb') as pfile :
            problem_num = pickle.load(pfile)
            company_list = pickle.load(pfile)
        
        # problem_num is the previously solved problem
        # company_list is the list of companies encountered
 
    else :
        # have to create new pickle file
        problem_num = 0     # previously solved problem num is 0 [nothing solved yet]
        company_list = []
    
    if problem_num == 0:
        print(f"\nAccording to the records, you have not solved any problem.")
    else :
        print(f"\nAccording to the records, you have solved till problem no. {problem_num}.")
       
    prob,comp,diff = search_by_problem_num(imap_Obj,problem_num+1)
    update_pickle_file(problem_num+1,comp,company_list,verbose=False)
    create_file(prob,comp,diff,problem_num+1)
    
    # logout and close connection
    imap_Obj.close()        # close the selected mailbox
    imap_Obj.logout()       # logout of server


if __name__ == "__main__":
    main()
