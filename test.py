from MITRE import APT_Info
import pandas as pd


def main():
    y = APT_Info()
    res_df = y.display_apt_info("APT33")
    res_df.to_csv("res.csv")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
