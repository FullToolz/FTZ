import os


def main(path):
    def find_suspicious_patterns(path, window=20):
        with open(path, "rb") as f:
            data = f.read()

        hits = []

        for i in range(len(data)):
            b = data[i]

            # Short conditional jumps (Jcc)
            if 0x70 <= b <= 0x7F:
                context = data[max(0, i - window) : i]
                if any(c in range(0x30, 0x36) for c in context):  # XOR nearby
                    hits.append(("JCC + XOR", i))
                elif any(c in range(0x38, 0x3E) for c in context):  # CMP nearby
                    hits.append(("JCC + CMP", i))
                elif any(c in (0x84, 0x85) for c in context):  # TEST nearby
                    hits.append(("JCC + TEST", i))

            # Near conditional jumps (0F 8x)
            if b == 0x0F and i + 1 < len(data) and 0x80 <= data[i + 1] <= 0x8F:
                context = data[max(0, i - window) : i]
                if any(c in range(0x30, 0x36) for c in context):
                    hits.append(("JCC(near) + XOR", i))
                else:
                    hits.append(("JCC(near)", i))

        return hits

    def render_patterns(module, patterns):
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(
            title=f"[bold red]Suspicious Control-Flow → {os.path.basename(module)}",
            show_lines=True,
        )

        table.add_column("Pattern", style="magenta")
        table.add_column("Offset", style="yellow")

        for kind, offset in patterns:
            table.add_row(kind, hex(offset))

        console.print(table)

    # path = input("Enter path to EXE or DLL: ").strip().strip('"')

    patterns = find_suspicious_patterns(path)
    render_patterns(path, patterns)


