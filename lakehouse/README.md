# Apache Iceberg vs Delta Lake vs Apache Hive: A Detailed Comparison

This README compares three major data lake solutions: **Apache Iceberg**, **Delta Lake**, and **Apache Hive**, focusing on how they handle updates, deletes, metadata management, file handling, and compaction. Each system has unique strengths and design philosophies that cater to different use cases in modern data engineering.

---

## **Overview**

| **Aspect**                  | **Apache Iceberg**                                            | **Delta Lake**                                               | **Apache Hive**                                      |
|-----------------------------|--------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------|
| **Primary Use Case**         | Multi-engine transactional data lakes.                     | ACID-compliant data lakes within the Spark ecosystem.        | Batch processing and querying in Hadoop-based systems. |
| **Data Format**              | Apache Parquet, ORC, Avro.                                  | Apache Parquet.                                             | Apache Parquet, ORC, Avro.                         |
| **ACID Compliance**          | Yes (row-level updates and deletes).                       | Yes (file-level updates and deletes).                      | Yes (via Hive ACID tables, with limitations).      |
| **Time Travel**              | Snapshot-based.                                             | Log-based.                                                  | Limited; snapshot isolation introduced recently.   |
| **Integration**              | Multi-engine (Spark, Flink, Trino, etc.).                  | Spark-centric, with growing support for other engines.      | Primarily tied to Hive and Hadoop ecosystem.       |

---

## **File Handling**

### **Apache Iceberg**
- **How It Works**:
  - Updates or deletes create new files for:
    - **Updated rows**.
    - **Remaining rows** (unchanged rows).
  - Uses **manifest files** to track valid files for each snapshot.
- **Compaction**:
  - Required to merge small files created during updates/deletes.
  - Reduces query overhead by consolidating many small files into fewer larger files.

### **Delta Lake**
- **How It Works**:
  - Similar to Iceberg, updates or deletes create new files for:
    - **Updated rows**.
    - **Remaining rows** (unchanged rows).
  - Marks old files as **invalid** in the `_delta_log`.
- **Compaction**:
  - Also required to merge small files into larger ones for optimized query performance.
  - Maintains compaction metadata in the `_delta_log`.

### **Apache Hive**
- **How It Works**:
  - Uses delta files to log changes (inserts, updates, deletes).
  - Periodically merges base files with delta files to create new base files.
- **Compaction**:
  - Essential for maintaining performance.
  - Two types: **Minor** (merges delta files) and **Major** (merges delta files with base files).

---

## **Metadata Management**

### **Apache Iceberg**
- **Mechanism**:
  - Stores metadata in **manifest files**.
  - Manifests list valid data files for a snapshot.
- **Time Travel**:
  - Directly supported by retaining old snapshots in the metadata.
- **Concurrency Control**:
  - Snapshot-based isolation ensures consistent reads and writes.

### **Delta Lake**
- **Mechanism**:
  - Tracks metadata via a transaction log (`_delta_log`).
  - Each operation appends a new entry to the log.
- **Time Travel**:
  - Log-based time travel; queries can access previous versions of the data by referencing older log entries.
- **Concurrency Control**:
  - Uses optimistic concurrency with conflict detection during writes.

### **Apache Hive**
- **Mechanism**:
  - Relies on the Hive Metastore to manage table metadata.
  - Delta files log changes; compaction consolidates these changes into the base data.
- **Time Travel**:
  - Limited support; newer versions support snapshot-like features for ACID tables.
- **Concurrency Control**:
  - Basic locking mechanisms to prevent conflicts during writes.

---

## **Row-Level Updates and Deletes**

### **Apache Iceberg**
- Handles updates and deletes at the **row level**:
  - Rewrites affected rows into new files.
  - Remaining rows are copied into separate new files.

### **Delta Lake**
- Handles updates and deletes at the **file level**:
  - Invalidates the old file containing affected rows.
  - Rewrites both updated rows and remaining rows into new files.

### **Apache Hive**
- Updates and deletes are handled via **delta files**:
  - Logs changes (inserts, updates, deletes) in separate delta files.
  - Periodic compaction merges these changes into base files.

