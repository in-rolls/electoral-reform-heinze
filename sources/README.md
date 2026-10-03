# Source acquisition

Retrieved October 2, 2026. All downloads were public and required no token.

| Local file | Exact source |
|---|---|
| `dataverse-metadata.json` | `https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/QGH7P4` |
| `dataverse-v1.0-original.zip` | `https://dataverse.harvard.edu/api/access/dataset/:persistentId/versions/1.0?persistentId=doi:10.7910/DVN/QGH7P4&format=original` |
| `paper.pdf` | `https://alyssaheinze.github.io/docs/democratic-deepening-or-elite-persistence-how-local-elites-adapt-to-electoral-reform-in-rural-india.pdf` |
| `appendix.pdf` | `https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS0003055425101068/resource/name/S0003055425101068sup001.pdf` |

The archive contains all 113 deposited files. Original CSV format was requested rather than Dataverse's ingested TAB export. Every original file matches the MD5 listed by Dataverse. No missing/restricted file was inferred from the archive alone: the file list was reconciled against dataset metadata.

`paper.txt` and `appendix.txt` were extracted using `pdftotext -layout`; PDFs are the authoritative source for page layout. Questionnaire and codebook DOCX files reside in the archive's `documentation/` directory and are extracted by `make verify`.

The version-pinned archive and downloaded PDFs have never been rewritten. `SHA256SUMS` and `file-manifest.csv` were initialized once, after download, then verified throughout execution. The generated ZIP is the server's complete export, not a locally repackaged substitute.

API behavior was checked against [Dataverse's official Data Access API documentation](https://guides.dataverse.org/en/latest/api/dataaccess.html). The dataset metadata records the deposit's CC0 terms; the paper states CC BY 4.0. These source terms remain separate from the new audit code.
