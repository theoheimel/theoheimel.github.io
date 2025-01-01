import json
from urllib.request import urlopen

url = "https://inspirehep.net/api/literature?sort=mostrecent&size=100&q=f+a+Heimel,+T"
max_authors = 6

with urlopen(url) as f:
    response = json.load(f)

with open("_data/publications.yaml", "w") as f:
    publications = response["hits"]["hits"]
    for publication in publications:
        pub_meta = publication["metadata"]
        title = pub_meta["titles"][0]["title"]
        if "arxiv_eprints" not in pub_meta:
            continue
        arxiv_id = pub_meta["arxiv_eprints"][0]["value"]
        if "publication_info" in pub_meta:
            journal_info = pub_meta["publication_info"][0]
            journal = (
                f"{journal_info['journal_title']} {journal_info['journal_volume']}, "
                f"{journal_info['artid']} ({journal_info['year']})"
            )
            if "dois" in pub_meta:
                doi = pub_meta["dois"][0]["value"]
            else:
                doi = None
        else:
            journal = None
            doi = None
        n_authors = len(pub_meta["authors"])
        authors = ", ".join(
            f"{author['first_name'][:1]}. {author['last_name']}"
            for author, _ in zip(pub_meta["authors"], range(max_authors if n_authors < 20 else 1))
        )
        if n_authors > max_authors:
            authors += " et al."
        f.write("\n".join([
            f'- authors: "{authors}"',
            f'  title: "{title}"',
            f'  arxiv: "{arxiv_id}"',
            *([f'  journal: "{journal}"'] if journal is not None else []),
            *([f'  doi: "{doi}"'] if doi is not None else []),
        ]))
        f.write('\n')

