from include.hab_study import HabStudy
import json

if __name__ == "__main__":

    with open("studies/hab_studies.json", "r") as f:
        studies = json.load(f)

    test_lat = 37.80
    test_lng = -122.40

    for study in studies:
        new_study = HabStudy(
            study["lat"],
            study["lng"],
            study["resolution"],
            study["k"],
            study["buffer_rad_m"],
            study["name"],
        )

        cell_found = new_study.check_coord(test_lat, test_lng)

        if cell_found:
            print(
                f"Coordinate ({test_lat}, {test_lng}) is in cluster cell {cell_found}."
            )
        else:
            print(f"Coordinate ({test_lat}, {test_lng}) is NOT in the cluster.")

        new_study.create_map()
        new_study.save_cells()
