import sublime, sublime_plugin, subprocess

STATUS_KEY = "itunes-plugin"
SETTING_NAME = "itunes.sublime-settings"

class EventiTunes(sublime_plugin.EventListener):
    def __init__(self):
        super().__init__()
        self.settings = sublime.load_settings(SETTING_NAME)

    def on_activated_async(self, view):
        self.set_track(view)
        if not self.settings.get("auto_hide"): return
        sublime.set_timeout_async(lambda: self.unset_track(view), self.settings.get("hide_msec"))

    def set_track(self, view):
        status = self._format_status_string()
        if not status: return
        view.set_status(STATUS_KEY, status)

    def unset_track(self, view):
        view.erase_status(STATUS_KEY)

    def _format_status_string(self):
        track_data = self.get_track_data()
        if not track_data: return
        return "▶ {artist} - {name}".format(**track_data)

    def get_track_data(self):
        track_p = subprocess.Popen("osascript -l JavaScript -e 'Application(\"System Events\").applicationProcesses[\"iTunes\"](); Application(\"iTunes\").currentTrack.name();'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        track_name, err = track_p.communicate()
        if err: return
        artist_p = subprocess.Popen("osascript -l JavaScript -e 'Application(\"System Events\").applicationProcesses[\"iTunes\"](); Application(\"iTunes\").currentTrack.artist();'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        artist_name, err = artist_p.communicate()
        if err: return
        return {
            "name": track_name.decode().strip(),
            "artist": artist_name.decode().strip()
        }
