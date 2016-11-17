#!/usr/bin/python
import pyaria2
import curses, os, sys, time

server = pyaria2.PyAria2('raspberrypi', 6800, None)

class Download:
    def __init__(self, data):
        self.data = data
        self.gid = self.data['gid']
        self.name = os.path.basename(self.data['files'][0]['path'])
        if self.name == '':
            self.name = "N/A"
        self.size = int(self.data['totalLength'])
        self.refresh(True)

    def refresh(self, scope):
        # if scope == 1 and self.status != 'active':
            # return

        self.done = int(self.data['completedLength'])
        self.status = self.data['status']
        if self.size != 0:
            self.progress = self.done / self.size * 100
        else:
            self.progress = 0
        self.dl_speed = int(self.data['downloadSpeed']) / 1024
        if self.dl_speed != 0:
            eta_s = (self.size - self.done) / (self.dl_speed * 1024)
            m, s = divmod(eta_s, 60)
            h, m = divmod(m, 60)
            self.eta = "%d:%02d:%02d" % (h, m, s)
        else:
            self.eta = "N/A"
        return self


def curse(screen):
    screen.clear()

    curses.curs_set(False)
    dims = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    s_name = 56
    s_size = 14
    s_status = 14
    s_progress = 12
    s_dl = 16
    s_eta = 12

    def get_downloads():
        downloads = []
        active = server.tellActive()
        waiting = server.tellWaiting(0, 100)
        stopped = server.tellStopped(0, 100)
        states = [active, waiting, stopped]

        for state in states:
            for i in range(len(state)):
                downloads.append(Download(state[i]))
        return downloads


    def menu():
        selection = -1
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        option = 0
        screen.nodelay(True)
        downloads = get_downloads()
        while selection < 0:
            screen.clear()
            time.sleep(0.2)
            num = len(downloads)
            if num == 0:
                num = 1
            graphics = [0] * num
            graphics[option] = curses.A_REVERSE
            t_name, t_size, t_status, t_progress, t_dl, t_eta = "NAME", "SIZE", "STATUS", "PROGRESS", "DL", "ETA"
            t_string = (
                        t_name + ((s_name) - len(t_name)) * ' ' +
                        t_size + ((s_size) - len(t_size)) * ' ' +
                        t_status + ((s_status) - len(t_status)) * ' ' +
                        t_progress + ((s_progress) - len(t_progress)) * ' ' +
                        t_dl + ((s_dl) - len(t_dl)) * ' ' +
                        t_eta + ((s_eta) - len(t_eta)) * ' '
                    )
            screen.addstr(0, 0, t_string, curses.color_pair(1) | curses.A_BOLD)
            if len(downloads) != 0:
                for i in range(len(downloads)):
                    name = downloads[i].name[:50]
                    size = str("%0.2f" % (downloads[i].size / 1048576)) + " MB"
                    status = downloads[i].status.replace("active", "active  ")
                    progress = str("%0.2f" % downloads[i].progress) + "%"
                    dl_speed = (str("%0.1f" % downloads[i].dl_speed) + " KB/s").replace("0.0 KB/s", "N/A")
                    eta = downloads[i].eta
                    item = (
                            name + (s_name - len(name)) * ' ' +
                            size + (s_size - len(size)) * ' ' +
                            status + (s_status - len(status)) * ' ' +
                            progress + (s_progress - len(progress)) * ' ' +
                            dl_speed + (s_dl - len(dl_speed)) * ' ' +
                            eta + (s_eta - len(eta)) * ' '
                           )

                    if status == 'waiting':
                        color = 2
                    elif status == 'complete':
                        color = 3
                    elif status == 'error':
                        color = 4
                    else:
                        color = 1

                    screen.addstr(i + 1, 0, item, graphics[i]|curses.color_pair(color))
            screen.refresh()
            action = screen.getch()

            if action == curses.KEY_UP or action == ord('k'):
                option = (option - 1) % num
            elif action == curses.KEY_DOWN or action == ord('j'):
                option = (option + 1) % num
            elif action == ord('P'):
                if len(server.tellActive()) == 0:
                    server.unpauseAll()
                else:
                    server.pauseAll()
            elif action == ord('b'):
                screen.addstr(10, 0, str(option))
                screen.refresh()
            elif action == ord('q'):
                break

            downloads = get_downloads()


    menu()


curses.wrapper(curse)

