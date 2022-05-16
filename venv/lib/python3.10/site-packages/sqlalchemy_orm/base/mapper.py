import inspect
from typing import List, Type, Union

import sqlalchemy
import typing_inspect
from sqlalchemy import Column, ForeignKey, event
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_base import _add_attribute

from sqlalchemy_orm.base.helper import HelperBase
from sqlalchemy_orm.base.inheritance import InheritanceBase
from sqlalchemy_orm.typemapper import default_type_mapper


class DataclassConsistencyError(BaseException):
    pass


class MapperBase(InheritanceBase, HelperBase):
    type_mapper = default_type_mapper

    unresolved = {}
    models = {}

    @classmethod
    def __ignore_fields__(cls):
        return []

    @classmethod
    def fields(cls):
        fields = []

        def add_fields(cls_):
            ignore_fields = []

            if hasattr(cls_, "__ignore_fields__"):
                ignore_fields = cls_.__ignore_fields__()
            for key, type_ in cls_.__dict__.get('__annotations__', {}).items():
                if key not in ignore_fields:
                    default = getattr(cls_, key, None)
                    if isinstance(default, InstrumentedAttribute):
                        default = None
                    fields.append((key, type_, default))

        # fields for any mixins
        for cls_ in inspect.getmro(cls)[1:]:
            is_abstract = cls_.__dict__.get('__abstract__', False)

            if issubclass(cls_, MapperBase) and not is_abstract:
                break
            add_fields(cls_)

        # fields for current class
        add_fields(cls)

        return fields

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        fields = []

        if not cls.__inheritance__:
            for cls_ in MapperBase.models.values():
                if issubclass(cls, cls_):
                    fields.extend(cls_.fields())

        fields.extend(cls.fields())

        mappable = []

        for field in fields:

            key, type_, default = field
            flat_type = get_type(type_)

            if isinstance(flat_type, str):
                MapperBase.unresolved[(cls.identifier(), field)] = flat_type

            elif inspect.isclass(flat_type) and \
                    inspect.isclass(cls.declarative_base) and \
                    issubclass(flat_type, cls.declarative_base):
                key_ = (cls.identifier(), field)
                MapperBase.unresolved[key_] = flat_type.__name__

            else:
                mappable.append(field)

        cls.map(mappable)

        MapperBase.models[cls.__name__] = cls
        MapperBase.resolve()

        @event.listens_for(cls, 'mapper_configured')
        def receive_mapper_configured(mapper, class_):
            MapperBase.resolve()

        @event.listens_for(cls, 'init')
        def instant_defaults_listener(target, args, kwargs):
            defaults = {}
            for key, column in \
                    sqlalchemy.inspect(target.__class__).columns.items():
                if (
                        hasattr(column, 'default') and
                        column.default is not None and
                        key not in kwargs
                ):
                    if callable(column.default.arg):
                        defaults[key] = column.default.arg(target)
                    else:
                        defaults[key] = column.default.arg
            kwargs.update(defaults)

    @classmethod
    def map(cls, fields):
        base = cls.base()
        inheritance = cls.__inheritance__
        is_base = cls.is_base()
        parent = cls.super()

        if base and not is_base and inheritance:
            for pk in parent.primary_keys():
                key = pk.name
                column = pk._copy()
                fk = ForeignKey(f"{parent.__tablename__}.{key}")
                column.append_foreign_key(fk)
                setattr(cls, key, column)

        had_primary_key = False

        # Map the direct fields to columns
        for field in fields:
            key, type_, default = field

            nullable = is_nullable(type_)
            primary_key = not had_primary_key and (
                    is_base or not inheritance or not base)

            if primary_key:
                had_primary_key = True
            flat_type = get_type(type_)

            column_args = []

            column_type = cls.type_mapper.to_type(flat_type)

            if not column_type:
                raise TypeError(
                    f"Type '{flat_type}' could not be mapped to a Column Type"
                )

            column = Column(
                key,
                column_type,
                *column_args,
                primary_key=primary_key,
                nullable=nullable,
                default=default
            )

            _add_attribute(cls, key, column)

    @classmethod
    def resolve(cls):
        resolved = []

        for unresolved, dependency in MapperBase.unresolved.items():
            model, field = unresolved

            model = MapperBase.models.get(model)
            dependency = MapperBase.models.get(dependency)

            if dependency is not None and dependency.is_mapped():
                key, type_, default = field

                nullable = is_nullable(type_)

                if is_list(type_):
                    nullable = True
                    use_list = True
                    single_parent = False
                    cascade = "all, delete-orphan"
                    f_key_on = dependency
                    f_key_to = model
                    f_key_prefix = model.__tablename__

                else:
                    nullable = nullable
                    use_list = False
                    single_parent = False
                    cascade = "all, delete"
                    f_key_on = model
                    f_key_to = dependency
                    f_key_prefix = key

                f_keys = []

                for p_key in f_key_to.primary_keys():
                    f_key_name = f_key_prefix + "_" + p_key.name

                    fk = ForeignKey(
                        f"{f_key_to.__tablename__}.{p_key.name}",
                        onupdate="CASCADE",
                        ondelete="SET NULL"
                    )

                    f_key = Column(
                        f_key_name,
                        p_key.type,
                        fk
                    )

                    if hasattr(f_key_on, f_key_name):
                        existing_column = getattr(f_key_on, f_key_name)
                        validate_columns(f_key, existing_column, f_key_name)

                        f_key = existing_column

                    f_key.nullable = nullable
                    f_keys.append(f_key)
                    setattr(f_key_on, f_key_name, f_key)

                # Set the Relationship
                setattr(model, key, relationship(
                    dependency,
                    uselist=use_list,
                    single_parent=single_parent,
                    foreign_keys=f_keys,
                    cascade=cascade)
                        )
                # Mark as resolved
                resolved.append(unresolved)

        # Remove resolved dependencies
        for dependency in resolved:
            del MapperBase.unresolved[dependency]


