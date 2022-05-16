import uuid
from typing import Type

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.base.helper import HelperBase
from sqlalchemy_orm.patterns.taggable import Taggable
from sqlalchemy_orm.utils import Memoized


class TagBase(HelperBase):
    tag: str

    __inheritance__ = False

    @classmethod
    @Memoized
    def mixin(cls) -> Type[Taggable]:
        tag_cls: Type[TagBase] = cls

        class Mixin(Taggable, HelperBase):

            @classmethod
            def relations(cls, checked=None):
                super_relations = super().relations(checked=checked)
                return super_relations & {cls.tag_association_cls()}

            @classmethod
            @Memoized
            def tag_association_cls(cls):
                class TagAssociation(tag_cls.declarative_base):
                    id: str = uuid.uuid4
                    tag: tag_cls
                    parent: cls = None

                    __tablename__ = cls.__tablename__ + '_tag'
                    __inheritance__ = False

                    @declared_attr
                    def tag_str(self):
                        return association_proxy('tag', 'tag')

                tag_name = TagAssociation.__name__
                tag_module = TagAssociation.__module__

                TagAssociation.__name__ = cls.__name__ + tag_name
                TagAssociation.__module__ = cls.__module__ + tag_module

                return TagAssociation

            @declared_attr
            def tag_associations(self):
                return relationship(
                    self.tag_association_cls(),
                    cascade="all, delete, delete-orphan"
                )

            @declared_attr
            def tags(self):
                TagAssociation = self.tag_association_cls()
                Tag: Type[TagBase] = tag_cls

                def creator(tag):
                    tag_obj = Tag(tag=tag)
                    return TagAssociation(tag=tag_obj)

                return association_proxy(
                    'tag_associations',
                    'tag_str',
                    creator=creator
                )

        return Mixin
