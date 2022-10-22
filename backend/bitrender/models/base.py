"""Contains the base class for all database models."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal, Type, TypeVar
from uuid import UUID

from tortoise.fields import (
    DatetimeField,
    ForeignKeyRelation,
    OneToOneNullableRelation,
    ReverseRelation,
    UUIDField,
)
from tortoise.models import Model
from tortoise.queryset import CountQuery, QuerySet, QuerySetSingle

from bitrender.core.acl import EVERYONE, AclAction, AclEntry, AclList, AclPermit
from bitrender.enums.list_request import SearchRule, SortOrder

if TYPE_CHECKING:
    from bitrender.schemas.list_request import ListRequestInput, ListRequestSearch

MODEL = TypeVar("MODEL", bound="BaseModel")


class BaseModel(Model):
    """Class that serves as the base for all database models.

    Attributes:
        id (UUID): Primary key of the database entry.
        created_at (datetime): Datetime, when the entry was created.
        modified_at (datetime): Datetime, when the entry was modified.
        columns (Literal): Columns present in the current model,\
             used in defining pydantic schemas."""

    id: UUID = UUIDField(pk=True)
    created_at: datetime = DatetimeField(auto_now_add=True)
    modified_at: datetime = DatetimeField(auto_now=True)

    columns = Literal["id", "created_at", "modified_at"]

    class Meta:
        """Additional model config"""

        abstract = True

    @classmethod
    def get_all(cls: Type[MODEL], lock: bool = True, skip_locked: bool = False) -> QuerySet[MODEL]:
        """Returns all database entries of the given model.

        Args:
            lock (bool, optional): Specifies if the entries should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
            skip_locked (bool, optional): Specifies if the query should skip all rows that are \
                currently locked. Defaults to False.
        Returns:
            QuerySet[_MODEL]: Queryset returning a list of entries from the database."""
        if not lock:
            return cls.all()
        return cls.all().select_for_update(skip_locked=skip_locked)

    @classmethod
    def get_by_id(cls: Type[MODEL], model_id: UUID, lock: bool = True) -> QuerySetSingle[MODEL]:
        """Returns a database entry based on the provided id.

        Args:
            model_id (UUID): Id of the database entry that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
        Returns:
            _MODEL: Entry of the model extracted from the database."""
        if not lock:
            return cls.get(id=model_id)
        return cls.select_for_update().get(id=model_id)

    @classmethod
    def get_latest(cls: Type[MODEL], lock: bool = True) -> QuerySetSingle[MODEL | None]:
        """Returns the last created database entry of the model.

        Args:
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
        Returns:
            _MODEL: Entry of the model extracted from the database."""
        if not lock:
            return cls.all().order_by("-created_at").first()
        return cls.select_for_update().order_by("-created_at").first()

    @classmethod
    def get_amount(
        cls: Type[MODEL],
        amount: int,
        offset: int,
        order: str = "-created_at",
        lock: bool = True,
        skip_locked: bool = False,
    ) -> QuerySet[MODEL]:
        """Returns a specified amount of database entries of the model.

        Args:
            amount (int): Amount of entries to select.
            offset (int): First entry to select from.
            order (str, optional): How to order the results. Defaults to "-created_at".
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
            skip_locked (bool, optional): Specifies if the query should skip all rows that are \
                currently locked. Defaults to False.

        Returns:
            list[_MODEL]: Selected database entries."""
        if not lock:
            return cls.all().order_by(order).offset(offset).limit(amount)
        return (
            cls.all()
            .select_for_update(skip_locked=skip_locked)
            .order_by(order)
            .offset(offset)
            .limit(amount)
        )

    @classmethod
    def get_list(
        cls: Type[MODEL],
        request_input: ListRequestInput[str],
        lock: bool = True,
    ) -> tuple[QuerySet[MODEL], CountQuery]:
        """Returns a list of entries of the model, filtered, sorted and limied by the data provided

        Args:
            request_input (ListRequestInput[str]): Data used to filter, sort and limit the\
                returned entries
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True
        Returns:
            tuple[QuerySet[MODEL], CountQuery]: The first item is a \
                Queryset that returns the selected database entries
                The second one is CountQuery that returns the full row amount."""
        query: QuerySet[MODEL] = cls.all()
        count_query: CountQuery | None = None
        if request_input.search is not None:
            for search_data in request_input.search:
                query = cls.__filter_query(query, search_data)
        count_query = query.count()

        if request_input.page is not None:
            query = (
                cls.all()
                .offset(request_input.page.page_nr * request_input.page.records_per_page)
                .limit(request_input.page.records_per_page)
            )
        else:
            query = cls.all()
        if lock:
            query = query.select_for_update()
        if request_input.sort is not None:
            if request_input.sort.order == SortOrder.ASC:
                query = query.order_by(request_input.sort.column)
            else:
                query = query.order_by("-" + request_input.sort.column)
        else:
            query = query.order_by("-created_at")
        return query, count_query

    @classmethod
    def __filter_query(
        cls: Type[MODEL], query: QuerySet[MODEL], filter_data: ListRequestSearch[str]
    ) -> QuerySet[MODEL]:
        match filter_data.rule:
            case SearchRule.EQUAL:
                return query.filter(**{filter_data.column: filter_data.value})
            case SearchRule.NOTEQUAL:
                return query.filter(**{f"{filter_data.column}__not": filter_data.value})
            case SearchRule.BEGINSWITH:
                return query.filter(**{f"{filter_data.column}__startswith": filter_data.value})
            case SearchRule.GREATER:
                return query.filter(**{f"{filter_data.column}__gt": filter_data.value})
            case SearchRule.GREATEROREQUAL:
                return query.filter(**{f"{filter_data.column}__gte": filter_data.value})
            case SearchRule.LESS:
                return query.filter(**{f"{filter_data.column}__lt": filter_data.value})
            case SearchRule.LESSOREQUAL:
                return query.filter(**{f"{filter_data.column}__lte": filter_data.value})
            case SearchRule.CONTAINS:
                return query.filter(**{f"{filter_data.column}__contains": filter_data.value})

    @staticmethod
    async def extend_dacl(
        relation: ForeignKeyRelation[MODEL]
        | OneToOneNullableRelation[MODEL]
        | ReverseRelation[MODEL]
        | MODEL,
        acl: list[list[AclEntry]],
    ) -> list[list[AclEntry]]:
        """Extends the dacl of a resource, with dacl of other related resources.
        It checks, if the related resource is already fetched, if it is, it gets it's dacl,\
             and extends the provided dacl with it.

        Args:
            relation (ForeignKeyRelation[MODEL] | OneToOneNullableRelation[MODEL]\
                 | ReverseRelation[MODEL] | MODEL):
                The related resource, that should extends the current dacl.
            acl (list[list[AclEntry]]): The current dacl, that should be extended.

        Returns:
            list[list[AclEntry]]: The extended dacl."""
        if isinstance(relation, BaseModel):
            relation_acl = await relation.__dacl__()
            acl.extend(relation_acl)
        elif isinstance(relation, ReverseRelation) and relation._fetched:  # pylint: disable=W0212
            for item in relation:
                if isinstance(item, BaseModel):
                    relation_item_acl = await item.__dacl__()
                    acl.extend(relation_item_acl)
        return acl

    @classmethod
    def __sacl__(cls) -> AclList:
        return [(AclPermit.DENY, EVERYONE, AclAction.VIEW)]

    async def __dacl__(self) -> list[AclList]:
        return [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
