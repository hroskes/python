import ROOT

def definegetattr(cls, functionname, condition = bool):
    assert hasattr(cls, functionname)
    assert not hasattr(cls, "__getattr__")
    def __getattr__(self, attr):
        result = getattr(self, functionname)(attr)
        if condition(result):
            return result
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, attr))
    cls.__getattr__ = __getattr__

def definegetitem(cls, getlistfunctionname, getitem=True, iter=True, len_=True, furtheraction=None):
    assert hasattr(cls, getlistfunctionname)

    if furtheraction is None: furtheraction = lambda x: x

    if getitem:
        assert not hasattr(cls, "__getitem__")
        def __getitem__(self, item):
            return furtheraction(getattr(self, getlistfunctionname)()[item])
        cls.__getitem__ = __getitem__

    if iter:
        assert not hasattr(cls, "__iter__")
        def __iter__(self):
            for entry in getattr(self, getlistfunctionname)():
                yield furtheraction(entry)
        cls.__iter__ = __iter__

    if len_:
        assert not hasattr(cls, "__len__")
        def __len__(self):
            return len(getattr(self, getlistfunctionname)())
        cls.__len__ = __len__

definegetattr(ROOT.TDirectory, "Get")
definegetattr(ROOT.RooWorkspace, "obj")

definegetitem(ROOT.TPad, "GetListOfPrimitives")
definegetitem(ROOT.THStack, "GetHists")
definegetitem(ROOT.TDirectory, "GetListOfKeys", furtheraction=lambda x: x.ReadObj())

import getpass, socket
if ("login-node" in socket.gethostname() or "compute" in socket.gethostname() or "bigmem" in socket.gethostname()) and getpass.getuser():
    class __PlotCopier(object):
        import os, subprocess
        def __init__(self):
            self.__tmpdir = None

        def __del__(self):
            if self.__tmpdir is not None:
                import os, subprocess
                subprocess.check_call(["rsync", "-azvP", os.path.join(self.tmpdir, "www", ""), "hroskes@lxplus.cern.ch:www/"])

        @property
        def tmpdir(self):
            import tempfile
            if self.__tmpdir is None: self.__tmpdir = tempfile.mkdtemp()
            return self.__tmpdir

        def marccfilename(self, filename):
            import os
            if "/www/" in filename:
                filename = os.path.join(self.tmpdir, "www", filename.split("/www/", 1)[1].lstrip("/"))
                self.mkdir_p(os.path.dirname(filename))
            return filename

        def mkdir_p(self, path):
            """http://stackoverflow.com/a/600612/5228524"""
            import errno, os
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

    __plotcopier = __PlotCopier()

    prevsaveas = ROOT.TPad.SaveAs
    def SaveAs(self, filename="", *otherargs, **kwargs):
        return prevsaveas(self, __plotcopier.marccfilename(filename), *otherargs, **kwargs)
    ROOT.TPad.SaveAs = SaveAs

    def CopyPlots():
        global __plotcopier
        __plotcopier = __PlotCopier()
    assert not hasattr(ROOT, "CopyPlots")
    ROOT.CopyPlots = CopyPlots
