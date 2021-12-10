from MITRE import APT_Info
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import pickle

def create_dataframe_obj(df_techniques, names, dataframe=None):
    list_of_tech = df_techniques.values.tolist()
    tech_list = [ item for elem in list_of_tech for item in elem]
    if dataframe is None:
        flat_list = ["APT_Name"] + tech_list
        dataframe = pd.DataFrame(columns=flat_list)
        dataframe["APT_Name"] = [names]
        dataframe[tech_list] = [1]
        return dataframe
    else:
        dict_dfobj = {"APT_Name": names}
        for item in tech_list:
            dict_dfobj[item] = 1
        dataframe = dataframe.append(dict_dfobj, ignore_index=True)
        return dataframe


def main():
    apt_info_obj = APT_Info()
    result_df = apt_info_obj.all()
    list_of_APT_names = result_df.index.to_list()
    dataframe = None
    for names in list_of_APT_names:
        apt_info = apt_info_obj.display_apt_info(names)
        if 'Techniques Used' in apt_info.keys():
            df_techniques = apt_info['Techniques Used']['ID'].str.extract(r'(T\d{4}(?:\.\d+)?)')
            dataframe = create_dataframe_obj(df_techniques, names, dataframe)
    dataframe.fillna(0, inplace=True)
    dataframe.sort_index(axis=1, inplace=True, ascending=True)
    y = dataframe["APT_Name"]
    print(y)
    input('s')
    x = dataframe.drop("APT_Name", axis=1)
    clf = DecisionTreeClassifier()
    clf = clf.fit(x, y)
    if pickle.dump(clf, open("APT_tech.sav", 'wb')):
        print("Dumped APT_tech.sav...")
    with open("Exisiting_Techniques.txt", "w+") as f:
        for item in dataframe.columns.tolist():
            f.write(str(item)+"\n")
    


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()