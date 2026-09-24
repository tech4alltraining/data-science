Yes. In fact, for teaching, I would **not start with Hadoop**.

You can teach the MapReduce programming model entirely in a Python notebook first:

```text
CSV dataset
   ↓
Pandas
   ↓
Mapper function
   ↓
key-value pairs
   ↓
Shuffle / Group
   ↓
Reducer function
   ↓
Result
```

Then, once students understand the logic, run essentially the **same Mapper/Reducer logic through Hadoop Streaming**. Hadoop Streaming is specifically designed to let executables such as Python programs act as the mapper and reducer. ([Apache Hadoop][1])

For your **i5 + 8 GB RAM machines**, this is also much more practical than trying to teach a full multi-node Hadoop cluster. A single-node/pseudo-distributed Hadoop installation is sufficient for the demonstrations; Apache documents this mode specifically for running Hadoop on one machine. ([Apache Hadoop][2])

## Recommended teaching structure

I would change the earlier plan to this:

| Demo | Dataset          |       Size | Python notebook | Hadoop               |
| ---- | ---------------- | ---------: | --------------- | -------------------- |
| 1    | Small text/CSV   |       Tiny | ✅               | Optional             |
| 2    | Small CSV        |      Small | ✅               | Optional             |
| 3    | Online Shoppers  |  ~12K rows | ✅               | Optional             |
| 4    | Clickstream      |  165K rows | ✅               | Recommended          |
| 5    | Online Retail    |  541K rows | ✅               | Recommended          |
| 6    | Online Retail II | 1.07M rows | ✅               | Strongly recommended |
| 7    | Streamlit        |    Results | ✅               | Optional             |

The UCI **Online Retail** dataset has 541,909 transactions, while **Online Retail II** has 1,067,371 transactions, making them particularly useful for demonstrating why distributed processing becomes interesting. ([UCI Machine Learning Repository][3])

---

# Part 1 — Environment

Since you already have pandas, I'd keep the environment simple.

### Conda

```bash
conda activate demo
```

Install the complete teaching stack:

```bash
pip install pandas numpy matplotlib seaborn jupyterlab streamlit requests openpyxl
```

Optional:

```bash
pip install ucimlrepo
```

I would actually use direct dataset downloads where possible so students can see the **"download → load → process"** workflow.

---

# Part 2 — Demo 1: Word Count Without Hadoop

The first notebook should deliberately avoid pandas.

That is important because students need to understand what a Mapper actually does.

## Notebook structure

### Cell 1 — Create a tiny dataset

```python
text = """
Python is simple
Python is powerful
Hadoop processes big data
Python processes data
Hadoop and Python work together
"""

with open("data.txt", "w") as f:
    f.write(text)

print(text)
```

---

### Cell 2 — Read the data

```python
with open("data.txt", "r") as f:
    lines = f.readlines()

lines
```

---

### Cell 3 — Mapper

```python
def mapper(lines):
    mapped = []

    for line in lines:
        words = line.strip().lower().split()

        for word in words:
            mapped.append((word, 1))

    return mapped


mapped_data = mapper(lines)

mapped_data
```

Students will see:

```text
('python', 1)
('is', 1)
('simple', 1)
('python', 1)
...
```

Explain:

> The Mapper converts the original data into **key-value pairs**.

---

### Cell 4 — Shuffle

Now implement the part Hadoop normally performs.

```python
from collections import defaultdict

def shuffle(mapped_data):
    grouped = defaultdict(list)

    for key, value in mapped_data:
        grouped[key].append(value)

    return grouped


grouped_data = shuffle(mapped_data)

dict(grouped_data)
```

Students will see something like:

```text
{
    'python': [1, 1, 1],
    'is': [1],
    'data': [1, 1],
    'hadoop': [1, 1],
    ...
}
```

This is the most important conceptual step.

---

### Cell 5 — Reducer

```python
def reducer(grouped_data):

    result = {}

    for key, values in grouped_data.items():
        result[key] = sum(values)

    return result


result = reducer(grouped_data)

result
```

