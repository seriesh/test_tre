import pandas as pd
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', 100)


# 架空のデータ
race_info_data = {
    'RaceDate': ['2023-10-01'] * 6,
    'RaceVenue': ['平和島'] * 6,
    'RaceNumber': [1] * 6,
    'Weather': ["晴れ"] * 61   q
    'WindDirection': ["北"] * 6,
    'WindSpeed': [3.0] * 6,
    'WaveHeight': [0.5] * 6,
    'AirTemperature': [25.0] * 6,
    'WaterTemperature': [22.0] * 6,
    'Tide': ["上げ潮"] * 6,
    'CurrentSpeed': [1.0] * 6,
    'Stabilizer': [True] * 6,
    'BoatNumber': [1, 2, 3, 4, 5, 6],
    'RegistrationNumber': [1001, 1002, 1003, 1004, 1005, 1006],
    'MotorNumber': [2001, 2002, 2003, 2004, 2005, 2006],
    'EntryCourse': [1, 2, 3, 4, 5, 6],
    'StartTiming': [0.1, 0.2, 0.15, 0.18, 0.12, 0.14],
    'Result': [1, 2, 3, 4, 5, 6],
    'WinningMove': ["逃げ", "差し", "まくり", "まくり差し", "抜き", "恵まれ"]
}

racer_info_data = {
    'RegistrationNumber': [1001, 1002, 1003, 1004, 1005, 1006],
    'RaceDate': ['2023-10-01'] * 6,
    'RaceVenue': ['平和島'] * 6,
    'RaceNumber': [1] * 6,
    'Class': ['A1', 'A2', 'B1', 'B2', 'A1', 'A2'],
    'Age': [30, 25, 35, 28, 24, 33],
    'Weight': [60.0, 65.0, 70.0, 75.0, 68.0, 72.0],
    'FCount': [0, 1, 2, 0, 1, 0],
    'LCount': [1, 0, 0, 1, 0, 1],
    'AverageST': [0.15, 0.16, 0.17, 0.14, 0.18, 0.13],
    'NationalWinRate': [30.0, 28.0, 25.0, 22.0, 35.0, 32.0],
    'NationalSecondPlaceRate': [20.0, 18.0, 15.0, 12.0, 25.0, 22.0],
    'NationalThirdPlaceRate': [10.0, 8.0, 5.0, 2.0, 15.0, 12.0],
    'WinRate': [30.0, 28.0, 25.0, 22.0, 35.0, 32.0],
    'SecondPlaceRateRacer': [20.0, 18.0, 15.0, 12.0, 25.0, 22.0],
    'ThirdPlaceRateRacer': [10.0, 8.0, 5.0, 2.0, 15.0, 12.0]
}

racer_master_data = {
    'RegistrationNumber': [1001, 1002, 1003, 1004, 1005, 1006],
    'Name': ['選手A', '選手B', '選手C', '選手D', '選手E', '選手F'],
    'Gender': [0, 1, 0, 1, 0, 1],
    'Hometown': ['東京', '大阪', '福岡', '名古屋', '札幌', '仙台'],
    'Branch': ['東京支部', '大阪支部', '福岡支部', '名古屋支部', '札幌支部', '仙台支部']
}

