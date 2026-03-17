from beanie import Document, PydanticObjectId
from typing import TypeVar, Generic, Type, Optional, Dict, Any, List, Union, Tuple
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

ModelType = TypeVar('ModelType', bound=Document)

class BaseRepo(Generic[ModelType]):
    """
    Generic repository for Beanie Document models.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: PydanticObjectId, fetch_links: bool = False) -> Optional[ModelType]:
        """Retrieve a document by its _id (Beanie handles str/ObjectId)."""
        return await self.model.get(document_id=id, fetch_links=fetch_links)
    
    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Create and insert a new document."""
        try:
            doc = self.model(**data)
            await doc.insert()
            return doc
        except ValidationError:
            raise
        except DuplicateKeyError:
            raise
    
    async def update(self, id: PydanticObjectId, update_data: Dict[str, Any]) -> Optional[ModelType]:
        """Update a document by loading it, applying changes, and saving."""
        doc = await self.model.find_one({"_id": id})
        if not doc:
            return None
        
        await doc.update({"$set": update_data})
        return doc
    
    async def delete(self, filters: Dict) -> bool:
        """Delete a document. Returns True if deleted."""
        doc = await self.model.find_one(filters)
        if not doc:
            return False
        await doc.delete()
        return True
    
    async def delete_get_count(self, filters: Dict) -> int:
        """Delete a document and get count"""
        result = await self.model.find(filters).delete()
        return result.deleted_count
    
    async def find(
            self, filters: Optional[Dict[str, Any]]=None, 
            sort: Optional[List[Union[Tuple[str, int], str]]]=None, skip: int = 0,
            limit: int = 10, fetch_links: bool=False
    ) -> List[ModelType]:
        """Find multiple documents using Beanie's query syntax."""
        query = self.model.find(filters or {}, fetch_links=fetch_links)
        if sort:
            for s in sort:
                query = query.sort(s)
        if skip:
            query = query.skip(n=skip)
        if limit is not None:
            query  = query.limit(n=limit)

        return await query.to_list()
    
    async def find_with_cursor(
            self, filters: Optional[Dict[str, Any]] = None,
            cursor_field: str = "created_at", cursor_value: Any = None,
            cursor_operator: str = "$lt", sort: Optional[List[Union[Tuple[str, int], str]]] = None,
            limit: int = 10, fetch_links: bool = False
    ) -> List[ModelType]:
        """Find multiple documents using Beanie's query syntax."""
        query = dict(filters or {})
        if cursor_value is not None:
            query[cursor_field] = {cursor_operator: cursor_value}
        return await self.find(filters=query, sort=sort, limit=limit, fetch_links=fetch_links)
    
    async def find_one(self, filters: Optional[Dict[str, Any]]=None, fetch_links: bool=False) -> Optional[ModelType]:
        """Find a single document matching the filter."""
        return await self.model.find_one(filters or {}, fetch_links=fetch_links)
    
    async def find_many_by_ids(self, ids: List[PydanticObjectId]) -> List[ModelType]:
        """Retrieve multiple documents by their _id values."""
        return await self.model.find({"_id": {"$in": ids}}).to_list()

    async def aggregate(
            self, pipeline: List[Dict[str, Any]],
            cursor_field: str = "created_at",
            cursor_value: Any = None,
            cursor_operator: str = "$lt",
            limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Run an aggregation pipeline."""
        if cursor_value:
            pipeline[0]["$match"][cursor_field] = {cursor_operator: cursor_value}

        pipeline.append({"$limit": limit})

        return await self.model.aggregate(pipeline).to_list()
        