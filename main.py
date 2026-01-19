from rdbms.engine import execute

print("Simple RDBMS REPL")
print("Type 'exit' to quit")

while True:
    sql = input("rdbms> ")

    if sql.lower() in ("exit", "quit"):
        break

    try:
        result = execute(sql)
        print(result)
    except Exception as e:
        print("Error:", e)
