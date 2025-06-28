# 2. Data persistence

Date: 2025-06-28

## Status

Accepted

## Context

The application requires to store data aswell as it's decision matrix. For this, a database is required.
In the past, several different database-like approaches were used, such as:

Distrochooser 1,2: Flat file (especially `JSON`)
Distrochooser 3, 4: MySQL/ MariaDB
Distrochooser 5: Postgres

As the nature of the database, there is the need for high performing databases, especially in the context as the database must be performing well on limited resources
inside of a container.

## Decision

Based on the current available infrastrcture, Postgres showed the best performance and the project will stick to that database vendor for now.

Local dev environments can fall back to SQLite for testing, **no Postgres-specific features shall be used**

## Consequences

We need some kind of ORM to prevent having to write the SQL by ourself and to be indepenendend as far as possible from the database itself.
The infrastructure needs to provide a suitable database server.