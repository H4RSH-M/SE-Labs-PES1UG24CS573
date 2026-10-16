"""Manage school bus rider registrations, rosters, dispatch, and fees."""

import sqlite3


def enroll_rider(connection, student, route, stop, fee):
    """Register a student on a bus route."""
    connection.execute(
        """
        INSERT INTO riders (student, route, stop, fee)
        VALUES (?, ?, ?, ?)
        """,
        (student, route, stop, fee),
    )
    connection.commit()


def route_roster(connection, route):
    """Return the names of students registered on a route."""
    cursor = connection.execute(
        "SELECT student FROM riders WHERE route = ?",
        (route,),
    )
    return [row[0] for row in cursor.fetchall()]


def export_roster(connection, path, route):
    """Export a route's student roster to a text file."""
    with open(path, "w", encoding="utf-8") as output_file:
        for student in route_roster(connection, route):
            output_file.write(f"{student}\n")


def dispatch_alert(route):
    """Display a dispatch alert for the specified route."""
    print(f"Dispatching bus {route}")


def fee_collected(connection, route):
    """Return the total fees collected for a route."""
    cursor = connection.execute(
        """
        SELECT COALESCE(SUM(fee), 0)
        FROM riders
        WHERE route = ?
        """,
        (route,),
    )
    return cursor.fetchone()[0]


def main():
    """Run a demonstration of the school transport register."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            """
            CREATE TABLE riders (
                id INTEGER PRIMARY KEY,
                student TEXT,
                route TEXT,
                stop TEXT,
                fee INTEGER
            )
            """
        )

        enroll_rider(connection, "Tara", "R1", "Lake Road", 1800)
        enroll_rider(connection, "Kabir", "R1", "Mill Street", 1800)
        enroll_rider(connection, "Zoya", "R2", "Fort Gate", 2100)

        if fee_collected(connection, "R1") != 3600:
            raise ValueError("Fee total for route R1 is incorrect")

        export_roster(connection, "route_r1.txt", "R1")
        dispatch_alert("R1")
        print(route_roster(connection, "R2"))


if __name__ == "__main__":
    main()
