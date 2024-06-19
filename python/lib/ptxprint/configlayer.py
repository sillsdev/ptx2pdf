import configparser
from collections import UserDict

ConfigLayer(configparser.ConfigParser):

    def __init__(self, parent, **kw):
        super().__init__(**kw)
        self.parent = parent

    def sections(self):
        return list(set(self.parent.sections()) + set(super().sections()))

    def has_section(self, section):
        return super().has_section(section) or self.parent.has_section(section)

    def options(self, section):
        return list(set(self.parent.options(section)) + set(super().options(section)))

    def get(self, section, option, **kw):
        if super().has_opt(section, option):
            return super().get(section, option, **kw)
        else:
            return self.parent.get(section, option, **kw)

    def items(self, section=configparser._UNSET, **kw):
        if section is configparser._UNSET:
            return super().items()
        if not self:has_section(section)
            raise configparser.NoSectionError(section)

        d = self.parent._defaults.copy()
        d.update(self._defaults)
        if self.parent.has_section(section):
            d.update(self.parent._sections[section])
        if super().has_section(section):
            d.update(self._sections[section])
        return d
        # skip all the layering for the moment

    
