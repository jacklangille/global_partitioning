import h3
import folium
import webbrowser
import os
from datetime import datetime


class HabStudy:
    def __init__(
        self,
        cells: list,
        study_name: str = None,
    ):
        self.cells: list = cells
        self.study_name: str = study_name

    def _save_map(self, m):
        map_file = f"output/maps/{self.study_name}.html"
        m.save(map_file)
        full_path = os.path.abspath(map_file)
        url = f"file://{full_path}"
        webbrowser.open(url)

    def create_map(self, zoom: int = 3):
        lat, lng = h3.cell_to_latlng(self.cells[0])

        m = folium.Map(location=[lat, lng], zoom_start=zoom)

        for cell_id in self.cells:
            boundary = h3.cell_to_boundary(cell_id)
            folium.Polygon(
                locations=boundary, color="red", fill=True, fill_opacity=0.2
            ).add_to(m)

        self._save_map(m)

    def save_cell_ndvi(self, ndvi_dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f"output/text/{self.study_name}_cells_{timestamp}.txt"

        with open(outfile, "w") as f:
            for cell_id in self.cells:
                ndvi = ndvi_dict[cell_id]
                lat, lng = h3.cell_to_latlng(cell_id)
                f.write(f"{cell_id}, {lat}, {lng}, {ndvi:.4f}\n")
