# digital-download-zip-packer

Pack a product folder into a clean customer-facing ZIP that always includes a README.

## Requirements

- Python 3.9+

## Usage

```bash
# Pack ./product-files into dist/my-product.zip with an auto README
python zip_packer.py ./product-files --name my-product --out dist

# Use your own customer README template
python zip_packer.py ./product-files --name my-product --readme customer_readme_template.md
```

The script:
1. Copies the source folder into a temp build dir
2. Writes / overwrites `README.txt` for the buyer
3. Creates `dist/<name>.zip`

Skips common junk: `.DS_Store`, `__MACOSX`, `.git`.

## License

MIT
