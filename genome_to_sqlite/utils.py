COLUMNS = ("rsid", "chromosome", "position", "genotype")


def convert_genome_text_to_sqlite(fp, db, progress_callback=None):
    # Need to call progress_callback with number of bytes processed each time
    if progress_callback is None:
        progress_callback = lambda n: n

    def yield_rows():
        for line in fp.readlines():
            progress_callback(len(line))
            if line.startswith(b"#"):
                continue
            bits = line.decode("utf-8").strip().split("\t")
            row = dict(zip(COLUMNS, bits))
            row["position"] = int(row["position"])
            yield row

    db["genome"].upsert_all(yield_rows(), pk="rsid")
    db["genome"].create_index(["chromosome"], if_not_exists=True)
