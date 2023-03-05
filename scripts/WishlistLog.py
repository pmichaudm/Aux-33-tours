from datetime import datetime


class WishlistLog:

    def add(self, userID, userName, recordName, recordLink):
        with open('wishlist_log.txt', 'w', encoding='utf-8') as f:
            now = datetime.now()
            current_date = now.strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            f.writelines(f'''[{current_date}] - [{current_time}] | {userID} ({userName}) added: {recordName} to their wishlist! {recordLink}''')

