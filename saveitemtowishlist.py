import os
from vinyls import Vinyls
import csv


class SaveItemToWishList:

    def __init__(self) -> None:
        self.record: dict = {}
        self.FILE_NAME: str = 'csv/users/wishlists/428198028864913408.csv'
        self.list: list = []

    def __repr__(self) -> str:
        return "\n".join(self.list)

    def file_exists(self) -> bool:
        return os.path.exists(self.FILE_NAME)

    def save_item(self, record: dict) -> None:
        if record is None:
            return
        self.record = record

    def save(self) -> None:
        if not self.file_exists() or self.record is None:
            # TODO — os.mkdir() ? os.touch()?
            return
        with open(self.FILE_NAME, mode="a", newline="") as csvfile:
            print(f'Writing {self.FILE_NAME} to file...')
            record = self.record
            try:
                record = {'name': record['name'], 'price': record['price'], 'link': record['link']}
                print(record)
            except KeyError as e:
                print(e)
            fieldnames = (["name", "price", "link"])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(record)
            csvfile.close()


if __name__ == "__main__":
    vinyl = Vinyls()
    vinyl.set_random_vinyl()
    wishlist = SaveItemToWishList()
    wishlist.save_item(vinyl.get_new_arrival_dict())
    wishlist.save()

