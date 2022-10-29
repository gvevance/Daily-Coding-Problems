# My script to automate Daily Coding Problem

# Steps :
# 1 Connect to email server
# 2 Search for mails with the required subject
#TODO 3 Set up a system where mails are appropriately sorted base on difficulty, company. Implement a search functiionality (dictionary?)
# 4 Push my solution to git with proper formatting (comments, file names, etc)


import pickle
from os.path import exists

from methods import getUserCredentials
from methods import connect_to_server
from methods import search_by_problem_num
from methods import update_pickle_file
from methods import create_file

pickle_file = 'DCP_object.pkl'
imap_url = "imap.gmail.com"
folder_name = '"daily coding problem"'      # enclose the mailbox inside single quotes and double quotes


def main():

    # step 1 - connect to server and login
    username,password = getUserCredentials()
    imap_Obj = connect_to_server(imap_url,username,password)    # IMAP4 object
    imap_Obj.select(mailbox=folder_name, readonly=True)

    if exists(pickle_file) :
        with open(pickle_file,'rb') as pfile :
            problem_num = pickle.load(pfile)
            company_dict = pickle.load(pfile)
        
        # problem_num is the previously solved problem
        # company_list is the list of companies encountered
 
    else :
        # have to create new pickle file
        problem_num = 0     # previously solved problem num is 0 [nothing solved yet]
        company_dict = {}
    
    if problem_num == 0:
        print(f"\nAccording to the records, you have not solved any problem.")
    else :
        print(f"\nAccording to the records, you have solved till problem no. {problem_num}.")
       
    try :
        prob_statement,company,difficulty = search_by_problem_num(imap_Obj,problem_num+1)
        print("Found.")
    except :
        print("Error occured in mail search. Aborting ... ")
        exit()
    
    update_pickle_file(problem_num+1,company,company_dict,verbose=False)
    create_file(prob_statement,company,difficulty,problem_num+1)
    
    # logout and close connection
    imap_Obj.close()        # close the selected mailbox
    imap_Obj.logout()       # logout of server


if __name__ == "__main__":
    main()
