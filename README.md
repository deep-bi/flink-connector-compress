# PyFlink Compress Connector

[![PyPI version](https://badge.fury.io/py/flink-connector-compress.svg)](https://badge.fury.io/py/flink-connector-compress)

This small library provides Python wrapper around Java API for writing compressed bulk file sinks
Should be compatible with any Flink version above 1.15.0. As long as the Java API does not change the Python code will
be valid.

## Example usage

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

stream.sink_to(file_sink)

```

Make sure that stream is a String type! For example:

```python
from pyflink.common import Types

stream = env.from_collection(list(range(1000)))
(stream
 .map(str, output_type=Types.STRING())  # Output type must be a Java String type (not Python PickledByteArray)
 .sink_to(file_sink)
 )
```

## Hadoop setup for the Snappy compression

Download [Hadoop](https://hadoop.apache.org/release/2.8.3.html)

```bash
wget -P ~/opt/hadoop https://archive.apache.org/dist/hadoop/common/hadoop-2.8.3/hadoop-2.8.3.tar.gz
cd ~/opt/hadoop
tar -xzf hadoop-2.8.3.tar.gz
```

Set environment variables (best to put it in `~/.bashrc`). These steps require that the `JAVA_HOME` is set.

```bash
export HADOOP_HOME=$(realpath hadoop-2.8.3)
export HADOOP_COMMON_LIB_NATIVE_DIR="$HADOOP_HOME/lib/native"
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$HADOOP_HOME/lib/native"
export HADOOP_CLASSPATH=$($HADOOP_HOME/bin/hadoop classpath)
```

You also need these two JARs in Flink `lib` directory (or in Python script with `.add_jars()`):

* [Flink : Connectors : Hadoop Compatibility](https://mvnrepository.com/artifact/org.apache.flink/flink-hadoop-compatibility_2.12/1.16.0)
* [Flink Shaded Hadoop 2 Uber](https://mvnrepository.com/artifact/org.apache.flink/flink-shaded-hadoop-2-uber/2.8.3-10.0)

```bash
wget -P $FLINK_HOME/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-hadoop-compatibility_2.12/1.16.0/flink-hadoop-compatibility_2.12-1.16.0.jar
wget -P $FLINK_HOME/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar
```

To check if Hadoop has correctly detected compression codecs and native libraries run:
```bash
$HADOOP_HOME/bin/hadoop checknative -a
```

The output should be similar to this one:
```
23/01/19 13:24:07 INFO bzip2.Bzip2Factory: Successfully loaded & initialized native-bzip2 library system-native
23/01/19 13:24:07 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
Native library checking:
hadoop:  true /home/bmikulski/opt/hadoop/hadoop-2.8.3/lib/native/libhadoop.so.1.0.0
zlib:    true /lib/x86_64-linux-gnu/libz.so.1
snappy:  true /lib/x86_64-linux-gnu/libsnappy.so.1
lz4:     true revision:10301
bzip2:   true /lib/x86_64-linux-gnu/libbz2.so.1
openssl: false Cannot load libcrypto.so (libcrypto.so: cannot open shared object file: No such file or directory)!
```

If snappy is not there you can install it with: `sudo apt install libsnappy-dev`.