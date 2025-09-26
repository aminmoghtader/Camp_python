def main():
    try:

        filename = input().strip()


        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]


        if len(lines) % 2 != 0:
            raise ValueError

        results = []
        for i in range(0, len(lines), 2):

            try:
                a, b = map(float, lines[i].split())
            except:
                raise ValueError


            op = lines[i + 1]
            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            elif op == "/":
                if b == 0:
                    raise ZeroDivisionError
                res = a / b
            else:
                raise ValueError

            results.append(f"{res:.2f}")


        print("[" + ", ".join(results) + "]")

    except:
        print("Invalid input or file")


if __name__ == "__main__":
    main()
