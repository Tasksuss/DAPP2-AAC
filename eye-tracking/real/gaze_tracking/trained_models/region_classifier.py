import math


class RegionClassifier:
    """
    Classifies gaze coordinates into 25 regions based on the existing calibration.py logic
    """

    def __init__(self):
        self.regions = {
            "25": "center",
            "1": "right", "2": "top-right-1", "3": "top-right-2", "4": "top-right-3", "5": "top-right-4",
            "6": "top-1", "7": "top-2", "8": "top-3", "9": "top-4", "10": "top-5",
            "11": "top-left-1", "12": "top-left-2", "13": "top-left-3", "14": "left-1", "15": "left-2",
            "16": "bottom-left-1", "17": "bottom-left-2", "18": "bottom-left-3", "19": "bottom-left-4",
            "20": "bottom-1",
            "21": "bottom-left-corner", "22": "bottom-right-corner", "23": "top-left-corner", "24": "top-right-corner"
        }

    def classify_point(self, x, y):
        """
        Classify normalized coordinates (0.0-1.0) into 25 regions
        This is the exact same logic from your calibration.py file

        Args:
            x (float): Normalized x coordinate (0.0-1.0)
            y (float): Normalized y coordinate (0.0-1.0)

        Returns:
            str: Region number as string ("1"-"25" or "outside")
        """
        a = 1
        cx, cy = 0.5, 0.5
        dx = x - cx
        dy = y - cy
        dist = math.hypot(dx, dy)

        inner_radius = 0.25 * a
        outer_radius = 0.47 * a

        if dist <= inner_radius:
            return "25"  # Center region

        elif dist <= outer_radius:
            # Middle ring - 20 sectors
            angle = math.degrees(math.atan2(dy, dx)) % 360
            if 0 <= angle < 36:
                return "1"
            elif 36 <= angle < 45:
                return "2"
            elif 45 <= angle < 360 / 7:
                return "3"
            elif 360 / 7 <= angle < 72:
                return "4"
            elif 72 <= angle < 2 * 360 / 7:
                return "5"
            elif 2 * 360 / 7 <= angle < 108:
                return "6"
            elif 108 <= angle < 135:
                return "7"
            elif 135 <= angle < 144:
                return "8"
            elif 144 <= angle < 3 * 360 / 7:
                return "9"
            elif 3 * 360 / 7 <= angle < 180:
                return "10"
            elif 180 <= angle < 4 * 360 / 7:
                return "11"
            elif 4 * 360 / 7 <= angle < 216:
                return "12"
            elif 216 <= angle < 225:
                return "13"
            elif 225 <= angle < 252:
                return "14"
            elif 252 <= angle < 5 * 360 / 7:
                return "15"
            elif 5 * 360 / 7 <= angle < 288:
                return "16"
            elif 288 <= angle < 6 * 360 / 7:
                return "17"
            elif 6 * 360 / 7 <= angle < 315:
                return "18"
            elif 315 <= angle < 324:
                return "19"
            else:
                return "20"
        else:
            # Outer corners
            if x < 0.5 and y < 0.5:
                return "23"  # top-left corner
            elif x > 0.5 and y < 0.5:
                return "24"  # top-right corner
            elif x < 0.5 and y > 0.5:
                return "21"  # bottom-left corner
            elif x > 0.5 and y > 0.5:
                return "22"  # bottom-right corner
            else:
                return "outside"

    def get_region_name(self, region_number):
        """Get human-readable region name"""
        return self.regions.get(str(region_number), "unknown")

    def visualize_regions(self):
        """Return ASCII visualization of the 25 regions"""
        return """
        25-Region Grid Layout:

        ┌─────┬─────┬─────┬─────┬─────┐
        │ 23  │ 11  │ 10  │  9  │ 24  │
        ├─────┼─────┼─────┼─────┼─────┤
        │ 14  │ 15  │  6  │  5  │  4  │
        ├─────┼─────┼─────┼─────┼─────┤
        │ 16  │ 17  │ 25  │  1  │  3  │
        ├─────┼─────┼─────┼─────┼─────┤
        │ 18  │ 19  │ 20  │  2  │  8  │
        ├─────┼─────┼─────┼─────┼─────┤
        │ 21  │ 12  │ 13  │  7  │ 22  │
        └─────┴─────┴─────┴─────┴─────┘

        Center: Region 25
        Inner Ring: Regions 1-20 (angular sectors)
        Outer Corners: Regions 21-24
        """