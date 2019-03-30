class AthenaCreateTableBuilder:

    def __init__(self):
        self.table = None
        self.location = None
        self.columns = {}
        self.partitions = {}

    def build(self):
        return f'''
            CREATE EXTERNAL TABLE {self.table}({self._build_columns()})
            {self._build_partitions()}
            ROW FORMAT SERDE
              'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
            WITH SERDEPROPERTIES ( 
              'escapeChar'='\\\\', 
              'separatorChar'='\;'
            ) 
            STORED AS INPUTFORMAT 
              'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
              'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
              '{self.location}'
            TBLPROPERTIES (
              'compressionType'='gzip', 
              'skip.header.line.count'='1'
            )
        '''

    def _build_columns(self):
        c = [f"{column} {d_type}" for column, d_type in self.columns.items()]
        return ", ".join(c)

    def _build_partitions(self):
        if self.partitions is not None and len(self.partitions) > 0:
            c = [f"{column} {d_type}" for column, d_type in self.partitions.items()]
            return "PARTITIONED BY (" + ", ".join(c) + ")"
        else:
            return ""


class AthenaLoadPartitionsBuilder:

    def __init__(self):
        self.table = None
        self.location = None
        self.partitions = []

    def build(self):
        return f'''
            ALTER TABLE {self.table} ADD
            {self._build_partitions()}
        '''

    def add_partition(self, partition):
        self.partitions.append(partition)

    def _build_partitions(self):
        q = ""
        for partition in self.partitions:
            values = ", ".join(f"{k} = '{v}'" for k, v in partition.items())
            location = f"{self.location}/" + "/".join(map(str, partition.values()))
            q += f"PARTITION ({values}) LOCATION '{location}'\n"

        return q
