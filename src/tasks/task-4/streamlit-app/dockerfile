# Use the OSRM backend image
FROM osrm/osrm-backend

# Set the working directory
WORKDIR /app

COPY bhopal.osrm /app/bhopal.osrm
COPY bhopal.osrm.cell_metrics /app/bhopal.osrm.cell_metrics
COPY bhopal.osrm.cells /app/bhopal.osrm.cells
COPY bhopal.osrm.cnbg /app/bhopal.osrm.cnbg
COPY bhopal.osrm.cnbg_to_ebg /app/bhopal.osrm.cnbg_to_ebg
COPY bhopal.osrm.datasource_names /app/bhopal.osrm.datasource_names
COPY bhopal.osrm.ebg /app/bhopal.osrm.ebg
COPY bhopal.osrm.ebg_nodes /app/bhopal.osrm.ebg_nodes
COPY bhopal.osrm.edges /app/bhopal.osrm.edges
COPY bhopal.osrm.enw /app/bhopal.osrm.enw
COPY bhopal.osrm.fileIndex /app/bhopal.osrm.fileIndex
COPY bhopal.osrm.geometry /app/bhopal.osrm.geometry
COPY bhopal.osrm.icd /app/bhopal.osrm.icd
COPY bhopal.osrm.maneuver_overrides /app/bhopal.osrm.maneuver_overrides
COPY bhopal.osrm.mldgr /app/bhopal.osrm.mldgr
COPY bhopal.osrm.names /app/bhopal.osrm.names
COPY bhopal.osrm.nbg_nodes /app/bhopal.osrm.nbg_nodes
COPY bhopal.osrm.partition /app/bhopal.osrm.partition
COPY bhopal.osrm.properties /app/bhopal.osrm.properties
COPY bhopal.osrm.ramIndex /app/bhopal.osrm.ramIndex
COPY bhopal.osrm.restrictions /app/bhopal.osrm.restrictions
COPY bhopal.osrm.timestamp /app/bhopal.osrm.timestamp
COPY bhopal.osrm.tld /app/bhopal.osrm.tld
COPY bhopal.osrm.tls /app/bhopal.osrm.tls
COPY bhopal.osrm.turn_duration_penalties /app/bhopal.osrm.turn_duration_penalties
COPY bhopal.osrm.turn_penalties_index /app/bhopal.osrm.turn_penalties_index
COPY bhopal.osrm.turn_weight_penalties /app/bhopal.osrm.turn_weight_penalties


# Expose the default OSRM HTTP port
EXPOSE 7860

# Run the OSRM backend server with preprocessed data
ENTRYPOINT [ "osrm-routed", "--algorithm", "mld", "--port", "7860", "/app/bhopal.osrm" ]