---

### Cell 6 — Sort the result

```python
sorted(result.items(), key=lambda x: x[1], reverse=True)
```

Expected idea:

```text
python     3
hadoop     2
data       2
...
```

---

### Cell 7 — Complete MapReduce pipeline

Now combine everything:

```python
def map_reduce(lines):

    # MAP
    mapped = mapper(lines)

    # SHUFFLE
    grouped = shuffle(mapped)

    # REDUCE
    result = reducer(grouped)

    return result


result = map_reduce(lines)

for key, value in sorted(result.items(), key=lambda x: x[1], reverse=True):
    print(f"{key:15} {value}")
```

Now students have implemented **MapReduce without Hadoop**.

That is exactly what I recommend for Demo 1.

---

# Part 3 — Demo 2: CSV + Pandas + MapReduce

Now introduce a real dataset downloaded from the Internet.

For this demo, I suggest **Online Shoppers Purchasing Intention** from UCI. It is small enough for every student's laptop but realistic enough to introduce CSV processing. The UCI repository provides the dataset as a CSV and documents its variables. ([UCI Machine Learning Repository][4])

## Cell 1 — Download

```python
import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv"

df = pd.read_csv(url)

df.head()
```

If that particular legacy URL becomes unavailable, use the UCI repository's dataset page/download mechanism instead. ([UCI Machine Learning Repository][4])

---

## Cell 2 — Inspect dataset

```python
print("Rows:", len(df))
print("Columns:", len(df.columns))

df.info()
```

---

## Cell 3 — Understand the problem

We can ask:

> **How many visitors belong to each VisitorType?**

For example:

```text
Returning_Visitor
New_Visitor
Other
```

---

## Cell 4 — Normal Pandas solution

First show students the conventional solution:

```python
df["VisitorType"].value_counts()
```

This establishes a baseline.

---

# Cell 5 — Mapper

Now recreate the same operation using MapReduce.

```python
def mapper(df):

    mapped = []

    for visitor_type in df["VisitorType"]:
        mapped.append((visitor_type, 1))

    return mapped


mapped = mapper(df)

mapped[:10]
```

Output:

```text
[
    ('Returning_Visitor', 1),
    ('Returning_Visitor', 1),
    ('Returning_Visitor', 1),
    ...
]
```

---

# Cell 6 — Shuffle

```python
from collections import defaultdict

def shuffle(mapped):

    grouped = defaultdict(list)

    for key, value in mapped:
        grouped[key].append(value)

    return grouped


grouped = shuffle(mapped)

for key, values in grouped.items():
    print(key, len(values))
```

---

# Cell 7 — Reducer

```python
def reducer(grouped):

    result = {}

    for key, values in grouped.items():
        result[key] = sum(values)

    return result


result = reducer(grouped)

result
```

---

# Cell 8 — Compare with Pandas

```python
pandas_result = df["VisitorType"].value_counts().to_dict()

print("MapReduce:")
print(result)

print("\nPandas:")
print(pandas_result)
```

The students should see that both approaches produce the same conceptual result.

---

# Cell 9 — Make the MapReduce framework reusable

This is where I would start making the teaching progressively more advanced.

```python
def map_reduce(df, mapper, reducer):

    mapped = mapper(df)

    grouped = defaultdict(list)

    for key, value in mapped:
        grouped[key].append(value)

    result = reducer(grouped)

    return result
```

Then:

```python
result = map_reduce(df, mapper, reducer)

result
```

Now students have their own miniature MapReduce framework.

---

# Part 4 — Why not Hadoop initially?

Because there are actually **two different things you want students to understand**:

### 1. MapReduce programming model

```text
Mapper
   ↓
Shuffle
   ↓
Reducer
```

### 2. Hadoop distributed execution

```text
                    Hadoop Cluster
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
   Mapper 1          Mapper 2          Mapper 3
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                  Shuffle / Sort
                         ↓
                Reducer 1 / 2 / 3
                         ↓
                       HDFS
```

