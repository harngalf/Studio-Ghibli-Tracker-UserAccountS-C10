from typing import Callable, Type

from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta

from sqlalchemy_orm.base.helper import HelperBase
from sqlalchemy_orm.base.inheritance import InheritanceBase
from sqlalchemy_orm.base.mapper import MapperBase
from sqlalchemy_orm.typemapper import TypeMapper


class DataRMBase(MapperBase, InheritanceBase, HelperBase):
    pass


class BaseDeclarativeMeta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_, **kw):
        dict_.update(cls.__dict__)
        super().__init__(classname, bases, dict_, **kw)


def base_factory(type_map=None, base=None):
    if base and type_map is not None:
        base.type_mapper = type_map

    if base:
        combined_base = type("Base", (base, DataRMBase), {})
    else:
        combined_base = DataRMBase

    if base is None and type_map is not None:
        combined_base.type_mapper = type_map

    model: DataRMBase = declarative_base(
        cls=combined_base,
        name="Base",
        metaclass=BaseDeclarativeMeta
    )
    model.declarative_base = model

    return model


Model: Callable[[TypeMapper, Type], Type] = base_factory
