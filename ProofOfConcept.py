import pandas as pd
import pickle

def main():
    with open("discovered_techniques.txt", 'r') as opened_file:
        col = opened_file.read()
    with open("Exisiting_Techniques.txt", 'r') as exist_tech:
        ex_tech = exist_tech.read()
    col = col.split("\n")
    ex_tech = ex_tech.split("\n")
    x = pd.DataFrame(columns=ex_tech)
    new_dict = {}
    for name in col:
        if name in x.columns:
            new_dict[name] = 1
    x = x.append(new_dict, ignore_index = True)
    x.fillna(0, inplace=True)
    loaded_model = pickle.load(open("APT_tech.sav", 'rb'))
    res = loaded_model.predict(x)
    print("Predicted Group: " + res[0])
    print("Visit https://attack.mitre.org/groups/ for group references.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()