If you introduce Hadoop immediately, students can easily become confused by:

* HDFS
* NameNode
* DataNode
* ResourceManager
* NodeManager
* Java
* SSH
* configuration files
* Hadoop Streaming
* mapper/reducer
* permissions
* environment variables

They may learn **Hadoop configuration instead of MapReduce**.

So I'd teach:

> **Python MapReduce → datasets → scaling problem → Hadoop → same MapReduce algorithm on Hadoop.**

That's a much better progression.

---

# Part 5 — Dataset progression

I'd use the following four datasets.

## Dataset 1 — Tiny

Our manually created:

```text
data.txt
```

Purpose:

**Understand Mapper / Shuffle / Reducer**

---

## Dataset 2 — Small

**Online Shoppers Purchasing Intention**

About 12,000 sessions.

It has variables such as administrative activity, product-related activity, bounce rate, exit rate, page values, visitor type and revenue. ([UCI Machine Learning Repository][4])

Purpose:

**MapReduce + Pandas + CSV**

---

## Dataset 3 — Medium

**Clickstream Data for Online Shopping**

UCI reports **165,474 instances and 14 features**. ([UCI Machine Learning Repository][5])

This is a good intermediate dataset.

Potential question:

> What is the average product price by country?

Mapper:

```text
country → price
```

Reducer:

```text
country → average(price)
```

Then introduce:

```text
Mapper
   ↓
Combiner
   ↓
Shuffle
   ↓
Reducer
```

---

## Dataset 4 — Large

**Online Retail**

UCI reports **541,909 transactions**. ([UCI Machine Learning Repository][3])

Questions can become much more realistic:

### Demo

> Calculate total revenue by country.

Mapper:

```text
country → quantity × unit_price
```

Reducer:

```text
country → sum(revenue)
```

Then:

> Find top 10 countries by revenue.

Then:

> Find top products by revenue.

Then:

> Calculate daily revenue.

Then:

> Calculate customer spending.

---

# Part 6 — Very Large Dataset

Finally use **Online Retail II**.

It contains approximately **1.07 million transactions** covering two years. ([UCI Machine Learning Repository][6])

This is where you can deliberately create the problem:

```python
df = pd.read_excel(...)
```

versus:

```text
MapReduce
```

and discuss:

> "What happens when the dataset becomes too large for the memory available to one machine?"

That gives you the natural motivation for Hadoop.

---

# Part 7 — When Hadoop becomes necessary

An important teaching point:

**1 million rows does NOT automatically require Hadoop.**

Your i5/8 GB machine can process datasets of this size with pandas, depending on data types, operations and available disk/RAM.

Hadoop becomes educationally useful when you want to demonstrate:

* distributed storage
* distributed computation
* data partitioning
* parallel mapping
* shuffle
* reducers
* fault tolerance
* scaling across machines

So don't tell students:

> "Big data means you must use Hadoop."

Instead:

> "Hadoop is one approach to distributing storage and computation when a single machine is insufficient or when distributed processing is useful."

---

# Part 8 — Hadoop on an i5 + 8 GB machine

Yes, you can run Hadoop.

But use:

### **Pseudo-distributed / single-node mode**

not a multi-node cluster.

Apache's documentation explicitly provides a single-node setup for running Hadoop on one machine. ([Apache Hadoop][2])

I'd recommend:

```text
i5
8 GB RAM
SSD
Ubuntu/Linux
```

if you have control over the operating system.

For teaching Hadoop, **Ubuntu is the least complicated option** of the three.

---

# Part 9 — Ubuntu Hadoop Setup

For your course, I'd use a current Hadoop 3.x release rather than old Hadoop tutorials you may find online.

### Step 1 — Java

Check:

```bash
java -version
```

Install OpenJDK if necessary:

```bash
sudo apt update
sudo apt install openjdk-17-jdk ssh rsync -y
```

Check:

```bash
java -version
```

