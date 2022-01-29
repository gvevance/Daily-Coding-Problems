''' To reset pickle to the state we want (problem number) in case of any mismatch.
Populate the company list too if required.
'''
from methods import *
import pickle

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