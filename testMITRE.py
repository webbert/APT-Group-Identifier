from MITRE import APT_Info


def main():
    apt_info_obj = APT_Info()
    # result_df = apt_info_obj.all()
    # result_df.to_csv("basic_info.csv")
    apt_dragonfly_dictionary = apt_info_obj.display_apt_info("G0035")
    for index in apt_dragonfly_dictionary.keys():
        apt_dragonfly_dictionary[index].to_csv(f"dragonfly-{index}.csv")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
