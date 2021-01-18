# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = article_model_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class ItemType(Enum):
    ARTICLE = "Article"


class Format(Enum):
    MEDIUM_THREE_BY_TWO210 = "mediumThreeByTwo210"
    NORMAL = "Normal"
    STANDARD_THUMBNAIL = "Standard Thumbnail"
    SUPER_JUMBO = "superJumbo"
    THUMB_LARGE = "thumbLarge"


class Subtype(Enum):
    PHOTO = "photo"


class TypeEnum(Enum):
    IMAGE = "image"


@dataclass
class Multimedia:
    url: str
    format: Format
    height: int
    width: int
    type: TypeEnum
    subtype: Subtype
    caption: str
    copyright: str

    @staticmethod
    def from_dict(obj: Any) -> 'Multimedia':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        format = Format(obj.get("format"))
        height = from_int(obj.get("height"))
        width = from_int(obj.get("width"))
        type = TypeEnum(obj.get("type"))
        subtype = Subtype(obj.get("subtype"))
        caption = from_str(obj.get("caption"))
        copyright = from_str(obj.get("copyright"))
        return Multimedia(url, format, height, width, type, subtype, caption, copyright)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_str(self.url)
        result["format"] = to_enum(Format, self.format)
        result["height"] = from_int(self.height)
        result["width"] = from_int(self.width)
        result["type"] = to_enum(TypeEnum, self.type)
        result["subtype"] = to_enum(Subtype, self.subtype)
        result["caption"] = from_str(self.caption)
        result["copyright"] = from_str(self.copyright)
        return result


@dataclass
class Result:
    section: str
    subsection: str
    title: str
    abstract: str
    url: str
    uri: str
    byline: str
    item_type: ItemType
    updated_date: datetime
    created_date: datetime
    published_date: datetime
    material_type_facet: str
    kicker: str
    des_facet: List[str]
    org_facet: List[str]
    per_facet: List[str]
    geo_facet: List[str]
    multimedia: List[Multimedia]
    short_url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        section = from_str(obj.get("section"))
        subsection = from_str(obj.get("subsection"))
        title = from_str(obj.get("title"))
        abstract = from_str(obj.get("abstract"))
        url = from_str(obj.get("url"))
        uri = from_str(obj.get("uri"))
        byline = from_str(obj.get("byline"))
        item_type = ItemType(obj.get("item_type"))
        updated_date = from_datetime(obj.get("updated_date"))
        created_date = from_datetime(obj.get("created_date"))
        published_date = from_datetime(obj.get("published_date"))
        material_type_facet = from_str(obj.get("material_type_facet"))
        kicker = from_str(obj.get("kicker"))
        des_facet = from_list(from_str, obj.get("des_facet"))
        org_facet = from_list(from_str, obj.get("org_facet"))
        per_facet = from_list(from_str, obj.get("per_facet"))
        geo_facet = from_list(from_str, obj.get("geo_facet"))
        multimedia = from_list(Multimedia.from_dict, obj.get("multimedia"))
        short_url = from_str(obj.get("short_url"))
        return Result(section, subsection, title, abstract, url, uri, byline, item_type, updated_date, created_date, published_date, material_type_facet, kicker, des_facet, org_facet, per_facet, geo_facet, multimedia, short_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["section"] = from_str(self.section)
        result["subsection"] = from_str(self.subsection)
        result["title"] = from_str(self.title)
        result["abstract"] = from_str(self.abstract)
        result["url"] = from_str(self.url)
        result["uri"] = from_str(self.uri)
        result["byline"] = from_str(self.byline)
        result["item_type"] = to_enum(ItemType, self.item_type)
        result["updated_date"] = self.updated_date.isoformat()
        result["created_date"] = self.created_date.isoformat()
        result["published_date"] = self.published_date.isoformat()
        result["material_type_facet"] = from_str(self.material_type_facet)
        result["kicker"] = from_str(self.kicker)
        result["des_facet"] = from_list(from_str, self.des_facet)
        result["org_facet"] = from_list(from_str, self.org_facet)
        result["per_facet"] = from_list(from_str, self.per_facet)
        result["geo_facet"] = from_list(from_str, self.geo_facet)
        result["multimedia"] = from_list(lambda x: to_class(Multimedia, x), self.multimedia)
        result["short_url"] = from_str(self.short_url)
        return result


@dataclass
class ArticleModel:
    status: str
    copyright: str
    section: str
    last_updated: datetime
    num_results: int
    results: List[Result]

    @staticmethod
    def from_dict(obj: Any) -> 'ArticleModel':
        assert isinstance(obj, dict)
        status = from_str(obj.get("status"))
        copyright = from_str(obj.get("copyright"))
        section = from_str(obj.get("section"))
        last_updated = from_datetime(obj.get("last_updated"))
        num_results = from_int(obj.get("num_results"))
        results = from_list(Result.from_dict, obj.get("results"))
        return ArticleModel(status, copyright, section, last_updated, num_results, results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_str(self.status)
        result["copyright"] = from_str(self.copyright)
        result["section"] = from_str(self.section)
        result["last_updated"] = self.last_updated.isoformat()
        result["num_results"] = from_int(self.num_results)
        result["results"] = from_list(lambda x: to_class(Result, x), self.results)
        return result


def article_model_from_dict(s: Any) -> ArticleModel:
    return ArticleModel.from_dict(s)


def article_model_to_dict(x: ArticleModel) -> Any:
    return to_class(ArticleModel, x)
