from aredis.client import StrictRedis as StrictRedisBase, StrictRedisCluster as StrictRedisClusterBase
from aredis.client import (
    ClusterCommandMixin, ConnectionCommandMixin, ExtraCommandMixin,
    GeoCommandMixin, HashCommandMixin, HyperLogCommandMixin,
    KeysCommandMixin, ListsCommandMixin, PubSubCommandMixin,
    ScriptingCommandMixin, SentinelCommandMixin, ServerCommandMixin,
    SetsCommandMixin, SortedSetCommandMixin, StringsCommandMixin,
    TransactionCommandMixin, StreamsCommandMixin
)
from aredis.client import (
    ClusterStringsCommandMixin, ClusterServerCommandMixin,
    ClusterConnectionCommandMixin, CLusterPubSubCommandMixin, ClusterSentinelCommands,
    ClusterKeysCommandMixin, ClusterScriptingCommandMixin, ClusterHashCommandMixin,
    ClusterSetsCommandMixin, ClusterSortedSetCommandMixin, ClusterTransactionCommandMixin,
    ClusterListsCommandMixin, ClusterHyperLogCommandMixin
)


class RedisBase(StrictRedisBase):
    __BF_RESERVE = 'BF.RESERVE'
    __BF_ADD = 'BF.ADD'
    __BF_MADD = 'BF.MADD'
    __BF_INSERT = 'BF.INSERT'
    __BF_EXISTS = 'BF.EXISTS'
    __BF_MEXISTS = 'BF.MEXISTS'
    __BF_SCANDUMP = 'BF.SCANDUMP'
    __BF_LOADCHUNK = 'BF.LOADCHUNK'
    __BF_INFO = 'BF.INFO'

    __CF_RESERVE = 'CF.RESERVE'
    __CF_ADD = 'CF.ADD'
    __CF_ADDNX = 'CF.ADDNX'
    __CF_INSERT = 'CF.INSERT'
    __CF_INSERTNX = 'CF.INSERTNX'
    __CF_EXISTS = 'CF.EXISTS'
    __CF_DEL = 'CF.DEL'
    __CF_COUNT = 'CF.COUNT'
    __CF_SCANDUMP = 'CF.SCANDUMP'
    __CF_LOADCHUNK = 'CF.LOADCHUNK'
    __CF_INFO = 'CF.INFO'

    __CMS_INITBYDIM = 'CMS.INITBYDIM'
    __CMS_INITBYPROB = 'CMS.INITBYPROB'
    __CMS_INCRBY = 'CMS.INCRBY'
    __CMS_QUERY = 'CMS.QUERY'
    __CMS_MERGE = 'CMS.MERGE'
    __CMS_INFO = 'CMS.INFO'

    __TOPK_RESERVE = 'TOPK.RESERVE'
    __TOPK_ADD = 'TOPK.ADD'
    __TOPK_QUERY = 'TOPK.QUERY'
    __TOPK_COUNT = 'TOPK.COUNT'
    __TOPK_LIST = 'TOPK.LIST'
    __TOPK_INFO = 'TOPK.INFO'

    @staticmethod
    def append_items(params, items):
        params.extend(['ITEMS'])
        params += items

    @staticmethod
    def append_error(params, error):
        if error is not None:
            params.extend(['ERROR', error])

    @staticmethod
    def append_capacity(params, capacity):
        if capacity is not None:
            params.extend(['CAPACITY', capacity])

    @staticmethod
    def append_expansion(params, expansion):
        if expansion is not None:
            params.extend(['EXPANSION', expansion])

    @staticmethod
    def append_no_scale(params, noScale):
        if noScale is not None:
            params.extend(['NONSCALING'])

    @staticmethod
    def append_weights(params, weights):
        if len(weights) > 0:
            params.append('WEIGHTS')
            params += weights

    @staticmethod
    def append_no_create(params, no_create):
        if no_create is not None:
            params.extend(['NOCREATE'])

    @staticmethod
    def append_items_and_increments(params, items, increments):
        for i in range(len(items)):
            params.append(items[i])
            params.append(increments[i])

    @staticmethod
    def append_max_iterations(params, max_iterations):
        if max_iterations is not None:
            params.extend(['MAXITERATIONS', max_iterations])

    @staticmethod
    def append_bucket_size(params, bucket_size):
        if bucket_size is not None:
            params.extend(['BUCKETSIZE', bucket_size])


