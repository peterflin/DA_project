import pymongo
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv("CSV2JSON.csv")
    data = {}
    member_gp = df.groupby("member_id")
    member_data = []
    for k in member_gp.groups:
        member_df = member_gp.get_group(k)
        member_row = {
            '_id': k,
            "member_id": k,
            'tags': []
        }
        tags = dict()
        for row in member_df[member_df['tag_name'] != "三年客訴"].iterrows():
            tags['tag_name'] = row[1]['tag_name']
            if "detail" not in tags:
                tags['detail'] = [{"detail_name": row[1]['detail_name'],
                                   "detail_value": int(row[1]['detail_value'])}]
            else:
                tags['detail'].append({"detail_name": row[1]['detail_name'],
                                       "detail_value": int(row[1]['detail_value'])})
        member_row['tags'].append(tags)
        for row in member_df[member_df['tag_name'] == "三年客訴"].iterrows():
            tags = dict()
            tags["tag_name"] = row[1]['tag_name']
            tags['detail'] = [{"detail_name": row[1]['detail_name'], "detail_value": row[1]['detail_value']}]
            member_row['tags'].append(tags)
        member_data.append(member_row)
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")  # port
    db = db_client['guotai']
    col = db['guotai']
    result = col.insert_many(member_data)
    print(result.inserted_ids)

