import pandas as pd
import networkx as nx
import pickle
from email.utils import getaddresses
from tqdm import tqdm

# --- Configuration ---
input_csv_file = 'emails.csv'
output_graph_file = 'enron_graph.gpickle'

def clean_email_addresses(addresses):
    """
    Cleans a string of one or more email addresses.
    Returns a list of clean, lowercase email addresses.
    """
    if pd.isna(addresses):
        return []
    
    # Use email.utils.getaddresses to handle complex formats
    # It returns a list of (real_name, email_address) tuples
    cleaned_addresses = [addr.lower() for name, addr in getaddresses([addresses]) if '@' in addr]
    return cleaned_addresses

# --- Main Script ---
print(f"Reading email data from {input_csv_file}...")
# Read the CSV into a pandas DataFrame
df = pd.read_csv(input_csv_file)

print("Building the communication graph...")
# Create a directed graph
G = nx.DiGraph()

# Use tqdm for a progress bar
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing Emails"):
    # Clean the 'From' address (should only be one)
    from_addr = clean_email_addresses(row['From'])
    if not from_addr:
        continue # Skip if sender is invalid
    
    sender = from_addr[0]
    
    # Clean the 'To' addresses (can be multiple)
    to_addrs = clean_email_addresses(row['To'])
    
    # Add sender as a node
    if not G.has_node(sender):
        G.add_node(sender)
    
    for recipient in to_addrs:
        # Add recipient as a node
        if not G.has_node(recipient):
            G.add_node(recipient)
        
        # Add or update the edge between sender and recipient
        if G.has_edge(sender, recipient):
            # If the edge already exists, increment its weight
            G[sender][recipient]['weight'] += 1
        else:
            # Otherwise, create the edge with a weight of 1
            G.add_edge(sender, recipient, weight=1)

print("\nGraph construction complete.")
print(f"Total nodes (people): {G.number_of_nodes()}")
print(f"Total edges (interactions): {G.number_of_edges()}")

# Save the graph object to a file using pickle
with open(output_graph_file, 'wb') as f:
    pickle.dump(G, f)

print(f"\nGraph has been pre-processed and saved to {output_graph_file}")
print("This file is the 'brain' for our web application.")