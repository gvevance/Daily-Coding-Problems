# My script to automate Daily Coding Problem

# Steps :
# 1 Connect to email server
# 2 Search for mails with the required subject
# 3 Set up a system where mails are appropriately sorted base on difficulty, company. Implement a search functiionality (dictionary?)
# 4 Push my solution to git with proper formatting (comments, file names, etc)

from methods import *
from os.path import exists
import pickle

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
