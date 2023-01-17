import os
import csv


class SaveToWishlist:

    def __init__(self, user_id: int) -> None:
        self.record: dict = {}
        self.user_id: int = user_id
        self.FILE_NAME: str = f'csv/users/wishlists/{user_id}.csv'
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
            print("file does not exist")
            with open(self.FILE_NAME, mode="w", newline="") as csvfile:
                print(f'Creating {self.FILE_NAME} and writing to file...')
                fieldnames = (["name", "price", "link", "genre"])
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                csvfile.close()

    def save(self) -> None:
        if not self.file_exists():
            self.create_file()

        with open(self.FILE_NAME, mode="a", newline="") as csvfile:
            record = self.record
            if not self.is_in_wishlist(record):
                fieldnames = (["name", "price", "link", "genre"])
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(record)
                csvfile.close()
            elif self.is_in_wishlist(record):
                print("Record is already in wishlist!")

    def is_in_wishlist(self, record: dict) -> bool:
        with open(self.FILE_NAME, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["name"] == record["name"]:
                    return True
            return False


# def setup(client):
#     client.add_cog(SaveToWishlist(client))

