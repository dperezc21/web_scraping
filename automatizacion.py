import pandas as pd
from urllib.parse import urlparse

def main(filename):
    df = read_filename(filename)
    df = extraer_newspaper_uid(filename, df)
    df = añadir_host(df)
    return df['newspaper_uid']

def read_filename(filename):
    print("opening filename")
    return pd.read_csv(filename)

def extraer_newspaper_uid(filename, df):
    newspaper = filename.split("_")[0]
    df['newspaper_uid'] = newspaper
    return df

def añadir_host(df):
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


if __name__ == '__main__':
    filename = 'eluniversal_2021-06-04_articles.csv'
    print(main(filename))