def get_value(cls, key):
    for _cls in inspect.getmro(cls):
        if key in _cls.__dict__.keys():
            return _cls.__dict__.get(key)


def validate_columns(column_1, column_2, model_name):
    if column_1.type != column_2.type:
        if str(column_1.type) != str(column_2.type):
            raise DataclassConsistencyError(
                f"Column {model_name}.{column_1.name} "
                f"redefined with a inconsistent type"
            )

    fk_names_1 = {fk.target_fullname for fk in column_1.foreign_keys}
    fk_names_2 = {fk.target_fullname for fk in column_2.foreign_keys}

    if fk_names_1 != fk_names_2:
        raise DataclassConsistencyError(
            f"Column {model_name}.{column_1.name} "
            f"redefined with inconsistent foreign keys"
        )


def get_type(field_type) -> Union[Type, str]:
    origin = typing_inspect.get_origin(field_type)

    if origin is List or origin is list or origin is Union:
        args = typing_inspect.get_args(field_type, evaluate=True)
        none_type = type(None)
        args = [arg for arg in args if arg is not none_type]

        if len(args) != 1:
            raise TypeError(
                f"Field type '{field_type}' origin: '{origin}' "
                f"contained invalid args: '{args}'."
            )

        python_type = args[0]
    else:
        python_type = field_type

    if hasattr(python_type, '__forward_arg__'):
        python_type = python_type.__forward_arg__

    if not inspect.isclass(python_type) and not isinstance(python_type, str):
        raise TypeError(
            f"Field type '{field_type}' converted to '{python_type}'"
            f" which is an invalid Python Type"
        )

    return python_type


def is_nullable(field_type) -> bool:
    if typing_inspect.is_union_type(field_type):
        union_args = typing_inspect.get_args(field_type, evaluate=True)
        return len(union_args) == 2 and type(None) in union_args
    return False


def is_list(field_type):
    origin = typing_inspect.get_origin(field_type)
    return origin is list or origin is List
