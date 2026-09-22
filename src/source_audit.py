"""Mokymo failų tapatybės patikra, leidžianti vien komentarų ir tarpų pakeitimus."""
import ast
import hashlib
import io
import tokenize
from pathlib import Path


def verify_training_source(project, relative, expected_hash):
    # Pirmiausia tikrinama tiksli mokymo manifesto kontrolinė suma.
    # Jei failas dokumentuotas vėliau, originalas privalo atitikti tą patį manifestą.
    project = Path(project)
    current = (project / relative).read_bytes()
    if hashlib.sha256(current).hexdigest() == expected_hash:
        return
    original = (project / 'audit' / 'training_sources' / relative).read_bytes()
    if hashlib.sha256(original).hexdigest() != expected_hash:
        raise ValueError(f'Originalus mokymo failas neatitinka manifesto: {relative}')

    def signature(content):
        # Ignoruojami tik komentarai ir fizinių eilučių tarpai; vykdomi tokenai lieka.
        # AST papildomai patikrina įtraukų nulemtą struktūrą. Docstring pakeitimai neleidžiami.
        source = content.decode('utf-8-sig')
        ignored = {tokenize.COMMENT, tokenize.NL, tokenize.ENCODING}
        tokens = [(t.type, t.string if t.type not in (tokenize.INDENT, tokenize.NEWLINE) else '')
                  for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type not in ignored]
        return ast.dump(ast.parse(source), include_attributes=False), tokens

    if signature(current) != signature(original):
        raise ValueError(f'Pasikeitė vykdomas mokymo kodas, ne vien komentarai: {relative}')
