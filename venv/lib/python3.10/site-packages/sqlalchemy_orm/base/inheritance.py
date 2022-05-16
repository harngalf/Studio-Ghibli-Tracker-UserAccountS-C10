from sqlalchemy import Column, String
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.base.helper import HelperBase


class InheritanceBase(HelperBase):
    __inheritance__ = True

    @declared_attr
    def _type(cls):
        if cls.__inheritance__:
            return Column(String)

    @declared_attr
    def __mapper_args__(cls):
        mapper_args = {}

        if cls.__inheritance__:
            mapper_args["polymorphic_identity"] = cls.__name__

            if cls.is_base():
                mapper_args["polymorphic_on"] = cls._type

        else:
            mapper_args["concrete"] = True

        return mapper_args
