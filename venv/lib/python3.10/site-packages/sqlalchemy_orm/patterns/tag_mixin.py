import uuid

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.base.helper import HelperBase
from sqlalchemy_orm.patterns.taggable import Taggable
from sqlalchemy_orm.utils import Memoized


class TagMixin(Taggable):

    @classmethod
    @Memoized
    def tag_cls(cls):
        if not issubclass(cls, HelperBase):
            raise TypeError(
                f"TagMixin class {cls} must be a subclass of {HelperBase}."
            )

        class Tag(cls.declarative_base):
            id: str = uuid.uuid4
            tag: str
            parent: cls = None

            __tablename__ = cls.__tablename__ + '_tag'
            __inheritance__ = False

        Tag.__name__ = cls.__name__ + Tag.__name__
        Tag.__module__ = cls.__module__ + Tag.__module__

        return Tag

    @declared_attr
    def tags_relationship(self):
        Tag = self.tag_cls()
        return relationship(Tag, cascade="all, delete, delete-orphan")

    @declared_attr
    def tags(self):
        return association_proxy(
            'tags_relationship',
            'tag',
            creator=lambda tag: self.tag_cls()(tag=tag)
        )
