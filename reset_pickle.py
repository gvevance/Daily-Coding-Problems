''' To reset pickle to the state we want (problem number) in case of any mismatch.
Populate the company list too if required.
'''

import pickle

pickle_file = "DCP_object.pkl"

def main():
    try :
        with open(pickle_file,'rb') as pfile :
            problem = pickle.load(pfile)
            comp_list = pickle.load(pfile)
        
        print(f"Records show that you have solved {problem} problems.")
        print("Companies stored till now :\n")

        for item in comp_list :
            print(item)

    except FileNotFoundError :
        print(f"{pickle_file} not found. Exiting ...")
        exit()

    except :
        print(f"Error. Check code and {pickle_file}. Exiting ...")
        exit()






if __name__ == "__main__" :
    main()