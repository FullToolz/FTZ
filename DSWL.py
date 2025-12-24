def main(path):
    def find_lea_string_decoders(path, window=32):
        with open(path, "rb") as f:
            data = f.read()

        hits = []

        for i in range(len(data)):
            if data[i] == 0x8D:  # LEA
                context = data[i : i + window]

                has_xor = any(0x30 <= b <= 0x35 for b in context)
                has_math = any(
                    b in range(0x00, 0x06) or b in range(0x28, 0x2E) for b in context
                )

                if has_xor:
                    hits.append(("LEA + XOR (string decode?)", i))
                elif has_math:
                    hits.append(("LEA + ADD/SUB (string build?)", i))

        return hits

    # path = input("Enter path to EXE or DLL: ").strip().strip('"')
    find_lea_string_decoders(path)
