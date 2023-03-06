import os
import json


class SaveToWishlist:

    def __init__(self, user_id: int) -> None:
        self.record: dict = {}
        self.user_id: int = user_id
        self.FILE_NAME: str = f'json/users/wishlists/{user_id}.json'
        self.list: list = []

    def __repr__(self) -> str:
        return "\n".join(self.list)

    def file_exists(self) -> bool:
        return os.path.exists(self.FILE_NAME)

    def save_item(self, record: dict) -> None:
        if record is None:
            return
        self.record = record

    def create_file(self):
        if not self.file_exists():
            with open(self.FILE_NAME, mode="x") as f:
                print(f'Creating {self.FILE_NAME} and writing to file...')
                json.dump({"RecordWishlist": [], "AudioWishlist": []}, f)



    def save(self) -> None:
        if not self.file_exists():
            self.create_file()
        with open(self.FILE_NAME, mode="r") as f:
            record = self.record
            data = json.load(f)
            if 'description' not in record:
                data['RecordWishlist'].append(record)
            if 'description' in record:
                data['AudioWishlist'].append(record)

        with open(self.FILE_NAME, mode="w") as outfile:
            if not self.is_in_wishlist(record):
                json.dump(data, outfile)
                # print("Record added to wishlist!")
            elif self.is_in_wishlist(record):
                print("Record is already in wishlist! Skipping...")


    def is_in_wishlist(self, record: dict) -> bool:
        with open(self.FILE_NAME, mode="r", newline="") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                return False
            return False