class BloomCommandMixin(RedisBase):
    async def bfCreate(self, key, error_rate, capacity, expansion=None, no_scale=None):
        """
        Creates a new Bloom Filter ``key`` with desired probability of false
        positives ``errorRate`` expected entries to be inserted as ``capacity``.
        Default expansion value is 2.
        By default, filter is auto-scaling.
        """
        params = [key, error_rate, capacity]
        self.append_expansion(params, expansion)
        self.append_no_scale(params, no_scale)

        return await self.execute_command(self.__BF_RESERVE, *params)

    async def bfAdd(self, key, item):
        """
        Adds to a Bloom Filter ``key`` an ``item``.
        """
        params = [key, item]

        return await self.execute_command(self.__BF_ADD, *params)

    async def bfMAdd(self, key, *items):
        """
        Adds to a Bloom Filter ``key`` multiple ``items``.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__BF_MADD, *params)

    async def bfInsert(self, key, items, capacity=None, error=None, no_create=None, expansion=None, no_scale=None):
        """
        Adds to a Bloom Filter ``key`` multiple ``items``. If ``nocreate``
        remain ``None`` and ``key does not exist, a new Bloom Filter ``key``
        will be created with desired probability of false positives ``errorRate``
        and expected entries to be inserted as ``size``.
        """
        params = [key]
        self.append_capacity(params, capacity)
        self.append_error(params, error)
        self.append_expansion(params, expansion)
        self.append_no_create(params, no_create)
        self.append_no_scale(params, no_scale)
        self.append_items(params, items)

        return await self.execute_command(self.__BF_INSERT, *params)

    async def bfExists(self, key, item):
        """
        Checks whether an ``item`` exists in Bloom Filter ``key``.
        """
        params = [key, item]

        return await self.execute_command(self.__BF_EXISTS, *params)

    async def bfMExists(self, key, *items):
        """
        Checks whether ``items`` exist in Bloom Filter ``key``.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__BF_MEXISTS, *params)

    async def bfScandump(self, key, iter_):
        """
        Begins an incremental save of the bloom filter ``key``. This is useful
        for large bloom filters which cannot fit into the normal SAVE
        and RESTORE model.
        The first time this command is called, the value of ``iter`` should be 0.
        This command will return successive (iter, data) pairs until
        (0, NULL) to indicate completion.
        """
        params = [key, iter_]

        return await self.execute_command(self.__BF_SCANDUMP, *params)

    async def bfLoadChunk(self, key, iter_, data):
        """
        Restores a filter previously saved using SCANDUMP. See the SCANDUMP
        command for example usage.
        This command will overwrite any bloom filter stored under key.
        Ensure that the bloom filter will not be modified between invocations.
        """
        params = [key, iter_, data]

        return await self.execute_command(self.__BF_LOADCHUNK, *params)

    async def bfInfo(self, key):
        """
        Returns capacity, size, number of filters, number of items inserted, and expansion rate.
        """

        return await self.execute_command(self.__BF_INFO, key)


