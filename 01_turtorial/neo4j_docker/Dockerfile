FROM neo4j:latest

# https://github.com/langchain-ai/langchain/issues/12901#issuecomment-1793683181
ENV NEO4J_dbms_security_procedures_unrestricted=apoc.*
ENV NEO4J_dbms_security_procedures_allowlist=apoc.*

ENV NEO4J_AUTH=neo4j/pleaseletmein

ENV NEO4JLABS_PLUGINS='["apoc"]'
ENV NEO4J_apoc_export_file_enabled=true
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_import_file_use__neo4j__config=true