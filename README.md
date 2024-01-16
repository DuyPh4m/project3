# Match results Analytics and Statistics Project

Analytics and Statistics for football match results.

## Table of Contents

- [Match results Analytics and Statistics Project](#match-results-analytics-and-statistics-project)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation

1. Clone the repository.
    ```bash
    git clone https://github.com/DuyPh4m/IT4931.git
    ```

2. Navigate to the project directory.
    ```bash
    cd IT4931
    ```

3. Install the dependencies.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the containers. (you can add "-d" to run in background and check logs with "docker logs container_name")
    ```bash
    docker-compose -f docker-compose-all.yml up
    ```

2. Run `Kafka` setup script.
    ```bash
    bash kafka/setup.sh
    ```
3. Run `Cassandra` setup script after Cassandra logs "Created superuser role 'cassandra'"
    ```
    docker exec -it cassandra bash -c "bash /app/setup.sh"
    ```
4. Submit Data processing and `Cassandra` stroing to `Spark` cluster. Monitor the progress [here](http://localhost:8080).
    ```bash
    bash spark/process.sh 
    ```
5. Run the producer.
    ```bash
    python producer.py
    ```
6. Submit Data for visualization to `ElasticSearch`. Monitor the progress [here](http://localhost:8080).
    ```bash
    bash spark/elasticsearch.sh 
    ```
7. Data visualization [here](http://localhost:5601)


