"""Hack assembler (Nand2Tetris). Usage: python assembler.py Prog.asm
Extra feature depends on K = last two digits of roll number."""
import sys

K = 91
FEATURE = K % 3             # 0: symbols.txt, 1: error messages, 2: duplicate label warning

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101'
}

DEST = {
    '': '000', 'M': '001', 'D': '010',
    'MD': '011', 'DM': '011',
    'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
}

JUMP = {
    '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
    'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
}


def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(path):
    symbols = {
        'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
        'SCREEN': 16384, 'KBD': 24576
    }
    symbols.update({f'R{i}': i for i in range(16)})

    lines = []
    errors = []
    labels = {}

    # ---------- First pass: labels ----------
    pc = 0
    with open(path, encoding='utf-8', errors='replace') as f:
        for n, raw in enumerate(f, 1):
            line = clean(raw)
            if not line:
                continue
            if line.startswith('('):
                if not line.endswith(')') or len(line) < 3:
                    errors.append(f'Line {n}: invalid instruction')
                    continue
                name = line[1:-1]
                if name in labels and FEATURE == 2:
                    print(f'Warning: Line {n}: label ({name}) already defined')
                labels[name] = pc
                symbols[name] = pc
            else:
                lines.append((n, line))
                pc += 1

    # ---------- Second pass: translate ----------
    out, next_var = [], 16
    for n, line in lines:
        try:
            if line.startswith('@'):
                s = line[1:]
                if not s:
                    raise ValueError('invalid instruction')
                if s.isdigit():
                    val = int(s)
                    if val > 32767:
                        raise ValueError('invalid instruction')
                else:
                    if s not in symbols:
                        symbols[s] = next_var
                        next_var += 1
                    val = symbols[s]
                out.append(format(val, '016b'))
            else:
                dest, jump = '', ''
                if '=' in line:
                    dest, line = line.split('=', 1)
                if ';' in line:
                    line, jump = line.split(';', 1)
                if line not in COMP or dest not in DEST or jump not in JUMP:
                    raise ValueError('invalid instruction')
                out.append('111' + COMP[line] + DEST[dest] + JUMP[jump])
        except ValueError as e:
            if FEATURE == 1:
                errors.append(f'Line {n}: {e}')
            else:
                raise

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    hack = path.rsplit('.', 1)[0] + '.hack'
    with open(hack, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')

    if FEATURE == 0:
        with open('symbols.txt', 'w', encoding='utf-8') as f:
            for name, addr in symbols.items():
                f.write(f'{name} {addr}\n')

    print(f'Written {hack} ({len(out)} instructions)')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python assembler.py Prog.asm')
        sys.exit(1)
    assemble(sys.argv[1])