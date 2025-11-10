Tolkien Fan Club Static Site Generator
Builds a small static site from Markdown using Python. Supports local dev and GitHub Pages deployment.

Features
Markdown → HTML (inline + block)
Template-based pages ({{ Title }}, {{ Content }})
Copies static assets
Configurable base path (/ or /REPO_NAME/)
Outputs to docs/ for GitHub Pages

Structure

content/: markdown
static/: css/images
src/: generator/parsers
template.html
docs/: built site
build.sh

Usage

Local build (base path “/”):
python3 src/main.py
Serve: python3 -m http.server -d docs 8888
Prod build (GitHub Pages):
bash build.sh # runs: python3 src/main.py "/REPO_NAME/"
Commit/push docs/
GitHub Settings → Pages → main /docs
Visit https://USERNAME.github.io/REPO_NAME/

Notes

Routes map from content:
content/index.md → /
content/blog/tom/index.md → /blog/tom
Links and assets starting with / are rewritten to base path (href/src).

Tests
bash test.sh

Troubleshooting

Broken assets on Pages: rebuild with "/REPO_NAME/", ensure Pages set to main /docs.
404 locally: serve docs/ directory.

Credit: Built as part of a Boot.dev project.

PT-BR:

Gerador de Site Estático – Tolkien Fan Club
Gera um site estático a partir de Markdown em Python. Suporta desenvolvimento local e deploy no GitHub Pages.

Recursos
Markdown → HTML (inline + bloco)
Páginas com template ({{ Title }}, {{ Content }})
Cópia de assets estáticos
Base path configurável (/ ou /REPO_NAME/)
Saída em docs/ para GitHub Pages

Estrutura

content/: markdown
static/: css/imagens
src/: gerador/parsers
template.html
docs/: site gerado
build.sh

Uso

Build local (base path “/”):
python3 src/main.py
Servir: python3 -m http.server -d docs 8888
Build de produção (GitHub Pages):
bash build.sh # executa: python3 src/main.py "/REPO_NAME/"
Commit/push de docs/
GitHub Settings → Pages → main /docs
Acesse: https://USERNAME.github.io/REPO_NAME/

Notas

Rotas mapeadas de content:
content/index.md → /
content/blog/tom/index.md → /blog/tom
Links e assets começando com / são reescritos para o base path (href/src).

Testes
bash test.sh

Solução de problemas

Assets quebrados no Pages: faça build com "/REPO_NAME/" e confirme Pages em main /docs.
404 local: sirva o diretório docs/.

Crédito: Construído como parte de um projeto da Boot.dev.