import pandas as pd
import csv
import json
import pickle
import sys

class Member:
    @staticmethod
    def results(filename: str, json_file: str = "report.json", pkl_file: str = "report.pkl"):


        def log_error(message, rows=None):
            with open("deepcamp_errors.log", "a") as log_file:
                log_file.write(f"- ERROR - {message}\n")
                print(f"- ERROR - {message}")
                if rows:
                    for row_num, row_text in rows.items():
                        log_file.write(f"    {row_num}: {row_text}\n")
                        print(f"    {row_num}: {row_text}")

        valid_rows = []
        seen_members = {}  


        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  
                team_id = row.get("team_id")
                member_id = row.get("member_id")
                exercise_id = row.get("exercise_id")
                score = row.get("score")
                row_text = ", ".join([team_id or "", member_id or "", exercise_id or "", score or ""])


                if not team_id or not member_id or not score or not exercise_id:
                    log_error(f"Missing some fields in row {row_num}", {row_num: row_text})
                    continue

                try:
                    score = float(score)
                except ValueError:
                    log_error(f"Invalid score format in row {row_num}: {row_text}")
                    continue


                if not (0 <= score <= 100):
                    log_error(f"Invalid score range in row {row_num}: {row_text}")
                    continue

 
                if member_id in seen_members and seen_members[member_id]["team_id"] != team_id:
                    first_row = seen_members[member_id]["row_num"]
                    first_row_text = seen_members[member_id]["row_text"]
                    log_error(
                        f"Duplicate team member between rows {first_row} and {row_num}:",
                        {first_row: first_row_text, row_num: row_text}
                    )
                    continue


                seen_members[member_id] = {"team_id": team_id, "row_num": row_num, "row_text": row_text}
                valid_rows.append({"team_id": team_id, "member_id": member_id, "score": score})


        if not valid_rows:
            return {}


        df = pd.DataFrame(valid_rows)

        # محاسبه میانگین هر تیم
        team_avg = df.groupby("team_id")["score"].mean().to_dict()

        # پیدا کردن بهترین عضو در هر تیم
        member_avg = df.groupby(["team_id", "member_id"])["score"].mean()
        top_members = member_avg.groupby("team_id").idxmax().to_dict()

        results = {}
        for team_id, avg in team_avg.items():
            top_member = top_members[team_id][1]  
            results[team_id] = {
                "average": avg,
                "top_member": top_member
            }

        # پیدا کردن تیم/تیم‌های برتر
        max_avg = max(v["average"] for v in results.values())
        top_teams = [k for k, v in results.items() if v["average"] == max_avg]
        results["top_team"] = top_teams if len(top_teams) > 1 else top_teams[0]


        with open(json_file, "w") as f:
            json.dump(results, f, indent=4)

  
        with open(pkl_file, "wb") as f:
            pickle.dump(results, f)

        return results


################################################################
def main():
    csv_file = input().strip()
    if csv_file == "Exit":
        sys.exit()
 
    result = Member.results(csv_file)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()