from include.hab_study import HabStudy
import json
import random

if __name__ == "__main__":

    with open("studies/hab_studies.json", "r") as f:
        studies = json.load(f)

    n_trials = 10

    for study in studies:
        new_study = HabStudy(
            study["lat"],
            study["lng"],
            study["resolution"],
            study["k"],
            study["buffer_rad_m"],
            study["name"],
        )

        print("-" * 40 + study["name"] + "-" * 40)
        for i in range(n_trials):
            test_lat = random.randrange(36, 40, 1)
            test_lng = random.randrange(-120, -125, -1)
            cell_found = new_study.check_coord(test_lat, test_lng)

            print(
                f"({test_lat}, {test_lng}) {'in ' + str(cell_found) if cell_found else 'NOT in the cluster'}"
            )

        # new_study.create_map()
        # new_study.save_cells()