class CuckooCommandMixin(RedisBase):
    async def cfCreate(self, key, capacity, expansion=None, bucket_size=None, max_iterations=None):
        """
        Creates a new Cuckoo Filter ``key`` an initial ``capacity`` items.
        """
        params = [key, capacity]
        self.append_expansion(params, expansion)
        self.append_bucket_size(params, bucket_size)
        self.append_max_iterations(params, max_iterations)

        return await self.execute_command(self.__CF_RESERVE, *params)

    async def cfAdd(self, key, item):
        """
        Adds an ``item`` to a Cuckoo Filter ``key``.
        """
        params = [key, item]

        return await self.execute_command(self.__CF_ADD, *params)

    async def cfAddNX(self, key, item):
        """
        Adds an ``item`` to a Cuckoo Filter ``key`` only if item does not yet exist.
        Command might be slower that ``cfAdd``.
        """
        params = [key, item]

        return await self.execute_command(self.__CF_ADDNX, *params)

    async def cfInsert(self, key, items, capacity=None, nocreate=None):
        """
        Adds multiple ``items`` to a Cuckoo Filter ``key``, allowing the filter to be
        created with a custom ``capacity` if it does not yet exist.
        ``items`` must be provided as a list.
        """
        params = [key]
        self.append_capacity(params, capacity)
        self.append_no_create(params, nocreate)
        self.append_items(params, items)

        return await self.execute_command(self.__CF_INSERT, *params)

    async def cfInsertNX(self, key, items, capacity=None, nocreate=None):
        """
        Adds multiple ``items`` to a Cuckoo Filter ``key`` only if they do not exist yet,
        allowing the filter to be created with a custom ``capacity` if it does not yet exist.
        ``items`` must be provided as a list.
        """
        params = [key]
        self.append_capacity(params, capacity)
        self.append_no_create(params, nocreate)
        self.append_items(params, items)

        return await self.execute_command(self.__CF_INSERTNX, *params)

    async def cfExists(self, key, item):
        """
        Checks whether an ``item`` exists in Cuckoo Filter ``key``.
        """
        params = [key, item]

        return await self.execute_command(self.__CF_EXISTS, *params)

    async def cfDel(self, key, item):
        """
        Deletes ``item`` from ``key``.
        """
        params = [key, item]

        return await self.execute_command(self.__CF_DEL, *params)

    async def cfCount(self, key, item):
        """
        Returns the number of times an ``item`` may be in the ``key``.
        """
        params = [key, item]

        return await self.execute_command(self.__CF_COUNT, *params)

    async def cfScandump(self, key, iter):
        """
        Begins an incremental save of the Cuckoo filter ``key``. This is useful
        for large Cuckoo filters which cannot fit into the normal SAVE
        and RESTORE model.
        The first time this command is called, the value of ``iter`` should be 0.
        This command will return successive (iter, data) pairs until
        (0, NULL) to indicate completion.
        """
        params = [key, iter]

        return await self.execute_command(self.__CF_SCANDUMP, *params)

    async def cfLoadChunk(self, key, iter_, data):
        """
        Restores a filter previously saved using SCANDUMP. See the SCANDUMP
        command for example usage.
        This command will overwrite any Cuckoo filter stored under key.
        Ensure that the Cuckoo filter will not be modified between invocations.
        """
        params = [key, iter_, data]

        return await self.execute_command(self.__CF_LOADCHUNK, *params)

    async def cfInfo(self, key):
        """
        Returns size, number of buckets, number of filter, number of items inserted, number of items deleted,
        bucket size, expansion rate, and max iteration.
        """

        return await self.execute_command(self.__CF_INFO, key)


