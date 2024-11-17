import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    if None not in (lat1, lon1, lat2, lon2):
        R = 6371.0  # radius of the Earth
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        distance = R * c
        return distance

    return None

def find_closest_bus_station(df, current_lat, current_lon):
    df["distance"] = df.apply(
        lambda row: haversine(
            current_lat, current_lon, row["latitude"], row["longitude"]
        ),
        axis=1,
    )
    closest_point = df.loc[df["distance"].idxmin()]
    closest_point = closest_point.to_dict()
    closest_point["dir_to_closest_point"] = (
        f"https://www.google.com/maps/dir/{current_lat},{current_lon}/{closest_point['latitude']},{closest_point['longitude']}"
    )

    closest_point["all_routes"] = list(
        df[df["station"] == closest_point["station"]]["route"].unique()
    )

    return closest_point