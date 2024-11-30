import pandas as pd
from pyproj import Transformer
import geojson


def main():
    # read csv
    # TODO read file from user input
    df = pd.read_csv("data/fulldata_01_01_01_P_병원.csv", encoding="cp949")

    # preprocess
    df = df[
        [
            "영업상태명",
            "도로명전체주소",
            "도로명우편번호",
            "사업장명",
            "최종수정시점",
            "데이터갱신일자",
            "업태구분명",
            "좌표정보(x)",
            "좌표정보(y)",
            "의료인수",
            "진료과목내용명",
        ]
    ]
    transformer = Transformer.from_crs("epsg:2097", "epsg:4326")
    df["lat"], df["lon"] = zip(
        *df.apply(
            lambda row: transformer.transform(row["좌표정보(y)"], row["좌표정보(x)"]),
            axis=1,
        )
    )
    df = df.rename(
        columns={
            "영업상태명": "business_status",
            "도로명전체주소": "address",
            "도로명우편번호": "zipcode",
            "사업장명": "name",
            "최종수정시점": "last_modified_date",
            "데이터갱신일자": "updated_date",
            "업태구분명": "business_type",
            "좌표정보(x)": "x(epsg:2097)",
            "좌표정보(y)": "y(epsg:4326)",
            "의료인수": "medical_personnel",
            "진료과목내용명": "department_content",
        }
    )
    df = df.drop(
        columns=[
            "business_status",
            "business_type",
            "x(epsg:2097)",
            "y(epsg:4326)",
            "medical_personnel",
        ]
    )
    df = df[df["lat"].notna()]
    df = df[df["lon"].notna()]

    # create feature collection
    features = []
    for _, row in df.iterrows():
        point = geojson.Point((row["lon"], row["lat"]))
        properties = {
            "name": row["name"],
            "address": row["address"] if not pd.isna(row["address"]) else "",
            "last_modified_date": (
                row["last_modified_date"]
                if not pd.isna(row["last_modified_date"])
                else ""
            ),
            "updated_date": (
                row["updated_date"] if not pd.isna(row["updated_date"]) else ""
            ),
            "department_content": (
                row["department_content"]
                if not pd.isna(row["department_content"])
                else ""
            ),
        }
        features.append(geojson.Feature(geometry=point, properties=properties))

    feature_collection = geojson.FeatureCollection(features)

    # write feature collection
    with open("kr_medical_institutions.geojson", "w", encoding="utf-8") as f:
        geojson.dump(feature_collection, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
