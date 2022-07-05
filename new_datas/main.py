import pandas as pd

df = pd.read_json("sample.json")

if __name__ == '__main__':
    count_fee_base = 0
    count_fee_rate = 0
    count = 0
    edges = df["edges"]
    max_ = 0
    for i in edges:
        # if i["node1_policy"] is None or i["node2_policy"] is None:
        #     # if i["node2_policy"] is None:
        #     count += 1
        #     print(i["channel_id"])
        #     del i
        if max_ < int(i["node2_policy"]["fee_rate_milli_msat"]):
            max_ = int(i["node2_policy"]["fee_rate_milli_msat"])
        count_fee_base += int(i["node1_policy"]["fee_base_msat"])
        count_fee_base += int(i["node2_policy"]["fee_base_msat"])
        count_fee_rate += int(i["node1_policy"]["fee_rate_milli_msat"])
        count_fee_rate += int(i["node2_policy"]["fee_rate_milli_msat"])
        count += 1
    print("count:", count)
    print("max:", max_)
    average_fee_base = count_fee_base / count / 2
    print("count_fee_base:", count_fee_base)
    print("average_fee_base:", average_fee_base)
    average_fee_rate = count_fee_rate / count / 2
    print("count_fee_rate:", count_fee_rate)
    print("average_fee_rate:", average_fee_rate)
    for j in edges:
        j["node1_policy"]["fee_base_msat"] = average_fee_base
        j["node2_policy"]["fee_base_msat"] = average_fee_base
    edges.to_csv("third_edges.csv")
    edges.to_json("third_edges.json", orient='records', force_ascii=False, lines='orient')
    for k in edges:
        k["node1_policy"]["fee_rate_milli_msat"] = average_fee_rate
        k["node2_policy"]["fee_rate_milli_msat"] = average_fee_rate
    edges.to_csv("firth_edges.csv")
    edges.to_json("firth_edges.json", orient='records', force_ascii=False, lines='orient')


