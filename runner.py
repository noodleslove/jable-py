import sys
from app.scraper import Scraper

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit()

    s = Scraper()
    print(s._runner_path)
    if sys.argv[1] == "fetch" and len(sys.argv) == 2:
        try:
            print("* fetching...")
            s.fetch()
        except:
            sys.exit("Unknown fetch error!")

    elif sys.argv[1] == "send" and len(sys.argv) == 3:
        # IN PROGRESS: check this!!!
        try:
            if sys.argv[2] == "-d" or sys.argv[2] == "--daily":
                print("* sending daily email...")
                s.send_daily_email()
            elif sys.argv[2] == "-w" or sys.argv[2] == "--weekly":
                print("* sending weekly email...")
                s.send_weekly_email()
            else:
                sys.exit("Invalid arugment for send command.")
        except:
            sys.exit("Unknown send error!")

    elif sys.argv[1] == "list-model" and len(sys.argv) == 2:
        try:
            print(list(s.models.keys()))
        except:
            sys.exit("Invalid arugment for list-model command.")

    elif sys.argv[1] == "add-model" and len(sys.argv) == 4:
        try:
            print("* adding", sys.argv[2], sys.argv[3], end="...\n")
            s.add_model(sys.argv[2], sys.argv[3])
            print("* fetching...")
            s.fetch()
        except:
            s.remove_model(sys.argv[2])
            sys.exit("Invalid arugments for add-model command.")

    elif sys.argv[1] == "remove-model" and len(sys.argv) == 4:
        try:
            print("* removing", sys.argv[2], end="...\n")
            s.remove_model(sys.argv[2])
        except:
            sys.exit("Invalid arugments for remove-model command.")

    else:
        sys.exit("Unknown command!")

    print("DONE")
