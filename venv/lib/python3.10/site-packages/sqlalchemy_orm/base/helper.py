import inspect
from typing import Type, Set

from sqlalchemy import Column
from sqlalchemy.orm import class_mapper, RelationshipProperty
from sqlalchemy.orm.base import manager_of_class
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.query import Query


class HelperBase:
    declarative_base = None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def base(cls):
        declarative_base = cls.declarative_base
        if not declarative_base:
            return None

        mro = reversed(inspect.getmro(cls))
        for mro_cls in mro:
            if mro_cls != declarative_base and \
                    issubclass(mro_cls, declarative_base):

                if not mro_cls.__dict__.get(
                        '__abstract__',
                        False
                ):
                    return mro_cls

    @classmethod
    def is_base(cls):
        base = cls.base()
        if base:
            return cls == base
        return False

    @classmethod
    def super(cls):
        mro = inspect.getmro(cls)
        for mro_cls in mro[1:]:
            base = cls.declarative_base
            if base and issubclass(mro_cls, base):

                if not mro_cls.__dict__.get(
                        '__abstract__',
                        False
                ):
                    return mro_cls

    @classmethod
    def identifier(cls):
        return cls.__name__

    @classmethod
    def filter(cls, *args, **kwargs) -> Query:
        query = cls.query()
        if args:
            query = query.filter(*args)
        if kwargs:
            query = query.filter_by(**kwargs)

        return query

    @classmethod
    def parents(cls) -> Set[Type]:
        parents = []

        _cls = cls
        while _cls:
            _cls = _cls.super()

            if _cls:
                parents.append(_cls)

        return parents

    @classmethod
    def relations(cls, checked=None) -> Set[Type]:
        if not checked:
            checked = set()
        if hasattr(cls, '__mapper__') and hasattr(cls, '__table__'):
            relations = set()

            models = cls.models

            for foreign_key in cls.__table__.foreign_keys:
                table = foreign_key.column.table
                for model in models:
                    if hasattr(model, '__table__') and \
                            model.__table__ == table:
                        relations.add(model)
                        if model not in checked:
                            checked.add(model)
                            relations.update(model.relations(checked=checked))

            for prop in class_mapper(cls).iterate_properties:
                if isinstance(prop, RelationshipProperty):
                    model = prop.mapper.class_
                    relations.add(model)
                    if model not in checked:
                        checked.add(model)
                        relations.update(model.relations(checked=checked))

            return relations

        raise RuntimeError(
            "Attempted to retrieve relations from unmapped class '{cls}'"
        )

    @classmethod
    def is_mapped(cls):
        class_manager = manager_of_class(cls)
        return class_manager and class_manager.is_mapped

    @classmethod
    def primary_keys(cls):
        if hasattr(cls, '__mapper__'):
            return cls.__mapper__.primary_key

        _primary_keys = []
        for key, value in cls.__dict__.items():
            if isinstance(value, Column):
                if value.primary_key:
                    _primary_keys.append(value)

        if _primary_keys:
            return _primary_keys

        raise RuntimeError(
            "Attempted to retrieve primary keys from unmapped class '{cls}'"
        )

    @property
    def primary_key_values(self):
        return [getattr(self, key.name) for key in self.primary_keys()]

    def __hash__(self):
        primary_key_values = (*self.primary_key_values,)
        return hash(primary_key_values)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        primary_key_dict = {
            key.name: getattr(self, key.name)
            for key in self.primary_keys()
        }
        return f"<{self.__class__.__name__} '{primary_key_dict}'>"

    def create(self, session):
        return session.create(self)

    def delete(self, session):
        return session.delete(self)
