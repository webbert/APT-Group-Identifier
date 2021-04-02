from MITRE import APT_Info


def main():
    y = APT_Info()
    # res_df = y.all()
    # res_df.to_csv("res.csv")
    res_df = y.display_apt_info("Dragonfly")
    # res_df.to_csv("res.csv")
    for index in res_df.keys():
        print(res_df[index])
        res_df[index].to_csv(f"res{index}.csv")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