---

## Step 2 — Download Hadoop

Download a stable Hadoop binary from the Apache Hadoop distribution site.

For example, after downloading:

```bash
tar -xzf hadoop-*.tar.gz
```

Move it:

```bash
sudo mv hadoop-* /opt/hadoop
```

---

## Step 3 — Environment variables

Edit:

```bash
nano ~/.bashrc
```

Add:

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

export HADOOP_HOME=/opt/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME

export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

Reload:

```bash
source ~/.bashrc
```

Check:

```bash
hadoop version
```

---

# Step 4 — SSH localhost

Hadoop's single-node configuration traditionally uses passwordless localhost SSH. The Apache single-node documentation includes this setup. ([Apache Hadoop][2])

Install:

```bash
sudo apt install openssh-server -y
```

Then:

```bash
ssh-keygen -t ed25519 -P ""
```

Add the key:

```bash
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```

Set permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Test:

```bash
ssh localhost
```

---

# Step 5 — Configure HDFS

Create directories:

```bash
mkdir -p ~/hadoopdata/hdfs/namenode
mkdir -p ~/hadoopdata/hdfs/datanode
```

Edit:

```bash
nano $HADOOP_HOME/etc/hadoop/core-site.xml
```

Use:

```xml
<configuration>

    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>

</configuration>
```

---

### hdfs-site.xml

```bash
nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```

```xml
<configuration>

    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/YOUR_USERNAME/hadoopdata/hdfs/namenode</value>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/YOUR_USERNAME/hadoopdata/hdfs/datanode</value>
    </property>

</configuration>
```

Replace:

```text
YOUR_USERNAME
```

with your actual Linux username.

---

# Step 6 — MapReduce configuration

Create/edit:

```bash
nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
```

```xml
<configuration>

    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>

</configuration>
```

---

# Step 7 — YARN

Edit:

```bash
nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
```

```xml
<configuration>

    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

</configuration>
```

---

# Step 8 — Format NameNode

**Only do this during initial setup.**

```bash
hdfs namenode -format
```

Then:

```bash
start-dfs.sh
start-yarn.sh
```

Check:

```bash
jps
```

You should see processes such as:

```text
NameNode
DataNode
ResourceManager
NodeManager
```

---

# Step 9 — Test HDFS

```bash
hdfs dfs -mkdir -p /demo/input
```

Copy a file:

```bash
hdfs dfs -put data.txt /demo/input/
```

Check:

```bash
hdfs dfs -ls /demo/input
```

Read:

```bash
hdfs dfs -cat /demo/input/data.txt
```

Now Hadoop is ready.

---

# Part 10 — Hadoop Streaming

This is the bridge from our notebook to Hadoop.

Our Python mapper:

```python
for line in sys.stdin:
    ...
```

and reducer:

```python
for line in sys.stdin:
    ...
```

can be executed by Hadoop Streaming.

That's one of the reasons I recommend this approach for your class. Hadoop Streaming allows MapReduce applications to be written using languages other than Java. ([Apache Hadoop][1])

So students can learn:

```text
Notebook
   ↓
Python Mapper
   ↓
Python Reducer
   ↓
Local MapReduce
   ↓
Same Mapper
   ↓
Same Reducer
   ↓
Hadoop Streaming
   ↓
HDFS
```

That's a very strong teaching progression.

---

# Part 11 — Windows

Hadoop on native Windows is possible, but I would **not recommend native Windows Hadoop for a beginner class**.

The problem isn't Python. The complexity comes from Hadoop's Unix-oriented environment and Windows-specific native components/configuration.

For Windows students, I would use:

### Option A — WSL2 ⭐

Install WSL:

```powershell
wsl --install -d Ubuntu
```

Then inside Ubuntu:

```bash
sudo apt update
```

and follow the **Ubuntu Hadoop installation** above.

This gives:

```text
Windows
   │
   └── WSL2
        │
        └── Ubuntu
             │
             └── Hadoop
                  │
                  └── Python
```

