#!/usr/bin/python
import pyaria2
import curses, os, sys, time

def curse(screen):
    # screen.clear()

    # screen.addstr(0, 0, "Current mode: Typing mode",
                  # curses.A_REVERSE)
    # screen.refresh()
    # screen.getch()
    curses.curs_set(False)
    dims = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def info():
        downloads = pyaria2.PyAria2('raspberrypi', 6800, None)

        result = []

        active = downloads.tellActive()
        waiting = downloads.tellWaiting(0, 100)
        stopped = downloads.tellStopped(0, 100)
        states = [active, waiting, stopped]

        for state in states:
            for item in state:
                name = os.path.basename(item['files'][0]['path'][:70])
                size = "%0.2f" % (int(item['totalLength']) / 1048576)
                status = item['status']
                progress = str("%0.2f" % (int(item['completedLength']) / int(item['totalLength']) * 100)) + "%"
                dl_speed = str("%0.1f" % (int(item['downloadSpeed']) / 1024)) + " KB/s"
                if dl_speed != "0.0 KB/s":
                    eta_s = (int(item['totalLength']) - int(item['completedLength'])) / int(item['downloadSpeed'])
                    m, s = divmod(eta_s, 60)
                    h, m = divmod(m, 60)
                    eta = "%d:%02d:%02d" % (h, m, s)
                else:
                    eta = "        N/A"
                result.append(name + "\t" +
                        size + " MB\t" +
                        status.replace("active", "active  ") + "\t" +
                        progress.replace("100.00", "100") + "\t\t" +
                        dl_speed.replace("0.0 KB/s", "N/A") + "\t" +
                        eta)
        return result


    def menu():
        screen.nodelay(True)
        selection = -1
        option = 0
        while selection < 0:
            string = info()
            graphics = [0] * len(string)
            graphics[option] = curses.A_REVERSE
            screen.addstr(0, 0, "NAME\t\t\t\t\t\t\tSIZE\t\tSTATUS\t\tPROGRESS\tDL\t\tETA", curses.color_pair(1) | curses.A_BOLD)
            for i in range(len(string)):
                screen.addstr(i + 1, 0, string[i], graphics[i])
            screen.refresh()
            action = screen.getch()

            if action == curses.KEY_UP:
                option = (option - 1) % len(string)
            elif action == curses.KEY_DOWN:
                option = (option + 1) % len(string)

    menu()

curses.wrapper(curse)

#main()
