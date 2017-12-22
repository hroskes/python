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

    if getitem and not hasattr(cls, "__getitem__"):
        def __getitem__(self, item):
            return furtheraction(getattr(self, getlistfunctionname)()[item])
        cls.__getitem__ = __getitem__

    if iter and not hasattr(cls, "__iter__"):
        def __iter__(self):
            for entry in getattr(self, getlistfunctionname)():
                yield furtheraction(entry)
        cls.__iter__ = __iter__

    if len_ and not hasattr(cls, "__len__"):
        def __len__(self):
            return len(getattr(self, getlistfunctionname)())
        cls.__len__ = __len__

definegetattr(ROOT.TDirectory, "Get")
definegetattr(ROOT.RooWorkspace, "obj")

definegetitem(ROOT.TCanvas, "GetListOfPrimitives")
definegetitem(ROOT.THStack, "GetHists")
definegetitem(ROOT.TDirectory, "GetListOfKeys", furtheraction=lambda x: x.ReadObj())
