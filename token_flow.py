import streamlit as st
from web3 import Web3
import pandas as pd
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# Initialize Web3
INFURA_URL = "https://mainnet.infura.io/v3/49c545ef2e02474298e4f40d34bd230d"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

st.title("On-Chain Token Flow Visualizer 🛰️")
target_wallet = st.text_input("Enter Wallet Address:", "0x28C6c06298d514Db089934071355E5743bf21d60") # Binance Hot Wallet 1 As Example

# Mock Data Generator to simulate real data extraction for visualization
def get_mock_token_flows(center_wallet):
    return [
        {"From": center_wallet, "To": "0xAddressA", "Value": 45.2, "Type": "Outflow"},
        {"From": center_wallet, "To": "0xAddressB", "Value": 12.0, "Type": "Outflow"},
        {"From": "0xAddressC", "To": center_wallet, "Value": 110.5, "Type": "Inflow"},
        {"From": "0xAddressA", "To": "0xAddressD", "Value": 25.0, "Type": "Hop-2 Outflow"},
        {"From": "0xAddressB", "To": "0xAddressD", "Value": 10.0, "Type": "Hop-2 Outflow"},
    ]

if st.button("Generate Token Flow Network Graph"):
    with st.spinner("Analyzing transaction hops..."):
        # Fetch flow records
        flows = get_mock_token_flows(target_wallet)
        df = pd.DataFrame(flows)
        
        # --- GRAPH VISUALIZATION SETUP ---
        st.subheader("Interactive Flow Topology")
        
        nodes = []
        edges = []
        
        # Find unique addresses across sender/receivers
        unique_addresses = set(df['From'].tolist() + df['To'].tolist())
        
        # 1. Create Nodes with behavioral aesthetics
        for addr in unique_addresses:
            # Highlight target wallet distinctly
            if addr.lower() == target_wallet.lower():
                nodes.append(Node(id=addr, label="TARGET WALLET", size=30, color="#FF4B4B"))
            else:
                short_label = f"{addr[:6]}...{addr[-4:]}"
                nodes.append(Node(id=addr, label=short_label, size=18, color="#1F77B4"))
                
        # 2. Create Directed Edges mapping transaction size
        for _, row in df.iterrows():
            edges.append(Edge(
                source=row['From'], 
                target=row['To'], 
                label=f"{row['Value']} ETH",
                type="CURVED_SMOOTH", 
                width=max(1, int(row['Value'] / 10)) # Thicker lines for bigger transactions
            ))
            
        # 3. Configure Layout Options (Physics Engine Controls)
        config = Config(
            width=700,
            height=500,
            directed=True,
            physics=True,
            hierarchicalLayout=False
        )
        
        # 4. Render Graph inside Streamlit
        agraph(nodes=nodes, edges=edges, config=config)
        
        # --- TABULAR AUDIT DATA ---
        st.subheader("Transaction Flow Ledger")
        st.dataframe(df, use_container_width=True)