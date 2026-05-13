import hashlib

def anonymize_employee_id(emp_id):
    """Return a SHA-256 hash of the employee ID for aggregated analytics."""
    return hashlib.sha256(str(emp_id).encode()).hexdigest()[:12]

def mask_sensitive_data(df, columns=['employee_id']):
    """Replace real IDs with anonymised versions."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(anonymize_employee_id)
    return df