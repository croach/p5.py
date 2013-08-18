from multiprocessing import Process
import webbrowser

from .server import SketchProcess, SketchServer


class Sketch(object):
    frame_rate = 10
    width = 100
    height = 100

    def setup(self):
        pass

    def draw(self):
        pass

    def run(self, port=8000):
        worker = Process(target=SketchProcess(self))
        server = Process(target=SketchServer(port))
        worker.start()
        server.start()
        webbrowser.open_new('http://localhost:%d' % port)
        print "Press ctrl-c to exit..."
        try:
            worker.join()
            server.join()
        except KeyboardInterrupt:
            worker.terminate()
            server.terminate()

    @property
    def frame(self):
        frame = self._frame
        frame['canvas'] = {
            'width': self.width,
            'height': self.height
        }
        return frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame

