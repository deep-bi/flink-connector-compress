# PyFlink Compress Connector

This small library provides Python wrapper around Java API for writing compressed bulk file sinks.

To run locally you need these JAR in your CLASSPATH:

* [flink-connector-files](https://mvnrepository.com/artifact/org.apache.flink/flink-connector-files/1.16.0) for File support
* [flink-compress](https://mvnrepository.com/artifact/org.apache.flink/flink-compress/1.16.0) for Compressed Writer
* [hadoop-client](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-client/3.3.4) for Hadoop Config
* [hadoop-common](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-common/3.3.4) for codes (like Snappy)
* [woodstox-core](https://mvnrepository.com/artifact/com.fasterxml.woodstox/woodstox-core/6.5.0) to resolve Hadoop errors
* [stax2-api](https://mvnrepository.com/artifact/org.codehaus.woodstox/stax2-api/4.2.1) to resolve Hadoop errors
* [hadoop-shaded-guava](https://mvnrepository.com/artifact/org.apache.hadoop.thirdparty/hadoop-shaded-guava/1.1.1) to resolve Hadoop errors

If you run the job on the Flink cluster with correctly defined Hadoop dependencies then only these two should be required:
* [flink-connector-files](https://mvnrepository.com/artifact/org.apache.flink/flink-connector-files/1.16.0) for File support
* [flink-compress](https://mvnrepository.com/artifact/org.apache.flink/flink-compress/1.16.0) for Compressed Writer

### Example usage

```python
from pyflink.datastream.connectors.file_system import FileSink, BucketAssigner, RollingPolicy, OutputFileConfig
from flink_connector_compress.compress import Extractor, CompressWriters

bulk_format = CompressWriters.for_extractor(Extractor.simple_string_extractor()).with_hadoop_compression("snappy")
output_config = OutputFileConfig.builder().with_part_suffix(".snappy.txt").build()

file_sink = (
    FileSink.for_bulk_format(output_path, bulk_format)
    .with_bucket_assigner(BucketAssigner.date_time_bucket_assigner(format_str="'date'=yyyy-MM-dd"))
    .with_rolling_policy(RollingPolicy.on_checkpoint_rolling_policy())
    .with_output_file_config(output_config)
    .build()
)

```