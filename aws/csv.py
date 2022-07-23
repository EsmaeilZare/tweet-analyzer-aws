import pandas as pd


class CSV():
    def read(self, file_name, start, end):
        try:
            df = pd.read_csv(file_name, skiprows=start, nrows=end-start)
            return df
        except Exception as e:
            print(
                f"error{e} occur reading csv file {file_name} in {start}, {end}")


csv = CSV()