class CountMinSketchCommandMixin(RedisBase):
    async def cmsInitByDim(self, key, width, depth):
        """
        Initializes a Count-Min Sketch ``key`` to dimensions
        (``width``, ``depth``) specified by user.
        """
        params = [key, width, depth]

        return await self.execute_command(self.__CMS_INITBYDIM, *params)

    async def cmsInitByProb(self, key, error, probability):
        """
        Initializes a Count-Min Sketch ``key`` to characteristics
        (``error``, ``probability``) specified by user.
        """
        params = [key, error, probability]

        return await self.execute_command(self.__CMS_INITBYPROB, *params)

    async def cmsIncrBy(self, key, items, increments):
        """
        Adds/increases ``items`` to a Count-Min Sketch ``key`` by ''increments''.
        Both ``items`` and ``increments`` are lists.
        Example - cmsIncrBy('A', ['foo'], [1])
        """
        params = [key]
        self.append_items_and_increments(params, items, increments)

        return await self.execute_command(self.__CMS_INCRBY, *params)

    async def cmsQuery(self, key, *items):
        """
        Returns count for an ``item`` from ``key``.
        Multiple items can be queried with one call.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__CMS_QUERY, *params)

    async def cmsMerge(self, dest_key, num_keys, src_keys, weights=None):
        """
        Merges ``numKeys`` of sketches into ``destKey``. Sketches specified in ``srcKeys``.
        All sketches must have identical width and depth.
        ``Weights`` can be used to multiply certain sketches. Default weight is 1.
        Both ``srcKeys`` and ``weights`` are lists.
        """
        weights = weights or []
        params = [dest_key, num_keys]
        params += src_keys
        self.append_weights(params, weights)

        return await self.execute_command(self.__CMS_MERGE, *params)

    async def cmsInfo(self, key):
        """
        Returns width, depth and total count of the sketch.
        """

        return await self.execute_command(self.__CMS_INFO, key)


class TopKCommandMixin(RedisBase):
    async def topkReserve(self, key, k, width, depth, decay):
        """
        Creates a new Cuckoo Filter ``key`` with desired probability of false
        positives ``errorRate`` expected entries to be inserted as ``size``.
        """
        params = [key, k, width, depth, decay]

        return await self.execute_command(self.__TOPK_RESERVE, *params)

    async def topkAdd(self, key, *items):
        """
        Adds one ``item`` or more to a Cuckoo Filter ``key``.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__TOPK_ADD, *params)

    async def topkQuery(self, key, *items):
        """
        Checks whether one ``item`` or more is a Top-K item at ``key``.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__TOPK_QUERY, *params)

    async def topkCount(self, key, *items):
        """
        Returns count for one ``item`` or more from ``key``.
        """
        params = [key]
        params += items

        return await self.execute_command(self.__TOPK_COUNT, *params)

    async def topkList(self, key):
        """
        Return full list of items in Top-K list of ``key```.
        """

        return await self.execute_command(self.__TOPK_LIST, key)

    async def topkInfo(self, key):
        """
        Returns k, width, depth and decay values of ``key``.
        """

        return await self.execute_command(self.__TOPK_INFO, key)


class StrictRedis(BloomCommandMixin, CountMinSketchCommandMixin, CuckooCommandMixin, TopKCommandMixin,
                  ClusterCommandMixin, ConnectionCommandMixin, ExtraCommandMixin,
                  GeoCommandMixin, HashCommandMixin, HyperLogCommandMixin,
                  KeysCommandMixin, ListsCommandMixin, PubSubCommandMixin,
                  ScriptingCommandMixin, SentinelCommandMixin, ServerCommandMixin,
                  SetsCommandMixin, SortedSetCommandMixin, StringsCommandMixin,
                  TransactionCommandMixin, StreamsCommandMixin):
    """
    This class subclasses `aredis` and implements
    RedisBloom's commands.
    The client allows to interact with RedisBloom and use all of
    it's functionality.
    Prefix is according to the DS used.
    - BF for Bloom Filter
    - CF for Cuckoo Filter
    - CMS for Count-Min Sketch
    - TopK for TopK Data Structure

    For complete documentation about RedisBloom's commands, refer to http://redisbloom.io/
    """
    pass


class StrictRedisCluster(StrictRedisClusterBase, StrictRedis, ClusterCommandMixin, ClusterStringsCommandMixin,
                         ClusterServerCommandMixin, ClusterConnectionCommandMixin, CLusterPubSubCommandMixin,
                         ClusterSentinelCommands, ClusterKeysCommandMixin, ClusterScriptingCommandMixin,
                         ClusterHashCommandMixin, ClusterSetsCommandMixin, ClusterSortedSetCommandMixin,
                         ClusterTransactionCommandMixin, ClusterListsCommandMixin, ClusterHyperLogCommandMixin):
    """
    If a command is implemented over the one in StrictRedis then it requires some changes compared to
    the regular implementation of the method.
    """
    pass
