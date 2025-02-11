import h3
import folium
import webbrowser
import os


class HabStudy:
    def __init__(
        self,
        lat: float,
        lng: float,
        resolution: int = 10,
        k: int = 45,
        buffer_rad_m: int = 10e3,
        study_name: str = None,
    ):
        self.lat: float = lat
        self.lng: float = lng
        self.res: int = resolution
        self.hex_rad: int = k
        self.buffer_rad: int = buffer_rad_m
        self.study_name: str = study_name

    def _get_center_cell(self):
        return h3.latlng_to_cell(self.lat, self.lng, self.res)

    def _get_cluster_cells(self):
        center = self._get_center_cell()
        return h3.grid_disk(center, self.hex_rad)

    def _save_map(self, m):

        if self.study_name:
            map_file = f"output/maps/{self.study_name}.html"
        else:
            map_file = f"output/maps/{self.lat}_{self.lng}.html"
        m.save(map_file)
        full_path = os.path.abspath(map_file)
        url = f"file://{full_path}"

        webbrowser.open(url)

    def create_map(self, zoom: int = 10):
        m = folium.Map(location=[self.lat, self.lng], zoom_start=zoom)
        cluster_cells = self._get_cluster_cells()

        for cell_id in cluster_cells:
            boundary = h3.cell_to_boundary(cell_id)
            folium.Polygon(
                locations=boundary, color="red", fill=True, fill_opacity=0.2
            ).add_to(m)

        folium.Circle(
            location=[self.lat, self.lng],
            radius=self.buffer_rad,
            color="red",
            fill=False,
            weight=2,
        ).add_to(m)

        self._save_map(m)

    def save_cells(self):
        if self.study_name:
            cells_db = f"output/text/{self.study_name}.txt"
        else:
            cells_db = f"output/text/{self.lat}_{self.lng}.txt"

        cluster_cells = self._get_cluster_cells()
        with open(cells_db, "w") as f:
            for cell_id in cluster_cells:
                # Get the cell's own center lat/lng
                cell_lat, cell_lng = h3.cell_to_latlng(cell_id)
                f.write(f"{cell_id} {cell_lat} {cell_lng}\n")

    def check_coord(self, lat_test: float, lng_test: float):
        test_cell = h3.latlng_to_cell(lat_test, lng_test, self.res)

        # Compare against our cluster set
        if test_cell in self._get_cluster_cells():
            return test_cell
        return None
