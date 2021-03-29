from MITRE import APT_Info


def main():
    y = APT_Info()
    print(y.all())
    res_df = y.display_apt_info("APT33")
    res_df.to_csv("res.csv")
    print(res_df)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
