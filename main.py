from takujoshiki import Takujoshiki
from googleSpreadsheet import send_sheet

import sys

SECRET_URL = sys.argv[1]


def main():
    takujoshiki = Takujoshiki()
    content, title = takujoshiki.run()
    if content is not None:
        send_sheet(content, title, SECRET_URL)



if __name__ == '__main__':
    main()
