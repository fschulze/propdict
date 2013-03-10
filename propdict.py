def dictproperty(method):
    method.__dictproperty__ = True
    return method


class propdict(dict):

    def __new__(cls, **kw):
        cls.__dict_properties__ = set()
        for name, method in cls.__dict__.iteritems():
            if hasattr(method, "__dictproperty__"):
                cls.__dict_properties__.add(name)
        return dict.__new__(cls, **kw)

    def __contains__(self, name):
        return name in self.keys()

    has_key = __contains__

    def __getitem__(self, key):
        if key in dict.keys(self):
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def keys(self):
        return list(set(dict.keys(self)).union(self.__dict_properties__))

    @property
    def __dict__(self):
        result = self
        for propkey in self.__dict_properties__:
            if propkey not in dict.keys(self):  # dict values take precedence
                result[propkey] = self[propkey]
        return result

    def __setattr__(self, name, value):
        if name in dir(self) and not name in self.keys():
            raise TypeError("cannot overwrite existing method")
        self[name] = value

    def __getattribute__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            item = object.__getattribute__(self, name)
            if hasattr(item, "__dictproperty__"):
                return item()
            else:
                return item

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def values(self):
        return [self[key] for key in self.keys()]

    def __len__(self):
        return len(self.keys())

    def get(self, key, default=None):
        try:
            return self[key]
        except AttributeError:
            return default

    def __repr__(self):
        r = ["{0!r}: {1!r}".format(k, v) for k, v in self.items()]
        return "propdict({" + ", ".join(r) + "})"

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if set(self.keys()) != set(other.keys()):
            return False
        for key, value in self.items():
            if other[key] != value:
                return False
        return True
