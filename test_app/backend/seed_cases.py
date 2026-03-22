from cases_db import ensure_cases_table, seed_default_case


def main():
    ensure_cases_table()
    seed_default_case()
    print("Cases table is ready and default case has been seeded if missing.")


if __name__ == "__main__":
    main()
