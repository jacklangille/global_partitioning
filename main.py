from include.hab_study import HabStudy
import random
import json

if __name__ == "__main__":

    with open("studies/hab_studies.json", "r") as f:
        studies = json.load(f)

    for i in range(len(studies)):
        name = studies[i]["name"]
        cells = studies[i]["cells"]
        ndvi_dict = {cell_id: random.random() for cell_id in cells}
        new_study = HabStudy(cells, name)
        new_study.create_map()
        new_study.save_cell_ndvi(ndvi_dict)