motor_info_data = {
    'MotorNumber': [2001, 2002, 2003, 2004, 2005, 2006],
    'RaceDate': ['2023-10-01'] * 6,
    'RaceVenue': ['平和島'] * 6,
    'RaceNumber': [1] * 6,
    'SecondPlaceRateMotor': [15.0, 14.0, 13.0, 12.0, 11.0, 10.0],
    'ThirdPlaceRateMotor': [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
}



race_info_df = pd.DataFrame(race_info_data)
racer_info_df = pd.DataFrame(racer_info_data)
racer_master_df = pd.DataFrame(racer_master_data)
motor_info_df = pd.DataFrame(motor_info_data)

# レーサー情報, レーサーマスタを結合
racer_info_merged = pd.merge(racer_info_df, racer_master_df, on='RegistrationNumber', how='left')
# レース情報, マージしたレーサー情報を結合
race_info_merged = pd.merge(race_info_df, racer_info_merged, on=['RegistrationNumber', 'RaceDate', 'RaceVenue', 'RaceNumber'], how='left')
# マージしたレース情報, モーター情報を結合
final_df = pd.merge(race_info_merged, motor_info_df, on=['MotorNumber', 'RaceDate', 'RaceVenue', 'RaceNumber'], how='left')

# 最終的なDFのイメージ
final_df.head(6)


### ラベリングの前に、データの前処理は必要<br>
- 欠損値の補完：空白やnullを処理する　異常データの破棄：通常はあり得ない数値や文字のデータを処理する
- 本データセット(ボートレース)は、1レースに対して6レーサー分の情報がある。
- とりあえず、平均値で処理、対象レコードを削除、、みたいな形で行うと、レースの特徴量分布を損ねてしまうかも(6レコードで一つの情報だから、どこか一つのパラメーターを勝手にいじれない)。
- → 前処理を行うとしたら、6レコード分削除するケースも出てくるかも



# 各項目のユニークな値に基づいてラベリングを実施する
def create_label_mapping(series):
    unique_values = series.unique()
    return {value: idx for idx, value in enumerate(unique_values)}



# ラベリングを行う
weather_mapping = create_label_mapping(final_df['Weather'])
wind_direction_mapping = create_label_mapping(final_df['WindDirection'])
tide_mapping = create_label_mapping(final_df['Tide'])
winning_move_mapping = create_label_mapping(final_df['WinningMove'])
class_mapping = create_label_mapping(final_df['Class'])
gender_mapping = create_label_mapping(final_df['Gender'])
hometown_mapping = create_label_mapping(final_df['Hometown'])
branch_mapping = create_label_mapping(final_df['Branch'])
venue_mapping = create_label_mapping(final_df['RaceVenue'])

# ラベリングを適用した値をDFに反映する
# ラベリングを行う項目はmdファイルに記載
final_df['Weather'] = final_df['Weather'].map(weather_mapping)
final_df['WindDirection'] = final_df['WindDirection'].map(wind_direction_mapping)
final_df['Tide'] = final_df['Tide'].map(tide_mapping)
final_df['WinningMove'] = final_df['WinningMove'].map(winning_move_mapping)
final_df['Class'] = final_df['Class'].map(class_mapping)
final_df['Gender'] = final_df['Gender'].map(gender_mapping)
final_df['Hometown'] = final_df['Hometown'].map(hometown_mapping)
final_df['Branch'] = final_df['Branch'].map(branch_mapping)
final_df['RaceVenue'] = final_df['RaceVenue'].map(venue_mapping)

# true,falseを0,1 
final_df['Stabilizer'] = final_df['Stabilizer'].apply(lambda x: 1 if x else 0)

# 日付と名前は学習データにいらないから削除
final_df = final_df.drop(columns=['RaceDate', 'Name'])

final_df.head(6)




# 正規化が必要な項目
columns_to_normalize = [
    'WindSpeed', 'WaveHeight', 'AirTemperature', 'WaterTemperature',
    'CurrentSpeed', 'StartTiming', 'Age', 'Weight', 'AverageST',
    'NationalWinRate', 'NationalSecondPlaceRate', 'NationalThirdPlaceRate',
    'WinRate', 'SecondPlaceRateRacer', 'ThirdPlaceRateRacer', 'SecondPlaceRateMotor','ThirdPlaceRateMotor'
]

# Min-Maxスケーリング
scaler = MinMaxScaler()
final_df[columns_to_normalize] = scaler.fit_transform(final_df[columns_to_normalize])

final_df.head(6)




# モデル作成
def create_model(classification_type, model_type, df):
    # 目的変数の分類数を選択
    if classification_type == 1:
        final_df['Target'] = final_df['Result'].apply(lambda x: 1 if x == 1 else 0)
    elif classification_type == 2:
        final_df['Target'] = final_df['Result'].apply(lambda x: x if x in [1, 2] else 0)
    elif classification_type == 3:
        final_df['Target'] = final_df['Result'].apply(lambda x: x if x in [1, 2, 3] else 0)
        
    # 特徴量と目的変数を分ける
    X = final_df.drop(['Result', 'Target'], axis=1)
    y = final_df['Target']
    print(y)

    # 訓練データ、テストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=777)

    # モデル選択
    if model_type == 'RandomForest':
        model = RandomForestClassifier(random_state=777)
    elif model_type == 'LogisticRegression':
        model = LogisticRegression(random_state=777)
    elif model_type == 'SVM':
        model = SVC(random_state=777)
    else:
        raise ValueError("Unsupported model")

    # 訓練
    model.fit(X_train, y_train)

    # 予測
    y_pred = model.predict(X_test)

    # モデルの評価
    print("正解率:", accuracy_score(y_test, y_pred))
    print("分類結果:\n", classification_report(y_test, y_pred))




# ランダムフォレスとで1位かそれ以外を予測する
create_model(1, 'RandomForest', final_df)

# ロジスティック回帰モデルで1位,2位,それ以外を予測する
create_model(2, 'LogisticRegression', final_df)

# サポートベクターマシーンで1位,2位,3位かそれ以外を予測する
create_model(3, 'SVM', final_df)


