import pymongo
from .objects import Sample


class Client:
    COLLECTION_NAMES = {Sample: 'samples'}

    def __init__(self, database):
        """
        Connect to a MongoDB datbase.

        Parameters
        ----------
        database: pymongo.Database or URI string
        """
        if isinstance(database, str):
            database = _get_database(database)
        self._db = database

    def _new_document(self, obj_type, args, kwargs):
        """
        Insert a new document with a new uuid.
        """
        # Make a new object (e.g. Sample)
        obj = obj_type(*args, **kwargs)

        # Find the assocaited MongoDB collection.
        collection_name = self.COLLECTION_NAMES[obj_type]
        collection = self._db[collection_name]

        # Insert the new object.
        collection.insert(obj.to_dict())

        # Observe any updates to the object and sync them to MongoDB.
        obj.observe(self._update)

        return obj

    def _update(self, change):
        """
        Sync a change to an object, observed via traitlets, to MongoDB.
        """
        # The 'revision' trait is a read-only trait, so if it is being changed
        # it is being changed by us, and we don't need to process it.
        # Short-circuit here to avoid an infinite recursion.
        if change['name'] == 'revision':
            return
        owner = change['owner']
        collection_name = self.COLLECTION_NAMES[type(owner)]
        collection = self._db[collection_name]
        revisions = self._db[f'{collection_name}_revisions']
        filter = {'uuid': owner.uuid}
        update = {'$set': {change['name']: change['new']},
                  '$inc': {'revision': 1}}
        # TODO Use transactions for this once we have MongoDB 4.0+.
        # Increment the revision number.
        owner.set_trait('revision', owner.revision + 1)
        # Update the document in {collection_name}.
        original = collection.find_one_and_update(filter, update)
        # Remove the internal MongoDB id.
        original.pop('_id')
        # Insert the old version in {collection_name}_revisions
        revisions = revisions.insert(original)

    def new_sample(self, *args, **kwargs):
        return self._new_document(Sample, args, kwargs)

    def revisions(self, obj):
        """
        Access all revisions to an object.
        """
        revisions = self._db[f'{self.COLLECTION_NAMES[type(obj)]}_revisions']
        for document in revisions.find({'uuid': obj.uuid}):
            # Remove the internal MongoDB id.
            document.pop('_id')
            # Handle the read_only traits separately.
            uuid = document.pop('uuid')
            revision = document.pop('revision')
            ret = type(obj)(**document)
            ret.set_trait('uuid', uuid)
            ret.set_trait('revision', revision)
            yield ret


def _get_database(uri):
    client = pymongo.MongoClient(uri)
    try:
        # Called with no args, get_database() returns the database
        # specified in the client's uri --- or raises if there was none.
        # There is no public method for checking this in advance, so we
        # just catch the error.
        return client.get_database()
    except pymongo.errors.ConfigurationError as err:
        raise ValueError(
            f"Invalid client: {client} "
            f"Did you forget to include a database?") from err
