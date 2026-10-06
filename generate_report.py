import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet


def generate_report():

    conn = sqlite3.connect(
        "database/attacks.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            ip_address,
            attack_type,
            severity,
            timestamp

        FROM attacks

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    document = SimpleDocTemplate(
        "reports/attack_report.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(
            "<b>HoneyTrapX Attack Report</b>",
            styles["Title"]
        )

    )

    elements.append(
        Spacer(1, 20)
    )

    data = [

        [
            "IP Address",
            "Attack Type",
            "Severity",
            "Timestamp"
        ]

    ]

    data.extend(rows)

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            )

        ])

    )

    elements.append(
        table
    )

    document.build(
        elements
    )

    print(
        "Report generated successfully."
    )


if __name__ == "__main__":

    generate_report()