For teaching, this is much cleaner than maintaining separate Windows Hadoop instructions.

### Option B — Linux VM

VirtualBox/VMware:

```text
Windows
   ↓
Virtual Machine
   ↓
Ubuntu
   ↓
Hadoop
```

But with only 8 GB RAM, WSL2 is preferable.

---

# Part 12 — macOS

macOS can run Hadoop locally as well.

Install Java:

```bash
brew install openjdk@17
```

Then:

```bash
brew install hadoop
```

Check:

```bash
hadoop version
```

You then configure the Hadoop XML files in:

```text
/usr/local/etc/hadoop/
```

or, on Apple Silicon/Homebrew setups, under the Homebrew prefix, which can differ.

Check:

```bash
brew --prefix hadoop
```

and:

```bash
brew --prefix openjdk@17
```

Then configure:

```text
core-site.xml
hdfs-site.xml
mapred-site.xml
yarn-site.xml
```

using the same single-node configuration concept as Ubuntu.

---

# My recommendation for your class

Don't make students install Hadoop on Day 1.

I'd organize the notebooks like this:

```text
01_word_count.ipynb
        ↓
02_csv_mapreduce.ipynb
        ↓
03_groupby_mapreduce.ipynb
        ↓
04_clickstream_mapreduce.ipynb
        ↓
05_online_retail_mapreduce.ipynb
        ↓
06_large_dataset_mapreduce.ipynb
        ↓
07_hadoop_streaming.ipynb
        ↓
08_hdfs.ipynb
        ↓
09_hadoop_mapreduce.ipynb
        ↓
10_streamlit_dashboard.ipynb
```

And each notebook should follow the **same teaching template**:

```text
1. Download dataset
2. Load dataset
3. Understand dataset
4. Define problem
5. Solve using Pandas
6. Write Mapper
7. Inspect Mapper output
8. Write Shuffle
9. Inspect grouped data
10. Write Reducer
11. Run complete MapReduce pipeline
12. Compare with Pandas
13. Measure execution time
14. Visualize result
15. Explain how Hadoop would execute it
16. Run on Hadoop where appropriate
```

This gives students a very clear progression from **"I know Python/Pandas" → "I understand MapReduce" → "I understand why Hadoop exists" → "I can actually run Python MapReduce on Hadoop."**

And yes, **Streamlit is absolutely possible locally**. The final notebook/project can turn the MapReduce outputs into an interactive dashboard—for example, country revenue, top products, transaction counts, and daily sales—with:

```bash
streamlit run app.py
```

For the datasets, I'd use the UCI Online Retail family because it gives you a particularly clean progression from small/intermediate data to **541K and 1.07M records** from the same real-world domain. ([UCI Machine Learning Repository][3])

If you want, I can next give you **`01_word_count.ipynb` and `02_csv_mapreduce.ipynb` as complete, copy-paste-ready notebook cells**, followed by the four real Internet datasets and the Hadoop version of each.

[1]: https://hadoop.apache.org/docs/r1.0.4/index.pdf?utm_source=chatgpt.com "Overview

1\. Getting Started

The Hadoop documenta"
[2]: https://hadoop.apache.org/docs/stable1/single_node_setup.pdf?utm_source=chatgpt.com "Single Node Setup"
[3]: https://www.archive.ics.uci.edu/dataset/352/online%2Bretail?utm_source=chatgpt.com "UCI Machine Learning Repository"
[4]: https://www.archive.ics.uci.edu/dataset/468/online%20shoppers%20purchasing%20intention%20dataset?utm_source=chatgpt.com "UCI Machine Learning Repository"
[5]: https://www.archive.ics.uci.edu/dataset/553/clickstream%2Bdata%2Bfor%2Bonline%2Bshopping?utm_source=chatgpt.com "UCI Machine Learning Repository"
[6]: https://archive.ics.uci.edu/dataset/502/online%2Bretail?utm_source=chatgpt.com "UCI Machine Learning Repository"
