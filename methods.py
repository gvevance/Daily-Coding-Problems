# functions that are used by multiple scripts

import imaplib,email,pickle
from os.path import exists


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

    if problem_num > 850 :      
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
    # split at '[' , choose the 2nd piece , omit last 2 characters (fullstop and another character)
    
    spl = "--------------------------------------------------------------------------------"
    # Their mails have this separator

    for part in email_message.walk():
        if part.get_content_type()== "text/plain":
            body = part.get_payload(decode = True)
            text_list = body.decode().split(spl)[0].strip().split('\r\n\r\n')
            # split at ---- separator, remove whitespaces, split at '\r\n\r\n'
            company_name = text_list[1].split(" asked by ")[-1][:-1]
            # choose 2nd line, split at "asked by" (common in all mails), take last piece and remove last fullstop.
            problem_statement = '\r\n\r\n'.join(text_list[2:])
            # join the remaining piece back because they all form the problem statement
    
    return problem_statement,company_name,difficulty_rating


def update_pickle_file(problem_num,comp,company_dict,verbose = False):
    ''' update the file to reflect the most recent problem solved'''

    with open(pickle_file,'wb') as pfile :
        pickle.dump(problem_num,pfile)

        if comp not in company_dict :
            company_dict[comp] = [problem_num]

        else :
            company_dict[comp].append(problem_num)

        pickle.dump(company_dict,pfile)

    print("Updated pickle file with the new problem number and the company detected (if any).")

    if verbose :
        with open(pickle_file,'rb') as pfile :
            problem = pickle.load(pfile)
            comp_dict = pickle.load(pfile)

        print(f"\nLast problem solved = #{problem}\n")
        print("Companies encountered : \n")

        for x in comp_dict:
            print(x,end=' - ')
            print(f"{len(comp_dict.get(x))} problem(s).")
        print()


def create_file(prob,comp,diff,problem_num):
    
    newfile = "Problem #"+str(problem_num)+" "+diff+" "+comp+".py"
    starter_code = '''
def main():
    pass

if __name__ == "__main__" :
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
