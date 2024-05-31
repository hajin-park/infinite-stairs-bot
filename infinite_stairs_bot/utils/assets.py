import cv2
import os


class Assets:
    stair_asset_files = [
        "left_edge_green_brick_stair.png",
        "right_edge_green_brick_stair.png",
        "top_edge_green_brick_stair.png",
        "bottom_edge_green_brick_stair.png",
        "left_edge_gold_stair.png",
        "right_edge_gold_stair.png",
        "top_edge_gold_stair.png",
        "bottom_edge_gold_stair.png",
        "green_brick_stair.png",
        "gold_stair.png",
        "gem_stair.png",
    ]

    misc_asset_files = []

    def __init__(self, method=cv2.IMREAD_UNCHANGED):
        stair_file_paths = [
            os.path.join(os.getcwd(), "mtm", "templates", name)
            for name in self.stair_asset_files
        ]
        stair_imgs = [
            cv2.imread(
                path,
                method,
            )
            for path in stair_file_paths
        ]
        misc_file_paths = [
            os.path.join(os.getcwd(), "mtm", "templates", name)
            for name in self.misc_asset_files
        ]
        misc_imgs = [
            cv2.imread(
                path,
                method,
            )
            for path in misc_file_paths
        ]
        self.stair_assets = {
            name: file for name, file in zip(self.stair_asset_files, stair_imgs)
        }
        self.misc_assets = {
            name: file for name, file in zip(self.misc_asset_files, misc_imgs)
        }
        self.assets = {**self.stair_assets, **self.misc_assets}

    def get_asset(self, file):
        raw_name = file.split(".", 1)[0]
        return (raw_name, self.assets[file])

    def get_assets(self):
        raw_names = [name.split(".", 1)[0] for name in self.assets.keys()]
        return list(zip(raw_names, self.assets.values()))

    def get_stair_assets(self):
        raw_names = [name.split(".", 1)[0] for name in self.stair_assets.keys()]
        return list(zip(raw_names, self.stair_assets.values()))

    def get_misc_assets(self):
        raw_names = [name.split(".", 1)[0] for name in self.misc_assets.keys()]
        return list(zip(raw_names, self.misc_assets.values()))
