from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

from support.database.mariadb_ import SupportMariadb

from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from support.interface.database import ISupportDb


class SupportDbClass:
    __vendor_to_class: Mapping[DatabaseVendorEnum, ISupportDb[Any]] = {
        DatabaseVendorEnum.MARIADB: SupportMariadb,
    }

    @classmethod
    def get_class(cls, vendor: DatabaseVendorEnum):
        return cls.__vendor_to_class[vendor]
