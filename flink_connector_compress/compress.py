from pyflink.common.serialization import BulkWriterFactory
from pyflink.common.utils import JavaObjectWrapper
from pyflink.java_gateway import get_gateway


class Extractor(JavaObjectWrapper):
    """ An Extractor turns a record into a byte array for writing data. """

    def __init__(self, j_extractor):
        super().__init__(j_extractor)

    @staticmethod
    def simple_string_extractor() -> 'Extractor':
        """
        A Extractor implementation that extracts element to string with line separator. Make sure that the output stream
        type is a String type, not a PickledByteArray.
        """
        jvm = get_gateway().jvm
        extractor = jvm.org.apache.flink.formats.compress.extractor.DefaultExtractor()
        return Extractor(extractor)


class CompressWriterFactory(BulkWriterFactory):
    def __init__(self, j_compress_writer_factory):
        super().__init__(j_compress_writer_factory)

    def with_hadoop_compression(self, codec: str) -> 'CompressWriterFactory':
        """ Compresses the data using the provided Hadoop CompressionCodec. """
        return CompressWriterFactory(self._j_object.withHadoopCompression(codec))


class CompressWriters:
    """ Convenience builder for creating CompressWriterFactory instances. """

    @staticmethod
    def for_extractor(extractor: Extractor):
        jvm = get_gateway().jvm
        factory = jvm.org.apache.flink.formats.compress.CompressWriterFactory(extractor.get_java_object())
        return CompressWriterFactory(factory)
