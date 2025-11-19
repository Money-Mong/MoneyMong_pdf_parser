def insert_summary(db, DocumentSummary, document_id, summary):
    existing = db.query(DocumentSummary).filter_by(document_id=document_id).first()

    if existing:
        # update
        existing.summary_short = summary["summary_short"]
        existing.summary_long = summary["summary_long"]
        existing.key_points = summary.get("key_points", [])
        existing.entities = summary.get("entities", {})
        existing.model_version = summary["model_version"]
        db.flush()
        return existing.id

    # create new
    new_summary = DocumentSummary(
        document_id=document_id,
        summary_short=summary["summary_short"],
        summary_long=summary["summary_long"],
        key_points=summary.get("key_points", []),
        entities=summary.get("entities", {}),
        model_version=summary["model_version"],
    )
    db.add(new_summary)
    db.flush()
    return new_summary.id