---

## **Compaction**

| **Aspect**             | **Apache Iceberg**                                          | **Delta Lake**                                            | **Apache Hive**                              |
|------------------------|-----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------|
| **When Needed**         | After frequent updates or deletes that create small files.| After frequent updates or deletes that create small files.| After accumulating many delta files.        |
| **Process**             | Rewrites small files into larger ones.                   | Merges small files into larger ones.                    | Merges delta files with base files.          |
| **Impact on Queries**   | Improves read performance by reducing file scanning overhead.| Improves read performance by reducing file scanning overhead.| Improves query performance significantly.   |

---

## **Example Workflows**

### **Scenario**
- Initial data file: `file1.parquet` contains **1,000 rows** ([1, 2, ..., 1000]).
- Update operation: Modify rows [101, 102, ..., 200].

### **Apache Iceberg**
1. Identify the affected file (`file1.parquet`).
2. Create two new files:
   - `file2.parquet`: Rows [1, 2, ..., 100], [201, 202, ..., 1000] (unchanged rows).
   - `file3.parquet`: Rows [101, 102, ..., 200] (updated rows).
3. Update the manifest file to:
   - Add references to `file2.parquet` and `file3.parquet`.
   - Remove reference to `file1.parquet`.

### **Delta Lake**
1. Identify the affected file (`file1.parquet`).
2. Create two new files:
   - `file2.parquet`: Rows [1, 2, ..., 100], [201, 202, ..., 1000] (unchanged rows).
   - `file3.parquet`: Rows [101, 102, ..., 200] (updated rows).
3. Update the `_delta_log` to:
   - Mark `file1.parquet` as invalid.
   - Add `file2.parquet` and `file3.parquet` as valid.

### **Apache Hive**
1. Log changes (rows [101, 102, ..., 200]) in a delta file:
   - `delta_1.parquet`: Rows [101, 102, ..., 200] (updated rows).
2. During compaction:
   - Merge the delta file with the base file to create a new base file.

---

## **Key Differences**

| **Aspect**              | **Apache Iceberg**                                         | **Delta Lake**                                          | **Apache Hive**                                  |
|-------------------------|----------------------------------------------------------|-------------------------------------------------------|------------------------------------------------|
| **Update Granularity**   | Row-level.                                               | File-level.                                           | File-level with delta files.                   |
| **Metadata Format**      | Manifest files.                                          | Transaction log (`_delta_log`).                      | Hive Metastore.                                 |
| **Engine Compatibility** | Multi-engine (Spark, Flink, Trino, etc.).               | Spark-centric.                                        | Primarily tied to Hive ecosystem.              |
| **Efficiency**           | Rewrites only affected rows into new files.             | Rewrites entire files containing affected rows.       | Requires frequent compaction of delta files.   |

---

## **Conclusion**
- **Apache Iceberg**: Best for multi-engine environments and scenarios requiring efficient row-level updates and deletes.
- **Delta Lake**: Excellent for Spark-centric workflows, with robust ACID compliance and time travel capabilities.
- **Apache Hive**: Suitable for legacy Hadoop systems but less efficient for modern use cases.

Choose the system that aligns with your processing requirements, query patterns, and ecosystem preferences.

### Iceberg Time Travel:  
Key Points:  
•	Time Travel works only with non-expired snapshots.  
•	Expire_snapshots removes data associated with older snapshots, making them unavailable for historical queries.  
•	If a snapshot is expired, it cannot be restored for queries or historical data analysis.  
If you need to preserve specific snapshots for long-term analytics or compliance purposes,  
 ensure they are not expired or backed up externally before using the expire_snapshots procedure.  
Once a snapshot is expired using the expire_snapshots procedure in Apache Iceberg, 
it becomes impossible to time travel to that snapshot. This means:  
- You cannot query historical data associated with the expired snapshot.  
- Any data, deletes, updates, or inserts made in that snapshot are removed from the system.  
- Only non-expired snapshots remain available for time-travel queries and historical analytics.  





