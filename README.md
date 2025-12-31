This notebook visualizes the execution trace in nanoseconds after execution of the [iot-firehose](https://github.com/davidmenggx/iot-firehose) /readings/slow/pooling API endpoint for any number of concurrent users. 

The /readings/slow/pooling endpoint uses an asyncpg connection pool to write to a PostgreSQL database. I use the logging module to capture the timestamp of seven critical execution events including acquiring the connection pool, beginning the database transaction, finishing the database transaction, releasing the connection pool, and returning a success message. 

The plotly visualization tool can accomodate any number of concurrent requests and increased granularity of logging messages, as long as they are consistent with the existing logs in the /readings/slow/pooling endpoint.

This visualization highlights how the event loop handles task switching and identifies potential contention points within the connection pool when multiple users hit the endpoint simultaneously.

Execution trace with 7 concurrent requests:
<img width="1424" height="715" alt="seven_executions" src="https://github.com/user-attachments/assets/a85dafd7-898b-499c-9629-5679e7427833" />

Execution trace with 10 concurrent requests:
<img width="1424" height="715" alt="ten_executions" src="https://github.com/user-attachments/assets/423cc136-d152-4b6f-a84d-b8dc201bf249" />

Execution trace with 25 concurrent requests:
<img width="1424" height="715" alt="twentyfive_executions" src="https://github.com/user-attachments/assets/0acd89a2-ea0f-46a4-ae7f-2f73059eec3f" />

